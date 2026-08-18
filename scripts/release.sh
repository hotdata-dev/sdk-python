#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

die() { echo "error: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "$1 is required"; }

# An interpreter that can `import tomllib`, which is stdlib only from 3.11.
#
# `python3` carries no version guarantee, and this package's own requires-python
# is >=3.10 — so hardcoding it meant the release script could not run on the
# oldest Python the package claims to support. No workflow runs this script; only
# a human cutting a release does, which is why it went unnoticed for so long. The
# symptom was a bare ModuleNotFoundError, which reads as a broken checkout rather
# than a too-old interpreter.
#
# `uv` is the fallback because `prepare` below already shells out to `uv lock`
# when a uv.lock is present, so a machine able to cut a release here already has
# it. (CI installs with pip, so this is about the local release path only.)
resolve_python() {
  if command -v python3 >/dev/null 2>&1 && python3 -c "import tomllib" >/dev/null 2>&1; then
    echo python3
  elif command -v uv >/dev/null 2>&1; then
    # `>=3.11` not `3.12`: an exact request downloads a managed interpreter when
    # the machine's uv-visible one is 3.11 or 3.13, and fails outright under
    # UV_PYTHON_DOWNLOADS=never. It reads like a redirect but is not one —
    # $PY_BIN is expanded unquoted for word splitting, and bash does not rescan
    # expansion results for redirection operators, so uv receives it literally.
    echo "uv run --no-project --python >=3.11 python"
  else
    die "need python3 >= 3.11 (for tomllib) or uv; python3 is $(command -v python3 >/dev/null 2>&1 && python3 -V 2>&1 || echo absent)"
  fi
}

# Deferred, not resolved at load: the commands that never touch Python must keep
# working without a usable interpreter — otherwise the message telling you which
# interpreter you need is itself gated on having it, and `--help` breaks on
# exactly the machine this resolution exists for. Empty default satisfies `set -u`
# if a helper is ever reached by another path.
PY_BIN=""

usage() {
  cat <<'EOF'
Usage:
  ./scripts/release.sh prepare [patch|minor|major|X.Y.Z]
  ./scripts/release.sh publish

Workflow:
  1. Move notes from [Unreleased] in CHANGELOG.md (or add them there).
  2. ./scripts/release.sh prepare patch
  3. Merge the release PR.
  4. ./scripts/release.sh publish

Tag push triggers PyPI publish and GitHub Release creation in CI.
EOF
}

get_version() {
  $PY_BIN - <<'PY'
import tomllib
from pathlib import Path
print(tomllib.loads(Path("pyproject.toml").read_text())["project"]["version"])
PY
}

get_pkg_name() {
  $PY_BIN - <<'PY'
import tomllib
from pathlib import Path
print(tomllib.loads(Path("pyproject.toml").read_text())["project"]["name"])
PY
}

set_version() {
  local ver="$1"
  $PY_BIN - "$ver" <<'PY'
import re, sys
from pathlib import Path
ver = sys.argv[1]
path = Path("pyproject.toml")
text = path.read_text()
new, n = re.subn(r'(?m)^version = "[^"]+"', f'version = "{ver}"', text, count=1)
if n != 1:
    raise SystemExit("could not update version in pyproject.toml")
path.write_text(new)
PY
}

bump_version() {
  local kind="$1" current="$2"
  $PY_BIN - "$kind" "$current" <<'PY'
import re, sys
kind, current = sys.argv[1], sys.argv[2]
match = re.match(r"^(\d+)\.(\d+)\.(\d+)(.*)$", current)
if not match:
    raise SystemExit(f"unsupported version: {current}")
major, minor, patch, suffix = int(match[1]), int(match[2]), int(match[3]), match[4]
if suffix:
    raise SystemExit("pre-release versions must be set explicitly as X.Y.Z")
if kind == "patch":
    patch += 1
elif kind == "minor":
    minor += 1
    patch = 0
elif kind == "major":
    major += 1
    minor = 0
    patch = 0
else:
    raise SystemExit(f"unknown bump kind: {kind}")
print(f"{major}.{minor}.{patch}")
PY
}

default_branch() {
  local remote="${1:-origin}"
  git symbolic-ref --quiet "refs/remotes/${remote}/HEAD" 2>/dev/null | sed "s|refs/remotes/${remote}/||" \
    || { git branch -r | sed -n "s|^  ${remote}/\\(main\\|master\\)$|\\1|p" | head -1; } \
    || echo main
}

ensure_clean() {
  [[ -z "$(git status --porcelain)" ]] || die "working tree is not clean"
}

update_changelog() {
  local ver="$1"
  local date
  date="$(date +%Y-%m-%d)"
  $PY_BIN scripts/update_changelog.py "$ver" "$date"
}

cmd_prepare() {
  local bump="${1:-}"
  [[ -n "$bump" ]] || { usage; die "missing bump kind or explicit version"; }
  need gh
  PY_BIN="$(resolve_python)"
  ensure_clean

  local current new base branch pkg
  current="$(get_version)"
  if [[ "$bump" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    new="$bump"
  else
    new="$(bump_version "$bump" "$current")"
  fi
  [[ "$new" != "$current" ]] || die "new version ($new) equals current ($current)"

  base="$(default_branch)"
  git fetch origin "$base"
  git checkout "$base"
  git pull --ff-only origin "$base"
  ensure_clean

  set_version "$new"
  update_changelog "$new"
  if command -v uv >/dev/null 2>&1 && [[ -f uv.lock ]]; then
    uv lock
  fi

  branch="release/v${new}"
  git checkout -b "$branch"
  git add pyproject.toml CHANGELOG.md
  [[ -f uv.lock ]] && git add uv.lock
  git commit -m "chore: release v${new}"

  pkg="$(get_pkg_name)"
  git push -u origin "$branch"
  gh pr create --base "$base" --head "$branch" \
    --title "chore: release ${pkg} v${new}" \
    --body "## Summary
Release **${pkg} v${new}**.

## Checklist
- [x] Version bumped in \`pyproject.toml\`
- [x] \`CHANGELOG.md\` updated
- [ ] CI green

After merge, run \`./scripts/release.sh publish\` from a clean \`${base}\` checkout."

  echo "Prepared ${pkg} v${new}. Merge the PR, then run: ./scripts/release.sh publish"
}

cmd_publish() {
  need gh
  PY_BIN="$(resolve_python)"
  ensure_clean

  local base ver tag
  base="$(default_branch)"
  git fetch origin "$base"
  git checkout "$base"
  git pull --ff-only origin "$base"
  ensure_clean

  ver="$(get_version)"
  tag="v${ver}"

  git rev-parse "$tag" >/dev/null 2>&1 && die "tag $tag already exists"
  [[ -f CHANGELOG.md ]] || die "CHANGELOG.md is required"
  $PY_BIN - "$ver" <<'PY'
import re, sys
from pathlib import Path
ver = sys.argv[1]
text = Path("CHANGELOG.md").read_text()
if not re.search(rf"^## \[{re.escape(ver)}\]", text, re.M):
    raise SystemExit(f"CHANGELOG.md missing section for {ver}")
PY

  git tag "$tag"
  git push origin "$tag"

  pkg="$(get_pkg_name)"
  echo "Pushed ${tag} for ${pkg}."
  echo "CI will publish to PyPI and create the GitHub Release."
}

case "${1:-}" in
  prepare) shift; cmd_prepare "${1:-}" ;;
  publish) cmd_publish ;;
  -h|--help|help|"") usage ;;
  *) usage; die "unknown command: $1" ;;
esac
