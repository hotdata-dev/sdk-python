import importlib.util
from pathlib import Path


def _update_changelog_text(text: str, ver: str, date: str) -> str:
    path = Path(__file__).resolve().parents[1] / "scripts" / "update_changelog.py"
    spec = importlib.util.spec_from_file_location("update_changelog", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.update_changelog_text(text, ver, date)


HEADER = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-05-19

### Added

- Initial feature.
"""


def test_empty_unreleased_inserts_version_without_duplicate_heading():
    result = _update_changelog_text(HEADER, "0.1.2", "2026-05-20")
    assert result.count("## [Unreleased]") == 1
    assert "## [0.1.2] - 2026-05-20" in result
    assert "The format is based on [Keep a Changelog]" in result.split("## [0.1.2]")[0]
    assert result.index("## [0.1.2]") < result.index("## [0.1.1]")
    assert "## [Unreleased]\n\n## [0.1.2]" in result
    assert "\n\n\n" not in result


def test_populated_unreleased_moves_notes_into_new_section():
    text = HEADER.replace(
        "## [Unreleased]\n\n",
        "## [Unreleased]\n\n### Added\n\n- New widget.\n\n",
    )
    result = _update_changelog_text(text, "0.1.2", "2026-05-20")
    assert result.count("## [Unreleased]") == 1
    assert "- New widget." in result
    assert result.index("- New widget.") < result.index("## [0.1.1]")
    assert "The format is based on [Keep a Changelog]" in result.split("## [0.1.2]")[0]
    assert "## [Unreleased]\n\n## [0.1.2]" in result
    assert "\n\n\n" not in result
