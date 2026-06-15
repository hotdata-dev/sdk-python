"""Unit tests for hotdata.query (#688).

These stub the generated API methods (QueryApi.query, ResultsApi.get_result,
QueryRunsApi.get_query_run) so no server is needed, and patch time.sleep /
random.random so retry/poll timing is deterministic and instant. They cover the
behaviors the bounded-memory query contract requires:

* 429 (OVERLOADED) retry: honor Retry-After, retry-then-succeed, exhaustion by
  max-retries and by deadline budget, and non-429 pass-through.
* Truncation auto-follow: materialize the full row set, fall back to the
  query-run total when total_row_count is null-while-persisting, the
  max_auto_rows guard, failed results, missing result_id, and the opt-out.
* Forward-compatible deserialization: unknown response fields are ignored.
"""

from __future__ import annotations

from contextlib import ExitStack
from types import SimpleNamespace
from typing import Any, List, Optional
from unittest.mock import patch

import pytest

from hotdata.api.query_api import QueryApi as _GeneratedQueryApi
from hotdata.api.query_runs_api import QueryRunsApi as _QueryRunsApi
from hotdata.api.results_api import ResultsApi as _ResultsApi
from hotdata.exceptions import ApiException
from hotdata.models.async_query_response import AsyncQueryResponse
from hotdata.models.get_result_response import GetResultResponse
from hotdata.models.query_request import QueryRequest
from hotdata.models.query_response import QueryResponse
from hotdata.query import (
    PollPolicy,
    QueryApi,
    ResultError,
    ResultFailedError,
    ResultIncompleteError,
    ResultTimeoutError,
    ResultTooLargeError,
    ResultUnavailableError,
    RetryPolicy,
    ServerOverloadedError,
)


REQ = QueryRequest(sql="SELECT 1 AS x")


def _api(**kwargs: Any) -> QueryApi:
    # api_client is a dummy: every HTTP method is patched at the class level, so
    # the instance's client is never actually exercised.
    return QueryApi(api_client=object(), **kwargs)


def _preview(
    *,
    truncated: bool = True,
    result_id: Optional[str] = "rslt1",
    total: Optional[int] = None,
    rows: Optional[List[List[Any]]] = None,
) -> QueryResponse:
    rows = rows if rows is not None else [[1]]
    return QueryResponse(
        columns=["x"],
        execution_time_ms=1,
        nullable=[False],
        preview_row_count=len(rows),
        query_run_id="qrun1",
        result_id=result_id,
        row_count=len(rows),
        rows=rows,
        total_row_count=total,
        truncated=truncated,
        warning=None,
    )


def _result(
    *,
    status: str = "ready",
    rows: Optional[List[List[Any]]] = None,
    error_message: Optional[str] = None,
) -> GetResultResponse:
    return GetResultResponse(
        result_id="rslt1", status=status, rows=rows, error_message=error_message
    )


def _too_many(retry_after: Optional[str] = None) -> ApiException:
    exc = ApiException(status=429, reason="Too Many Requests")
    exc.headers = {"Retry-After": retry_after} if retry_after is not None else {}
    return exc


# --- 429 retry ----------------------------------------------------------------


def test_passthrough_when_not_truncated() -> None:
    resp = _preview(truncated=False)
    with patch.object(_GeneratedQueryApi, "query", return_value=resp) as q, \
            patch.object(_ResultsApi, "get_result") as gr:
        out = _api().query(REQ, x_database_id="db1")
    assert out is resp
    assert q.call_count == 1
    gr.assert_not_called()  # no follow when not truncated


def test_non_429_error_propagates_unchanged() -> None:
    boom = ApiException(status=400, reason="Bad Request")
    with patch.object(_GeneratedQueryApi, "query", side_effect=boom), \
            patch("hotdata.query.time.sleep") as sleep:
        with pytest.raises(ApiException) as ei:
            _api().query(REQ)
    assert ei.value.status == 400
    assert not isinstance(ei.value, ServerOverloadedError)
    sleep.assert_not_called()


def test_429_retry_then_succeed() -> None:
    resp = _preview(truncated=False)
    side = [_too_many("1"), _too_many("1"), resp]
    with patch.object(_GeneratedQueryApi, "query", side_effect=side) as q, \
            patch("hotdata.query.time.sleep") as sleep, \
            patch("hotdata.query.random.random", return_value=0.0):
        out = _api(retry=RetryPolicy(max_retries=5)).query(REQ)
    assert out is resp
    assert q.call_count == 3
    assert sleep.call_count == 2


def test_429_honors_retry_after_header() -> None:
    resp = _preview(truncated=False)
    with patch.object(_GeneratedQueryApi, "query", side_effect=[_too_many("3"), resp]), \
            patch("hotdata.query.time.sleep") as sleep, \
            patch("hotdata.query.random.random", return_value=0.0):
        _api(retry=RetryPolicy()).query(REQ)
    # jitter fraction is 0.0 here, so the delay is exactly Retry-After.
    sleep.assert_called_once_with(3.0)


def test_429_exhausts_max_retries() -> None:
    with patch.object(_GeneratedQueryApi, "query", side_effect=_too_many("1")) as q, \
            patch("hotdata.query.time.sleep") as sleep, \
            patch("hotdata.query.random.random", return_value=0.0):
        with pytest.raises(ServerOverloadedError) as ei:
            _api(retry=RetryPolicy(max_retries=2, deadline_s=1000)).query(REQ)
    assert ei.value.status == 429
    assert ei.value.attempts == 3  # initial + 2 retries
    assert q.call_count == 3
    assert sleep.call_count == 2
    assert "retries exhausted" in str(ei.value)


def test_429_exhausts_deadline_budget() -> None:
    with patch.object(_GeneratedQueryApi, "query", side_effect=_too_many("1")) as q, \
            patch("hotdata.query.time.sleep") as sleep, \
            patch("hotdata.query.random.random", return_value=0.0):
        with pytest.raises(ServerOverloadedError) as ei:
            # A zero budget means the first computed delay already overruns it.
            _api(retry=RetryPolicy(max_retries=10, deadline_s=0.0)).query(REQ)
    assert ei.value.attempts == 1
    assert q.call_count == 1
    sleep.assert_not_called()
    assert "budget" in str(ei.value)


# --- truncation auto-follow ---------------------------------------------------


def _follow_patches(
    stack: ExitStack,
    *,
    query_response: QueryResponse,
    get_result_side_effect: Any,
    run_row_count: Optional[int] = None,
) -> None:
    stack.enter_context(
        patch.object(_GeneratedQueryApi, "query", return_value=query_response)
    )
    stack.enter_context(
        patch.object(_ResultsApi, "get_result", side_effect=get_result_side_effect)
    )
    stack.enter_context(
        patch.object(
            _QueryRunsApi,
            "get_query_run",
            return_value=SimpleNamespace(row_count=run_row_count),
        )
    )
    stack.enter_context(patch("hotdata.query.time.sleep"))


def test_autofollow_materializes_full_rows() -> None:
    # Inline preview has 1 row; the full result has 3. total_row_count is null
    # while persisting, so the total comes from the query-run record.
    preview = _preview(truncated=True, total=None, rows=[[1]])
    full = [[1], [2], [3]]

    def get_result(result_id, offset=None, limit=None, format=None, **kw):
        if format is None:  # poll: wait_for_result
            return _result(status="ready")
        # paginate: single page covers all rows
        return _result(status="ready", rows=full[offset:offset + limit])

    with ExitStack() as stack:
        _follow_patches(
            stack,
            query_response=preview,
            get_result_side_effect=get_result,
            run_row_count=3,
        )
        out = _api(poll=PollPolicy(page_size=1000)).query(REQ, x_database_id="db1")

    assert out.rows == full
    assert out.total_row_count == 3  # backfilled from the authoritative total
    assert out.truncated is True  # original server flag preserved


def test_autofollow_paginates_across_pages() -> None:
    preview = _preview(truncated=True, total=5, rows=[[0]])
    full = [[0], [1], [2], [3], [4]]

    def get_result(result_id, offset=None, limit=None, format=None, **kw):
        if format is None:
            return _result(status="ready")
        return _result(status="ready", rows=full[offset:offset + limit])

    with ExitStack() as stack:
        _follow_patches(
            stack, query_response=preview, get_result_side_effect=get_result
        )
        out = _api(poll=PollPolicy(page_size=2)).query(REQ)

    assert out.rows == full


def test_autofollow_polls_until_ready() -> None:
    preview = _preview(truncated=True, total=1, rows=[[1]])
    statuses = iter(["processing", "processing", "ready"])

    def get_result(result_id, offset=None, limit=None, format=None, **kw):
        if format is None:
            return _result(status=next(statuses))
        return _result(status="ready", rows=[[1]])

    with ExitStack() as stack:
        _follow_patches(
            stack, query_response=preview, get_result_side_effect=get_result
        )
        out = _api(poll=PollPolicy(base_backoff_s=0.01, deadline_s=100)).query(REQ)

    assert out.rows == [[1]]


def test_autofollow_disabled_returns_preview() -> None:
    preview = _preview(truncated=True, rows=[[1]])
    with patch.object(_GeneratedQueryApi, "query", return_value=preview), \
            patch.object(_ResultsApi, "get_result") as gr:
        out = _api().query(REQ, auto_follow=False)
    assert out is preview
    assert out.truncated is True
    gr.assert_not_called()


def test_autofollow_failed_result_raises() -> None:
    preview = _preview(truncated=True, total=3)

    def get_result(result_id, offset=None, limit=None, format=None, **kw):
        return _result(status="failed", error_message="planner exploded")

    with ExitStack() as stack:
        _follow_patches(
            stack, query_response=preview, get_result_side_effect=get_result
        )
        with pytest.raises(ResultFailedError) as ei:
            _api().query(REQ)
    assert ei.value.result_id == "rslt1"
    assert "planner exploded" in str(ei.value)


def test_autofollow_guard_rejects_oversized_result() -> None:
    preview = _preview(truncated=True, total=None)
    calls: List[Any] = []

    def get_result(result_id, offset=None, limit=None, format=None, **kw):
        calls.append(format)
        return _result(status="ready")  # only the poll should run

    with ExitStack() as stack:
        _follow_patches(
            stack,
            query_response=preview,
            get_result_side_effect=get_result,
            run_row_count=10,
        )
        with pytest.raises(ResultTooLargeError) as ei:
            _api(max_auto_rows=5).query(REQ)
    assert ei.value.kind == "rows"
    assert ei.value.observed == 10
    assert ei.value.limit == 5
    # Guard trips before any JSON page is fetched (only the readiness poll ran).
    assert all(fmt is None for fmt in calls)


def test_autofollow_unbounded_when_guard_disabled() -> None:
    preview = _preview(truncated=True, total=3)
    full = [[1], [2], [3]]

    def get_result(result_id, offset=None, limit=None, format=None, **kw):
        if format is None:
            return _result(status="ready")
        return _result(status="ready", rows=full[offset:offset + limit])

    with ExitStack() as stack:
        _follow_patches(
            stack, query_response=preview, get_result_side_effect=get_result
        )
        out = _api(max_auto_rows=None, poll=PollPolicy(page_size=1000)).query(REQ)
    assert out.rows == full


def test_autofollow_missing_result_id_raises() -> None:
    preview = _preview(truncated=True, result_id=None)
    preview.warning = "result persistence could not be initiated"
    with patch.object(_GeneratedQueryApi, "query", return_value=preview):
        with pytest.raises(ResultUnavailableError) as ei:
            _api().query(REQ)
    assert "result persistence could not be initiated" in str(ei.value)


def test_wait_for_result_times_out() -> None:
    preview = _preview(truncated=True, total=1)

    def get_result(result_id, offset=None, limit=None, format=None, **kw):
        return _result(status="processing")

    with ExitStack() as stack:
        _follow_patches(
            stack, query_response=preview, get_result_side_effect=get_result
        )
        with pytest.raises(ResultTimeoutError) as ei:
            _api(poll=PollPolicy(base_backoff_s=0.01, deadline_s=0.0)).query(REQ)
    assert ei.value.result_id == "rslt1"
    assert ei.value.status == "processing"


# --- forward-compatible deserialization --------------------------------------


def test_unknown_response_fields_are_ignored() -> None:
    # A future additive contract field must not break an older SDK build.
    payload = {
        "columns": ["x"],
        "execution_time_ms": 1,
        "nullable": [False],
        "preview_row_count": 1,
        "query_run_id": "qrun1",
        "row_count": 1,
        "rows": [[1]],
        "truncated": False,
        "some_future_field": {"nested": [1, 2, 3]},
    }
    resp = QueryResponse.from_dict(payload)
    assert resp is not None
    assert resp.truncated is False
    assert resp.preview_row_count == 1
    assert not hasattr(resp, "some_future_field")


# --- bug fixes ----------------------------------------------------------------


def test_async_response_passes_through_untouched() -> None:
    # var_async=True returns AsyncQueryResponse (no .truncated). The enhanced
    # query() must return it untouched, not AttributeError on response.truncated.
    async_resp = AsyncQueryResponse(
        query_run_id="qrun1", status="running", status_url="/v1/query-runs/qrun1"
    )
    with patch.object(_GeneratedQueryApi, "query", return_value=async_resp) as q, \
            patch.object(_ResultsApi, "get_result") as gr:
        out = _api().query(REQ, x_database_id="db1")
    assert out is async_resp
    assert q.call_count == 1
    gr.assert_not_called()  # no auto-follow attempted on an async submission


def test_retry_after_not_capped_by_max_backoff() -> None:
    # Retry-After larger than max_backoff_s must be honored, not shrunk to the
    # cap — the server told us exactly how long to wait.
    resp = _preview(truncated=False)
    with patch.object(_GeneratedQueryApi, "query", side_effect=[_too_many("60"), resp]), \
            patch("hotdata.query.time.sleep") as sleep, \
            patch("hotdata.query.random.random", return_value=0.0):
        _api(retry=RetryPolicy(max_backoff_s=30.0, deadline_s=1000)).query(REQ)
    sleep.assert_called_once_with(60.0)


def test_pagination_raises_on_premature_empty_page() -> None:
    # total is known (5) but the server returns no more rows after 2 — must
    # raise rather than silently returning a partial result.
    preview = _preview(truncated=True, total=5, rows=[[0]])
    partial = [[0], [1]]

    def get_result(result_id, offset=None, limit=None, format=None, **kw):
        if format is None:
            return _result(status="ready")
        return _result(status="ready", rows=partial[offset:offset + limit])

    with ExitStack() as stack:
        _follow_patches(
            stack, query_response=preview, get_result_side_effect=get_result
        )
        with pytest.raises(ResultIncompleteError) as ei:
            _api(poll=PollPolicy(page_size=2)).query(REQ)
    assert ei.value.expected == 5
    assert ei.value.fetched == 2


# --- byte guard + exception hierarchy ----------------------------------------


def test_byte_guard_trips_before_row_guard() -> None:
    # Few rows, but each is wide — the byte guard must catch it even though the
    # row count stays well under max_auto_rows.
    preview = _preview(truncated=True, total=3, rows=[["x"]])
    wide = [["A" * 10_000], ["B" * 10_000], ["C" * 10_000]]

    def get_result(result_id, offset=None, limit=None, format=None, **kw):
        if format is None:
            return _result(status="ready")
        return _result(status="ready", rows=wide[offset:offset + limit])

    with ExitStack() as stack:
        _follow_patches(
            stack, query_response=preview, get_result_side_effect=get_result
        )
        with pytest.raises(ResultTooLargeError) as ei:
            _api(
                max_auto_rows=1_000_000,
                max_auto_bytes=15_000,
                poll=PollPolicy(page_size=1),
            ).query(REQ)
    assert ei.value.kind == "bytes"
    assert ei.value.limit == 15_000


def test_result_errors_share_a_base() -> None:
    # Callers should be able to catch every lifecycle error with one except.
    preview = _preview(truncated=True, total=3)

    def get_result(result_id, offset=None, limit=None, format=None, **kw):
        return _result(status="failed", error_message="boom")

    with ExitStack() as stack:
        _follow_patches(
            stack, query_response=preview, get_result_side_effect=get_result
        )
        with pytest.raises(ResultError):  # ResultFailedError is a ResultError
            _api().query(REQ)
    assert issubclass(ResultFailedError, ResultError)
    assert issubclass(ResultTimeoutError, ResultError)
    assert issubclass(ResultTooLargeError, ResultError)
    assert issubclass(ResultUnavailableError, ResultError)
    assert issubclass(ResultIncompleteError, ResultError)


# --- default export ----------------------------------------------------------


def test_enhanced_clients_are_the_default_export() -> None:
    # `from hotdata import QueryApi` / `ResultsApi` must resolve to the enhanced
    # clients (retry + auto-follow / Arrow), not the bare generated ones, so the
    # obvious happy path gets the safe behavior. (Patched by patch_query_exports.)
    import hotdata
    from hotdata.arrow import ResultsApi as ArrowResultsApi
    from hotdata.query import QueryApi as EnhancedQueryApi

    assert hotdata.QueryApi is EnhancedQueryApi
    assert hotdata.ResultsApi is ArrowResultsApi
    # The raw generated classes stay reachable on their explicit path.
    assert _GeneratedQueryApi is not EnhancedQueryApi
