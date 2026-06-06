"""Scenario: managed_tables_lifecycle.

The heaviest scenario — it ties databases, uploads, and managed tables together
against a fresh scratch database (whose default catalog is a managed catalog):

  1. declare a schema and a table on the database's default catalog connection,
  2. upload a small parquet file,
  3. load it into the table (load_managed_table),
  4. poll get_table_profile until the load syncs,
  5. purge_table_cache,
  6. delete the managed table.

Note on managed-catalog semantics: there is no `refresh` step. `refresh` is
rejected with a 400 on a managed catalog ("use the loads endpoint to update its
data") — `load_managed_table` is itself the load. The profile is populated
asynchronously after the load, so step 4 polls get_table_profile (a 404 means
"not synced yet") rather than reading it once.

The scratch_database fixture tears the database (and its catalog) down, so the
test touches no seeded data. pyarrow is a hard test dependency (see
test-requirements.txt) and is imported directly — a missing pyarrow must fail
loudly, never silently skip this scenario in CI.
"""

from __future__ import annotations

import io
import time

import pyarrow as pa
import pyarrow.parquet as pq

from hotdata.api.connections_api import ConnectionsApi
from hotdata.api.databases_api import DatabasesApi
from hotdata.api.uploads_api import UploadsApi
from hotdata.exceptions import ApiException
from hotdata.models.add_managed_schema_request import AddManagedSchemaRequest
from hotdata.models.add_managed_table_request import AddManagedTableRequest
from hotdata.models.load_managed_table_request import LoadManagedTableRequest


PROFILE_SYNC_TIMEOUT_S = 60.0
PROFILE_POLL_INTERVAL_S = 2.0


def _parquet_bytes() -> bytes:
    table = pa.table({"x": [1, 2, 3], "msg": ["a", "b", "c"]})
    buf = io.BytesIO()
    pq.write_table(table, buf)
    return buf.getvalue()


def test_managed_tables_lifecycle(
    databases_api: DatabasesApi,
    connections_api: ConnectionsApi,
    uploads_api: UploadsApi,
    scratch_database: str,
) -> None:
    # The database's auto-provisioned default catalog is a managed catalog,
    # addressed through its default_connection_id.
    connection_id = databases_api.get_database(scratch_database).default_connection_id
    schema_name = "sdkci_mt"
    table_name = "sdkci_loaded"

    connections_api.add_managed_schema(
        connection_id, AddManagedSchemaRequest(name=schema_name)
    )
    connections_api.add_managed_table(
        connection_id, schema_name, AddManagedTableRequest(name=table_name)
    )

    upload = uploads_api.upload_file(
        body=_parquet_bytes(), _content_type="application/parquet"
    )
    assert upload.id

    loaded = connections_api.load_managed_table(
        connection_id,
        schema_name,
        table_name,
        LoadManagedTableRequest(mode="replace", upload_id=upload.id),
    )
    assert loaded.schema_name == schema_name
    assert loaded.table_name == table_name
    assert loaded.row_count == 3

    # The profile syncs asynchronously after the load — get_table_profile 404s
    # ("Table may not be synced yet") until it lands. Poll instead of reading
    # once. There is no manual trigger to force this: refresh is rejected on a
    # managed catalog, and load_managed_table is the load.
    deadline = time.monotonic() + PROFILE_SYNC_TIMEOUT_S
    profile = None
    while time.monotonic() < deadline:
        try:
            profile = connections_api.get_table_profile(
                connection_id, schema_name, table_name
            )
            break
        except ApiException as exc:
            if exc.status != 404:
                raise
            time.sleep(PROFILE_POLL_INTERVAL_S)
    assert profile is not None, "table profile never synced after load"
    assert profile.var_schema == schema_name
    assert profile.table == table_name
    assert profile.row_count == 3

    # purge_table_cache and delete_managed_table both return None on success.
    connections_api.purge_table_cache(connection_id, schema_name, table_name)
    connections_api.delete_managed_table(connection_id, schema_name, table_name)
