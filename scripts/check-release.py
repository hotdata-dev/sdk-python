#!/usr/bin/env python3
"""Fail CI when pyproject.toml version changes without a matching CHANGELOG entry."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def git_show(path: str, ref: str) -> str:
    try:
        return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)
    except subprocess.CalledProcessError:
        return ""


def read_version(text: str) -> str:
    match = re.search(r'(?m)^version = "([^"]+)"', text)
    if not match:
        raise SystemExit("could not read version from pyproject.toml")
    return match.group(1)


def has_changelog_section(version: str) -> bool:
    changelog = Path("CHANGELOG.md")
    if not changelog.exists():
        return False
    return bool(re.search(rf"^## \[{re.escape(version)}\]", changelog.read_text(), re.M))


def main() -> None:
    base = "origin/main"
    for candidate in ("origin/main", "origin/master"):
        if subprocess.call(["git", "rev-parse", "--verify", candidate], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            base = candidate
            break

    current = Path("pyproject.toml").read_text()
    previous = git_show("pyproject.toml", base)
    if not previous:
        print("skip: no base pyproject.toml to compare")
        return

    old_version = read_version(previous)
    new_version = read_version(current)
    if old_version == new_version:
        print(f"version unchanged ({new_version})")
        return

    if not has_changelog_section(new_version):
        raise SystemExit(
            f"pyproject.toml version bumped to {new_version} but CHANGELOG.md "
            f"has no '## [{new_version}]' section"
        )

    print(f"release metadata ok for {new_version}")


if __name__ == "__main__":
    main()
