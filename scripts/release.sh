#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

die() { echo "error: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "$1 is required"; }

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
  python3 - <<'PY'
import tomllib
from pathlib import Path
print(tomllib.loads(Path("pyproject.toml").read_text())["project"]["version"])
PY
}

get_pkg_name() {
  python3 - <<'PY'
import tomllib
from pathlib import Path
print(tomllib.loads(Path("pyproject.toml").read_text())["project"]["name"])
PY
}

set_version() {
  local ver="$1"
  python3 - "$ver" <<'PY'
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
  python3 - "$kind" "$current" <<'PY'
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
  python3 - "$ver" "$date" <<'PY'
import re, sys
from pathlib import Path

ver, date = sys.argv[1], sys.argv[2]
path = Path("CHANGELOG.md")

if not path.exists():
    path.write_text(
        "# Changelog\n\n"
        "All notable changes to this project will be documented in this file.\n\n"
        "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),\n"
        "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n"
        f"## [Unreleased]\n\n"
        f"## [{ver}] - {date}\n\n"
        "### Changed\n\n"
        f"- Release {ver}\n"
    )
    raise SystemExit(0)

text = path.read_text()
if re.search(rf"^## \[{re.escape(ver)}\]", text, re.M):
    raise SystemExit(0)

unreleased = re.search(r"^## \[Unreleased\]\s*\n(.*?)(?=^## \[|\Z)", text, re.M | re.S)
if unreleased and unreleased.group(1).strip():
    body = unreleased.group(1).rstrip() + "\n"
    text = re.sub(r"^## \[Unreleased\]\s*\n.*?(?=^## \[|\Z)", "", text, count=1, flags=re.M | re.S)
    insert = f"## [Unreleased]\n\n## [{ver}] - {date}\n{body}\n"
    if text.startswith("# Changelog"):
        parts = text.split("\n\n", 2)
        if len(parts) >= 2:
            text = parts[0] + "\n\n" + parts[1] + "\n\n" + insert + (parts[2] if len(parts) > 2 else "")
        else:
            text = insert + text
    else:
        text = insert + text
else:
    insert = (
        f"## [Unreleased]\n\n"
        f"## [{ver}] - {date}\n\n"
        "### Changed\n\n"
        f"- Release {ver}\n\n"
    )
    if "## [Unreleased]" in text:
        text = text.replace("## [Unreleased]", insert.strip() + "\n\n## [Unreleased]", 1)
    else:
        text = re.sub(r"(^# Changelog.*?)(\n\n|\Z)", r"\1\n\n" + insert, text, count=1, flags=re.S)

path.write_text(text)
PY
}

cmd_prepare() {
  local bump="${1:-}"
  [[ -n "$bump" ]] || { usage; die "missing bump kind or explicit version"; }
  need gh
  need python3
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

  branch="release/v${new}"
  git checkout -b "$branch"
  git add pyproject.toml CHANGELOG.md
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
  need python3
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
  python3 - "$ver" <<'PY'
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
