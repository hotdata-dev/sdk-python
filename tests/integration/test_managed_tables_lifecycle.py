"""Scenario: managed_tables_lifecycle.

The heaviest scenario — it ties databases, uploads, and managed tables together
against a fresh scratch database (whose default catalog is a managed catalog):

  1. declare a schema and a table on the database's default catalog connection,
  2. upload a small parquet file,
  3. load it into the table (load_managed_table) and verify the load response,
  4. purge_table_cache,
  5. delete the managed table.

Notes on managed-catalog semantics (both confirmed against prod):

  * There is no `refresh` step. `refresh` is rejected with a 400 on a managed
    catalog ("use the loads endpoint to update its data") — `load_managed_table`
    is itself the load.
  * There is no `get_table_profile` step. The profile is not populated within a
    usable window after a load, and no API call (refresh is rejected; there is
    no profile-build/scan endpoint) triggers it — so the load is verified via
    the `load_managed_table` response (row_count etc.), not a profile read.

The scratch_database fixture tears the database (and its catalog) down, so the
test touches no seeded data. pyarrow is a hard test dependency (see
test-requirements.txt) and is imported directly — a missing pyarrow must fail
loudly, never silently skip this scenario in CI.
"""

from __future__ import annotations

import io

import pyarrow as pa
import pyarrow.parquet as pq

from hotdata.api.connections_api import ConnectionsApi
from hotdata.api.databases_api import DatabasesApi
from hotdata.api.uploads_api import UploadsApi
from hotdata.models.add_managed_schema_request import AddManagedSchemaRequest
from hotdata.models.add_managed_table_request import AddManagedTableRequest
from hotdata.models.load_managed_table_request import LoadManagedTableRequest


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

    # purge_table_cache and delete_managed_table both return None on success.
    connections_api.purge_table_cache(connection_id, schema_name, table_name)
    connections_api.delete_managed_table(connection_id, schema_name, table_name)
