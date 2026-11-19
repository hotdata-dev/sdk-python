"""Unit tests for hotdata.query.QueryApi.query_arrow.

These stub the urllib3 transport with a queue of canned responses, so no server
is needed, and feed real Arrow IPC bytes through the SDK plumbing. They cover:

* the request: ``Accept`` asks for Arrow only, and ``dialect`` rides in the body,
* 200: the table plus the ``X-*`` response headers on the returned result,
* 429 retry, and errors (408) raised with their status,
* 202 (result too large to inline): follow to the Results API, the row guard,
  and the ``auto_follow=False`` opt-out,
* async submission is refused before any request is sent.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from unittest.mock import patch

import pytest

pa = pytest.importorskip("pyarrow")

from hotdata import ApiClient, Configuration, rest
from hotdata.arrow import ARROW_STREAM_MEDIA_TYPE
from hotdata.exceptions import ApiException
from hotdata.models.query_request import QueryRequest
from hotdata.models.rollup_usage import RollupUsage
from hotdata.query import (
    ArrowQueryResult,
    QueryApi,
    ResultNotInlineError,
    ResultTooLargeError,
    ResultUnavailableError,
    RetryPolicy,
    ServerOverloadedError,
)
from tests.test_arrow import _FakeUrllib3Response, _arrow_bytes

JSON = {"content-type": "application/json"}


def _table() -> Any:
    return pa.table({"n": pa.array([1, 2, 3], type=pa.int64())})


def _arrow_response(table: Any, **headers: str) -> _FakeUrllib3Response:
    return _FakeUrllib3Response(
        status=200,
        body=_arrow_bytes(table),
        headers={"content-type": ARROW_STREAM_MEDIA_TYPE, **headers},
    )


def _json_response(
    status: int, body: Dict[str, Any], **headers: str
) -> _FakeUrllib3Response:
    return _FakeUrllib3Response(
        status=status, body=json.dumps(body).encode(), headers={**JSON, **headers}
    )


def _too_large(result_id: Optional[str] = "rslt1") -> _FakeUrllib3Response:
    headers = {"X-Result-Id": result_id} if result_id else {}
    return _json_response(
        202,
        {
            "query_run_id": "qrun1",
            "status": "running",
            "status_url": "/v1/query-runs/qrun1",
            "reason": "the result is larger than an inline response can hold",
        },
        **headers,
    )


def _result_status(status: str) -> _FakeUrllib3Response:
    return _json_response(
        200 if status == "ready" else 202, {"result_id": "rslt1", "status": status}
    )


def _query_run(row_count: int) -> _FakeUrllib3Response:
    return _json_response(
        200,
        {
            "id": "qrun1",
            "created_at": "2026-01-01T00:00:00Z",
            "snapshot_id": "snap1",
            "sql_hash": "h",
            "sql_text": "SELECT 1",
            "status": "succeeded",
            "result_id": "rslt1",
            "row_count": row_count,
            "execution_time_ms": 42,
            "rollup": "used",
        },
    )


@pytest.fixture
def calls(monkeypatch: pytest.MonkeyPatch) -> List[Dict[str, Any]]:
    """Requests sent so far. Queue responses on ``calls.responses``."""

    class Calls(list):  # type: ignore[type-arg]
        responses: List[_FakeUrllib3Response] = []

    sent = Calls()
    sent.responses = []

    def fake_request(
        self: Any,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        body: Any = None,
        post_params: Any = None,
        _request_timeout: Any = None,
    ) -> rest.RESTResponse:
        sent.append(
            {"method": method, "url": url, "headers": dict(headers or {}), "body": body}
        )
        return rest.RESTResponse(sent.responses.pop(0))

    monkeypatch.setattr(rest.RESTClientObject, "request", fake_request)
    return sent


def _api(**kwargs: Any) -> QueryApi:
    config = Configuration(
        host="https://api.hotdata.test", api_key="test-key", workspace_id="ws_test"
    )
    return QueryApi(ApiClient(config), **kwargs)


REQ = QueryRequest(sql="SELECT n FROM t", dialect="clickhouse")


# --- 200 ----------------------------------------------------------------------


def test_returns_table_and_header_values(calls: Any) -> None:
    fake = _arrow_response(
        _table(),
        **{
            "X-Query-Run-Id": "qrun1",
            "X-Result-Id": "rslt1",
            "X-Total-Row-Count": "3",
            "X-Execution-Time-Ms": "7",
            "X-Query-Warning": "careful",
            "X-Rollup": "not_matched",
        },
    )
    calls.responses = [fake]

    out = _api().query_arrow(REQ, x_database_id="db1")

    assert isinstance(out, ArrowQueryResult)
    assert out.table.equals(_table())
    assert out.query_run_id == "qrun1"
    assert out.result_id == "rslt1"
    assert out.total_row_count == 3
    assert out.execution_time_ms == 7
    assert out.warning == "careful"
    assert out.rollup is RollupUsage.NOT_MATCHED
    assert out.followed is False
    assert fake.drain_conn_called and fake.release_conn_called

    # One round trip, asking for Arrow only, in the caller's dialect.
    assert len(calls) == 1
    call = calls[0]
    assert call["method"] == "POST"
    assert call["url"].endswith("/v1/query")
    assert call["headers"]["Accept"] == ARROW_STREAM_MEDIA_TYPE
    assert call["headers"]["Accept-Encoding"] == "identity"
    assert call["headers"]["X-Database-Id"] == "db1"
    assert call["body"]["dialect"] == "clickhouse"


def test_absent_headers_are_none(calls: Any) -> None:
    calls.responses = [_arrow_response(_table())]
    out = _api().query_arrow(REQ)
    assert out.rollup is None
    assert out.warning is None
    assert out.result_id is None


def test_unknown_rollup_value_is_ignored(calls: Any) -> None:
    calls.responses = [_arrow_response(_table(), **{"X-Rollup": "some_new_value"})]
    assert _api().query_arrow(REQ).rollup is None


# --- errors -------------------------------------------------------------------


def test_429_is_retried(calls: Any) -> None:
    overloaded = {"error": {"code": "OVERLOADED", "message": "busy"}}
    calls.responses = [
        _json_response(429, overloaded, **{"Retry-After": "2"}),
        _arrow_response(_table()),
    ]
    with patch("hotdata.query.time.sleep") as sleep, \
            patch("hotdata.query.random.random", return_value=0.0):
        out = _api().query_arrow(REQ)
    assert out.table.num_rows == 3
    assert len(calls) == 2
    sleep.assert_called_once_with(2.0)


def test_429_exhausted_raises_overloaded(calls: Any) -> None:
    overloaded = {"error": {"code": "OVERLOADED", "message": "busy"}}
    calls.responses = [_json_response(429, overloaded) for _ in range(2)]
    with patch("hotdata.query.time.sleep"), \
            patch("hotdata.query.random.random", return_value=0.0):
        with pytest.raises(ServerOverloadedError):
            _api(retry=RetryPolicy(max_retries=1)).query_arrow(REQ)


def test_timeout_raises_with_status(calls: Any) -> None:
    fake = _json_response(408, {"error": {"code": "TIMEOUT", "message": "too slow"}})
    calls.responses = [fake]
    with pytest.raises(ApiException) as ei:
        _api().query_arrow(REQ)
    assert ei.value.status == 408
    assert "too slow" in (ei.value.body or "")
    assert fake.release_conn_called


def test_async_request_is_refused(calls: Any) -> None:
    with pytest.raises(ValueError, match="async"):
        _api().query_arrow(QueryRequest(sql="SELECT 1", var_async=True))
    assert calls == []


# --- 202: too large to inline -------------------------------------------------


def test_too_large_follows_to_results_api(calls: Any) -> None:
    calls.responses = [
        _too_large(),
        _result_status("processing"),
        _result_status("ready"),
        _query_run(row_count=3),
        _arrow_response(_table()),
    ]
    with patch("hotdata.query.time.sleep"):
        out = _api().query_arrow(REQ, x_database_id="db1")

    assert out.table.equals(_table())
    assert out.followed is True
    assert out.query_run_id == "qrun1"
    assert out.result_id == "rslt1"
    assert out.total_row_count == 3
    assert out.execution_time_ms == 42
    assert out.rollup is RollupUsage.USED

    urls = [c["url"] for c in calls]
    assert "/v1/results/rslt1" in urls[1] and "limit=0" in urls[1]
    assert "/v1/query-runs/qrun1" in urls[3]
    assert "/v1/results/rslt1" in urls[4] and "format=arrow" in urls[4]
    # Every follow-up is scoped to the query's database.
    assert all(c["headers"]["X-Database-Id"] == "db1" for c in calls)


def test_follow_uses_body_database_id(calls: Any) -> None:
    calls.responses = [
        _too_large(),
        _result_status("ready"),
        _query_run(row_count=3),
        _arrow_response(_table()),
    ]
    _api().query_arrow(QueryRequest(sql="SELECT 1", database_id="db_body"))
    assert all(c["headers"]["X-Database-Id"] == "db_body" for c in calls[1:])


def test_follow_row_guard(calls: Any) -> None:
    calls.responses = [_too_large(), _result_status("ready"), _query_run(row_count=10)]
    with pytest.raises(ResultTooLargeError) as ei:
        _api().query_arrow(REQ, x_database_id="db1", max_auto_rows=5)
    assert ei.value.observed == 10
    assert len(calls) == 3  # the rows were never fetched


def test_too_large_without_auto_follow(calls: Any) -> None:
    calls.responses = [_too_large()]
    with pytest.raises(ResultNotInlineError) as ei:
        _api().query_arrow(REQ, x_database_id="db1", auto_follow=False)
    assert ei.value.result_id == "rslt1"
    assert ei.value.query_run_id == "qrun1"
    assert len(calls) == 1


def test_follow_row_guard_holds_when_run_lookup_fails(calls: Any) -> None:
    # No total from the run record: the guard must still stop the read.
    calls.responses = [
        _too_large(),
        _result_status("ready"),
        _json_response(500, {"error": {"code": "INTERNAL", "message": "boom"}}),
        _arrow_response(_table()),
    ]
    with pytest.raises(ResultTooLargeError) as ei:
        _api().query_arrow(REQ, x_database_id="db1", max_auto_rows=2)
    assert ei.value.observed == 3
    # The read asks for one row past the guard, not the whole result.
    assert "limit=3" in calls[3]["url"]


def test_follow_survives_failed_run_lookup(calls: Any) -> None:
    calls.responses = [
        _too_large(),
        _result_status("ready"),
        _json_response(500, {"error": {"code": "INTERNAL", "message": "boom"}}),
        _arrow_response(_table()),
    ]
    out = _api().query_arrow(REQ, x_database_id="db1")
    assert out.table.equals(_table())
    assert out.total_row_count == 3
    assert out.rollup is None


def test_too_large_without_result_id(calls: Any) -> None:
    calls.responses = [_too_large(result_id=None)]
    with pytest.raises(ResultUnavailableError) as ei:
        _api().query_arrow(REQ, x_database_id="db1", auto_follow=False)
    assert "qrun1" in str(ei.value)
    assert "preview" not in str(ei.value)


def test_follow_byte_guard(calls: Any) -> None:
    calls.responses = [
        _too_large(),
        _result_status("ready"),
        _query_run(row_count=3),
        _arrow_response(_table()),
    ]
    # Three int64 rows are 24 bytes: within the row guard, past this one.
    with pytest.raises(ResultTooLargeError) as ei:
        _api().query_arrow(REQ, x_database_id="db1", max_auto_bytes=8)
    assert ei.value.kind == "bytes"
    assert ei.value.observed == 24


def test_non_arrow_200_keeps_the_body(calls: Any) -> None:
    # A server that ignored Accept and answered in JSON: the query ran.
    fake = _json_response(200, {"query_run_id": "qrun1", "rows": [[1]]})
    calls.responses = [fake]
    with pytest.raises(ApiException) as ei:
        _api().query_arrow(REQ)
    assert ei.value.status == 200
    assert "qrun1" in (ei.value.body or "")
    assert "the query ran" in ei.value.reason
    assert len(calls) == 1  # not retried: a write must not run twice
    assert fake.release_conn_called
