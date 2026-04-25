"""Scenario: query_async_polling.

Submit a query asynchronously, poll get_query_run until terminal status, fetch
results, and verify list_query_runs / list_results surface the run.
"""

from __future__ import annotations

import time

import pytest

from hotdata.api.query_api import QueryApi
from hotdata.api.query_runs_api import QueryRunsApi
from hotdata.api.results_api import ResultsApi
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


def test_query_async_polling(
    query_api: QueryApi,
    query_runs_api: QueryRunsApi,
    results_api: ResultsApi,
) -> None:
    # async=True with a small async_after_ms forces the run to come back as
    # AsyncQueryResponse rather than synchronous. The QueryResponse / async
    # response variants are union-shaped on the client; we treat anything with
    # query_run_id as the start of the polling loop.
    submitted = query_api.query(
        QueryRequest(var_async=True, async_after_ms=1000, sql="SELECT 1 AS x")
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
    assert run.status in TERMINAL_STATUSES, (
        f"query {query_run_id} did not reach terminal status within "
        f"{POLL_TIMEOUT_S}s; last status was {run.status if run else 'None'}"
    )
    assert run.status == "succeeded", (
        f"expected succeeded, got {run.status}: {run.error_message}"
    )
    assert run.row_count == 1

    runs_listing = query_runs_api.list_query_runs(limit=50)
    assert any(r.id == query_run_id for r in runs_listing.query_runs), (
        f"query run {query_run_id} not surfaced by list_query_runs"
    )

    if run.result_id:
        result = results_api.get_result(run.result_id)
        assert result.result_id == run.result_id
        assert result.status in {"ready", "processing"}
        if result.status == "ready":
            assert result.row_count == 1
            assert result.rows == [[1]]

        # ResultInfo (list_results) exposes the id as `id`, not `result_id` —
        # only GetResultResponse uses `result_id`.
        results_listing = results_api.list_results(limit=50)
        assert any(r.id == run.result_id for r in results_listing.results), (
            f"result {run.result_id} not surfaced by list_results"
        )
