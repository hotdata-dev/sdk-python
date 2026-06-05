"""Scenario: databases_lifecycle.

Create a database (a metadata-only grouping that auto-provisions a default
catalog), read it back, confirm it appears in list_databases, declare a schema
and a table on its default catalog, then delete it and verify it's gone.

Self-cleaning: the database is created with a short `expires_at` and deleted in
a finally block, so a failed assertion never leaks a database into prod.
"""

from __future__ import annotations

import pytest

from hotdata.api.databases_api import DatabasesApi
from hotdata.exceptions import ApiException
from hotdata.models.add_managed_schema_request import AddManagedSchemaRequest
from hotdata.models.add_managed_table_request import AddManagedTableRequest
from hotdata.models.create_database_request import CreateDatabaseRequest


def test_databases_lifecycle(databases_api: DatabasesApi, sdkci_name) -> None:
    name = sdkci_name("databases-lifecycle")
    # Schema/table identifiers must be SQL identifiers (no dashes).
    schema_name = "sdkci_schema"
    table_name = "sdkci_table"
    db_id: str | None = None

    try:
        created = databases_api.create_database(
            CreateDatabaseRequest(name=name, expires_at="2h")
        )
        db_id = created.id
        assert created.id
        assert created.name == name
        assert created.default_connection_id, (
            "create_database must expose the auto-provisioned default catalog connection"
        )

        detail = databases_api.get_database(db_id)
        assert detail.id == db_id
        assert detail.name == name
        assert detail.default_connection_id == created.default_connection_id

        listing = databases_api.list_databases()
        assert any(d.id == db_id for d in listing.databases), (
            f"created database {db_id} not in list_databases"
        )

        schema_resp = databases_api.add_database_schema(
            db_id, AddManagedSchemaRequest(name=schema_name)
        )
        assert schema_resp.var_schema == schema_name

        table_resp = databases_api.add_database_table(
            db_id, schema_name, AddManagedTableRequest(name=table_name)
        )
        assert table_resp.var_schema == schema_name
        assert table_resp.table == table_name

        databases_api.delete_database(db_id)
        db_id = None

        with pytest.raises(ApiException) as excinfo:
            databases_api.get_database(created.id)
        assert excinfo.value.status == 404
    finally:
        if db_id is not None:
            try:
                databases_api.delete_database(db_id)
            except ApiException:
                pass
