#!/usr/bin/env python3
"""Print the Keep a Changelog section for a release version."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def extract(changelog: str, version: str) -> str:
    pattern = rf"^## \[{re.escape(version)}\].*$"
    match = re.search(pattern, changelog, re.M)
    if not match:
        raise SystemExit(f"no changelog section for {version}")

    start = match.start()
    rest = changelog[match.end() :]
    next_heading = re.search(r"^## \[", rest, re.M)
    end = match.end() + (next_heading.start() if next_heading else len(rest))
    section = changelog[start:end].strip()
    title, _, body = section.partition("\n")
    return body.strip() or f"Release {version}."


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: extract-changelog.py VERSION")

    version = sys.argv[1]
    changelog = Path("CHANGELOG.md").read_text()
    print(extract(changelog, version))


if __name__ == "__main__":
    main()
