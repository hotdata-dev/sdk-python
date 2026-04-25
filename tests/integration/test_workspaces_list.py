"""Scenario: workspaces_list.

List workspaces and confirm the seeded HOTDATA_TEST_WORKSPACE_ID is present.
Read-only — never creates or deletes workspaces against prod.
"""

from __future__ import annotations

from hotdata.api.workspaces_api import WorkspacesApi


def test_workspaces_list(workspaces_api: WorkspacesApi, workspace_id: str) -> None:
    response = workspaces_api.list_workspaces()
    assert response.ok
    found = [w for w in response.workspaces if w.public_id == workspace_id]
    assert found, (
        f"expected seeded workspace {workspace_id} in list, got "
        f"{[w.public_id for w in response.workspaces]}"
    )
