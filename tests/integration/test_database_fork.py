"""Scenario: database_fork.

Create a scratch source database, declare a schema and table on it, fork it into
an independent copy, and verify the fork is a distinct database that inherits the
source's catalog while the source is left intact. Deleting the fork must leave
the source untouched (independence).

Self-cleaning: both databases are created with a short `expires_at` and deleted
in a finally block, so a failed assertion never leaks a database into prod.
"""

from __future__ import annotations

from hotdata.api.databases_api import DatabasesApi
from hotdata.exceptions import ApiException
from hotdata.models.add_managed_schema_request import AddManagedSchemaRequest
from hotdata.models.add_managed_table_request import AddManagedTableRequest
from hotdata.models.create_database_request import CreateDatabaseRequest
from hotdata.models.fork_database_request import ForkDatabaseRequest


def test_database_fork(databases_api: DatabasesApi, sdkci_name) -> None:
    # Schema/table identifiers must be SQL identifiers (no dashes).
    schema_name = "sdkci_schema"
    table_name = "sdkci_table"
    source_id: str | None = None
    fork_id: str | None = None

    try:
        source = databases_api.create_database(
            CreateDatabaseRequest(name=sdkci_name("fork-src"), expires_at="2h")
        )
        source_id = source.id
        databases_api.add_database_schema(
            source_id, AddManagedSchemaRequest(name=schema_name)
        )
        databases_api.add_database_table(
            source_id, schema_name, AddManagedTableRequest(name=table_name)
        )

        # Fork with an explicit name + expiry so the copy is self-cleaning too.
        fork_name = sdkci_name("fork-dst")
        forked = databases_api.fork_database(
            source_id, ForkDatabaseRequest(name=fork_name, expires_at="2h")
        )
        fork_id = forked.id

        # The fork is a distinct database that inherits the source's catalog but
        # is backed by its own connection.
        assert fork_id
        assert fork_id != source_id
        assert forked.name == fork_name
        assert forked.default_catalog == source.default_catalog
        assert forked.default_connection_id != source.default_connection_id

        # Both the source and the fork are visible in the listing.
        ids = {d.id for d in databases_api.list_databases().databases}
        assert source_id in ids, "source database missing after fork"
        assert fork_id in ids, "fork not in list_databases"

        # Independence: deleting the fork leaves the source intact.
        databases_api.delete_database(fork_id)
        fork_id = None
        assert databases_api.get_database(source_id).id == source_id
    finally:
        for db_id in (fork_id, source_id):
            if db_id is not None:
                try:
                    databases_api.delete_database(db_id)
                except ApiException:
                    pass
