"""Scenario: saved_queries_read.

Create a saved query, confirm it appears in list_saved_queries, fetch it by id
with get_saved_query, then delete it. Read-focused companion to
saved_query_versioning (which exercises the version history).
"""

from __future__ import annotations

from hotdata.api.saved_queries_api import SavedQueriesApi
from hotdata.exceptions import ApiException
from hotdata.models.create_saved_query_request import CreateSavedQueryRequest


def test_saved_queries_read(saved_queries_api: SavedQueriesApi, sdkci_name) -> None:
    name = sdkci_name("savedq-read")
    sql = "SELECT 42 AS answer"
    created_id: str | None = None

    try:
        created = saved_queries_api.create_saved_query(
            CreateSavedQueryRequest(name=name, sql=sql, description="sdkci read test")
        )
        created_id = created.id
        assert created.id
        assert created.name == name

        listing = saved_queries_api.list_saved_queries()
        match = next((q for q in listing.queries if q.id == created_id), None)
        assert match is not None, f"created saved query {created_id} not in list"
        assert match.name == name

        got = saved_queries_api.get_saved_query(created_id)
        assert got.id == created_id
        assert got.name == name
        assert got.sql == sql

        saved_queries_api.delete_saved_query(created_id)
        created_id = None
    finally:
        if created_id is not None:
            try:
                saved_queries_api.delete_saved_query(created_id)
            except ApiException:
                pass
