#!/usr/bin/env python3
"""Re-apply the missing-workspace guard after OpenAPI regeneration.

The generated ``ApiClient.update_params_for_auth`` silently skips a security
scheme that has no configured value. For the ``WorkspaceId`` scheme that means
a ``Configuration`` built without ``workspace_id`` still sends the request,
and the server answers a workspace-scoped call with a bare 404.

The guard itself lives in ``hotdata/_workspace.py`` (generator-ignored); this
patch adds the import and one call at the top of ``update_params_for_auth`` so
the request fails client-side with :class:`hotdata.MissingWorkspaceError`,
which names the constructor argument and the environment variable.
Idempotent: a no-op if already applied.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

MARKER = "_workspace import ensure_workspace"


def patch_api_client() -> None:
    path = ROOT / "hotdata" / "api_client.py"
    src = path.read_text()
    if MARKER in src:
        return

    import_needle = "from hotdata.api_response import ApiResponse, T as ApiResponseT\n"
    import_replacement = (
        "from hotdata.api_response import ApiResponse, T as ApiResponseT\n"
        "from hotdata._workspace import ensure_workspace\n"
    )
    if import_needle not in src:
        sys.exit(f"Failed to patch {path}: api_response import anchor not found")
    src = src.replace(import_needle, import_replacement, 1)

    needle = (
        "        if not auth_settings:\n"
        "            return\n"
        "\n"
        "        if request_auth:\n"
        "            self._apply_auth_params(\n"
    )
    replacement = (
        "        if not auth_settings:\n"
        "            return\n"
        "\n"
        "        # Hand-applied (scripts/patch_workspace_guard.py): a workspace-scoped\n"
        "        # operation with no workspace id configured would otherwise go out\n"
        "        # without X-Workspace-Id and come back as a bare 404. Fail here with\n"
        "        # an error that says what is missing and how to supply it.\n"
        "        ensure_workspace(\n"
        "            self.configuration,\n"
        "            auth_settings,\n"
        "            headers,\n"
        "            resource_path,\n"
        "            method,\n"
        "            request_auth=request_auth,\n"
        "        )\n"
        "\n"
        "        if request_auth:\n"
        "            self._apply_auth_params(\n"
    )
    if needle not in src:
        sys.exit(f"Failed to patch {path}: update_params_for_auth anchor not found")
    src = src.replace(needle, replacement, 1)

    path.write_text(src)


def main() -> None:
    patch_api_client()


if __name__ == "__main__":
    main()
