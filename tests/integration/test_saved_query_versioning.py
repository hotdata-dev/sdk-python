"""Scenario: saved_query_versioning.

Create a saved query, update its SQL twice, confirm list_saved_query_versions
reflects the edits, and confirm execute_saved_query runs the latest SQL.
"""

from __future__ import annotations

from hotdata.api.saved_queries_api import SavedQueriesApi
from hotdata.exceptions import ApiException
from hotdata.models.create_saved_query_request import CreateSavedQueryRequest
from hotdata.models.update_saved_query_request import UpdateSavedQueryRequest


def test_saved_query_versioning(
    saved_queries_api: SavedQueriesApi, sdkci_name
) -> None:
    name = sdkci_name("savedq-versioning")
    created_id: str | None = None

    try:
        created = saved_queries_api.create_saved_query(
            CreateSavedQueryRequest(
                name=name,
                sql="SELECT 1 AS x",
                description="sdkci versioning test",
            )
        )
        created_id = created.id
        assert created.latest_version == 1
        assert created.sql == "SELECT 1 AS x"

        v2 = saved_queries_api.update_saved_query(
            created.id, UpdateSavedQueryRequest(sql="SELECT 2 AS x")
        )
        assert v2.latest_version == 2
        assert v2.sql == "SELECT 2 AS x"

        v3 = saved_queries_api.update_saved_query(
            created.id, UpdateSavedQueryRequest(sql="SELECT 3 AS x")
        )
        assert v3.latest_version == 3
        assert v3.sql == "SELECT 3 AS x"

        versions = saved_queries_api.list_saved_query_versions(created.id)
        assert versions.saved_query_id == created.id
        assert versions.count >= 3
        version_numbers = {v.version for v in versions.versions}
        assert {1, 2, 3}.issubset(version_numbers), (
            f"expected versions 1,2,3 in {sorted(version_numbers)}"
        )

        executed = saved_queries_api.execute_saved_query(created.id)
        assert executed.row_count == 1
        assert executed.rows == [[3]]
    finally:
        if created_id is not None:
            try:
                saved_queries_api.delete_saved_query(created_id)
            except ApiException:
                pass
