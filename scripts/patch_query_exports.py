#!/usr/bin/env python3
"""Re-apply enhanced default client exports after OpenAPI regeneration.

The generated ``hotdata/__init__.py`` binds the top-level ``QueryApi``,
``ResultsApi`` and ``UploadsApi`` to the raw generated classes. We want ``from
hotdata import QueryApi`` / ``ResultsApi`` / ``UploadsApi`` to resolve to the
hand-written enhanced clients instead — ``hotdata.query.QueryApi`` (429 retry +
truncation auto-follow), ``hotdata.arrow.ResultsApi`` (Arrow IPC fetch) and
``hotdata.uploads.UploadsApi`` (transparent presigned direct-to-storage upload)
— so the obvious happy path gets the safe, ergonomic behavior rather than the
bare client. The raw generated classes stay importable from ``hotdata.api.*``.

``hotdata/__init__.py`` is regenerated, so this override is appended (after all
generated imports, so every name it references is defined) and re-applied by
regenerate.yml on each regen. Idempotent: a no-op if already present.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

MARKER = "patch_query_exports.py"

OVERRIDE = (
    "\n\n"
    "# --- hand-applied: prefer the enhanced clients over the generated ones\n"
    "# (re-applied by scripts/patch_query_exports.py after regeneration).\n"
    "# hotdata.query.QueryApi adds 429 retry + truncation auto-follow;\n"
    "# hotdata.arrow.ResultsApi adds Arrow IPC result fetch;\n"
    "# hotdata.uploads.UploadsApi adds transparent presigned direct-to-storage\n"
    "# uploads. The raw generated classes remain importable from hotdata.api.*.\n"
    "from hotdata.query import QueryApi as QueryApi  # noqa: E402,F811\n"
    "from hotdata.arrow import ResultsApi as ResultsApi  # noqa: E402,F811\n"
    "from hotdata.uploads import UploadsApi as UploadsApi  # noqa: E402,F811\n"
    "# The upload error hierarchy + option/helper types, so `from hotdata import\n"
    "# UploadError` / `StorageError` / ... works (they otherwise live only under\n"
    "# hotdata.uploads and are invisible to autocomplete on `hotdata.`).\n"
    "from hotdata.uploads import (  # noqa: E402,F401\n"
    "    UploadError as UploadError,\n"
    "    SessionCreateError as SessionCreateError,\n"
    "    MalformedSessionError as MalformedSessionError,\n"
    "    SizeLimitError as SizeLimitError,\n"
    "    StorageError as StorageError,\n"
    "    StorageTransportError as StorageTransportError,\n"
    "    MissingETagError as MissingETagError,\n"
    "    MintPartError as MintPartError,\n"
    "    FinalizeError as FinalizeError,\n"
    "    UploadCancelledError as UploadCancelledError,\n"
    "    UploadOptions as UploadOptions,\n"
    "    UploadProgress as UploadProgress,\n"
    "    UploadSource as UploadSource,\n"
    "    tqdm_progress as tqdm_progress,\n"
    ")\n"
    "__all__ += [  # noqa: F405\n"
    '    "UploadError",\n'
    '    "SessionCreateError",\n'
    '    "MalformedSessionError",\n'
    '    "SizeLimitError",\n'
    '    "StorageError",\n'
    '    "StorageTransportError",\n'
    '    "MissingETagError",\n'
    '    "MintPartError",\n'
    '    "FinalizeError",\n'
    '    "UploadCancelledError",\n'
    '    "UploadOptions",\n'
    '    "UploadProgress",\n'
    '    "UploadSource",\n'
    '    "tqdm_progress",\n'
    "]\n"
)


def patch_init() -> None:
    path = ROOT / "hotdata" / "__init__.py"
    src = path.read_text()
    if MARKER in src:
        return
    if "import QueryApi as QueryApi" not in src:
        sys.exit(f"Failed to patch {path}: generated QueryApi export not found")
    path.write_text(src.rstrip("\n") + "\n" + OVERRIDE)


def main() -> None:
    patch_init()


if __name__ == "__main__":
    main()
