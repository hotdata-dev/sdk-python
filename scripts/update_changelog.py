#!/usr/bin/env python3
"""Update CHANGELOG.md for a new release version."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def update_changelog_text(text: str, ver: str, date: str) -> str:
    if re.search(rf"^## \[{re.escape(ver)}\]", text, re.M):
        return text

    unreleased = re.search(r"^## \[Unreleased\]\s*\n(.*?)(?=^## \[|\Z)", text, re.M | re.S)
    if unreleased:
        body = unreleased.group(1).strip()
        if body:
            section = f"## [{ver}] - {date}\n\n{body}\n\n"
        else:
            section = (
                f"## [{ver}] - {date}\n\n"
                "### Changed\n\n"
                f"- Release {ver}\n\n"
            )
        return re.sub(
            r"^(## \[Unreleased\]\s*\n)(.*?)(?=^## \[|\Z)",
            lambda match: match.group(1) + "\n" + section,
            text,
            count=1,
            flags=re.M | re.S,
        )

    section = (
        f"## [Unreleased]\n\n"
        f"## [{ver}] - {date}\n\n"
        "### Changed\n\n"
        f"- Release {ver}\n\n"
    )
    first_heading = re.search(r"^## \[", text, re.M)
    if first_heading:
        pos = first_heading.start()
        return text[:pos] + section + text[pos:]
    return text.rstrip() + "\n\n" + section


def update_changelog_file(path: Path, ver: str, date: str) -> None:
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
        return

    path.write_text(update_changelog_text(path.read_text(), ver, date))


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: update_changelog.py VERSION YYYY-MM-DD")
    update_changelog_file(Path("CHANGELOG.md"), sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
