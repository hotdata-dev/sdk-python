"""Scenario: results_arrow.

Submit a small query, poll until the result is ready, then fetch the result
as a pyarrow.Table via hotdata.arrow.ResultsApi.get_result_arrow. Verifies
that Arrow IPC content negotiation works end-to-end and that the streaming
variant yields the same data.

Skipped if pyarrow is not installed (the helper requires the ``arrow`` extra).
"""

from __future__ import annotations

import time

import pytest

pa = pytest.importorskip("pyarrow")

from hotdata.api.query_api import QueryApi
from hotdata.api.query_runs_api import QueryRunsApi
from hotdata.arrow import ResultsApi
from hotdata.models.query_request import QueryRequest


TERMINAL_STATUSES = {"succeeded", "failed", "cancelled"}
POLL_TIMEOUT_S = 60.0
POLL_INTERVAL_S = 1.0


@pytest.fixture
def query_api(api_client) -> QueryApi:
    return QueryApi(api_client)


@pytest.fixture
def query_runs_api(api_client) -> QueryRunsApi:
    return QueryRunsApi(api_client)


@pytest.fixture
def results_api(api_client) -> ResultsApi:
    return ResultsApi(api_client)


def test_results_arrow(
    query_api: QueryApi,
    query_runs_api: QueryRunsApi,
    results_api: ResultsApi,
) -> None:
    submitted = query_api.query(
        QueryRequest(
            var_async=True,
            async_after_ms=1000,
            sql="SELECT 1 AS x, 'hello' AS msg UNION ALL SELECT 2, 'world'",
        )
    )
    query_run_id = submitted.query_run_id
    assert query_run_id

    deadline = time.monotonic() + POLL_TIMEOUT_S
    run = None
    while time.monotonic() < deadline:
        run = query_runs_api.get_query_run(query_run_id)
        if run.status in TERMINAL_STATUSES:
            break
        time.sleep(POLL_INTERVAL_S)
    assert run is not None
    assert run.status == "succeeded", (
        f"expected succeeded, got {run.status}: {run.error_message}"
    )
    assert run.result_id, "succeeded run must expose a result_id"
    result_id = run.result_id

    # Wait for ready before fetching as Arrow — get_result_arrow raises
    # ResultNotReadyError on 202.
    deadline = time.monotonic() + POLL_TIMEOUT_S
    while time.monotonic() < deadline:
        result = results_api.get_result(result_id)
        if result.status == "ready":
            break
        time.sleep(POLL_INTERVAL_S)
    else:
        pytest.fail(f"result {result_id} never became ready")

    # Buffered: returns a full pyarrow.Table.
    table = results_api.get_result_arrow(result_id)
    assert isinstance(table, pa.Table)
    assert table.num_rows == 2
    assert set(table.column_names) == {"x", "msg"}
    assert table.column("x").to_pylist() == [1, 2]
    assert table.column("msg").to_pylist() == ["hello", "world"]

    # Streaming: same data via RecordBatchStreamReader.
    with results_api.stream_result_arrow(result_id) as reader:
        streamed = pa.Table.from_batches(list(reader), schema=reader.schema)
    assert streamed.equals(table)

    # Pagination forwards correctly.
    sliced = results_api.get_result_arrow(result_id, offset=1, limit=1)
    assert sliced.num_rows == 1
    assert sliced.column("x").to_pylist() == [2]
