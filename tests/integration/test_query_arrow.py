"""Scenario: query_arrow.

Run a small query with hotdata.query.QueryApi.query_arrow and check that the
rows come back as a pyarrow.Table in one call, with the run and result ids the
server sends as response headers, and that a non-default dialect is accepted.

pyarrow is a hard test dependency (see test-requirements.txt), so this imports
it directly rather than via importorskip.
"""

from __future__ import annotations

import pyarrow as pa
import pytest

from hotdata.models.query_request import QueryRequest
from hotdata.query import QueryApi


@pytest.fixture
def query_api(api_client) -> QueryApi:
    return QueryApi(api_client)


def test_query_arrow(query_api: QueryApi, database_id: str) -> None:
    out = query_api.query_arrow(
        QueryRequest(
            sql=(
                "SELECT x, msg FROM ("
                "SELECT 1 AS x, 'hello' AS msg "
                "UNION ALL SELECT 2, 'world'"
                ") ORDER BY x"
            ),
        ),
        x_database_id=database_id,
    )
    assert isinstance(out.table, pa.Table)
    assert out.table.column("x").to_pylist() == [1, 2]
    assert out.table.column("msg").to_pylist() == ["hello", "world"]
    assert out.query_run_id
    assert out.total_row_count == 2
    assert out.followed is False
    # No table read, so no rollup outcome to report.
    assert out.rollup is None


def test_query_arrow_clickhouse_dialect(query_api: QueryApi, database_id: str) -> None:
    out = query_api.query_arrow(
        QueryRequest(sql="SELECT toString(1) AS s", dialect="clickhouse"),
        x_database_id=database_id,
    )
    assert out.table.column("s").to_pylist() == ["1"]
