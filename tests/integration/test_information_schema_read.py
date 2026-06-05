"""Scenario: information_schema_read.

Read-only: information_schema returns the catalog/schema/table metadata visible
to the workspace. Verify the seeded connection's tables surface when filtered by
connection id, including column definitions.
"""

from __future__ import annotations

from hotdata.api.information_schema_api import InformationSchemaApi


def test_information_schema_read(
    information_schema_api: InformationSchemaApi, connection_id: str
) -> None:
    resp = information_schema_api.information_schema(
        connection_id=connection_id, include_columns=True
    )
    # Response is well-formed: count matches the page, has_more drives paging.
    assert isinstance(resp.tables, list)
    assert resp.count == len(resp.tables)
    assert isinstance(resp.has_more, bool)

    assert resp.tables, (
        f"seeded connection {connection_id} exposed no tables in information_schema"
    )
    for table in resp.tables:
        assert table.table
        assert table.var_schema
        # include_columns=True must populate column definitions.
        assert table.columns is not None
