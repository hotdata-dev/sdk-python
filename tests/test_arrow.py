"""Unit tests for hotdata.arrow.

These tests stub out the underlying urllib3 transport so they don't require a
running server. They build real Arrow IPC byte streams with pyarrow and feed
them through the SDK plumbing to verify:

* the Arrow Table round-trips schema and values,
* the request carries ``Accept: application/vnd.apache.arrow.stream`` and
  ``?format=arrow``,
* offset / limit are forwarded as query params,
* non-200 responses raise the right exceptions,
* the streaming variant yields RecordBatches and releases the connection.
"""

from __future__ import annotations

import io
import json
from typing import Any, Dict, List, Optional, Tuple
from unittest.mock import patch

import pytest

pa = pytest.importorskip("pyarrow")
pa_ipc = pytest.importorskip("pyarrow.ipc")

from hotdata import ApiClient, Configuration
from hotdata.arrow import (
    ARROW_STREAM_MEDIA_TYPE,
    ResultNotReadyError,
    ResultsApi,
)
from hotdata.exceptions import ApiException


def _arrow_bytes(table: Any) -> bytes:
    sink = io.BytesIO()
    with pa_ipc.new_stream(sink, table.schema) as writer:
        writer.write_table(table)
    return sink.getvalue()


class _FakeUrllib3Response(io.RawIOBase):
    """Minimal stand-in for urllib3.HTTPResponse.

    pyarrow.ipc.open_stream wants a real file-like object (it checks
    ``closed`` and ``readable()``); the SDK's RESTResponse needs ``status``,
    ``reason``, ``data``, and ``headers``. release_conn is recorded.
    """

    def __init__(self, status: int, body: bytes, headers: Dict[str, str]):
        super().__init__()
        self.status = status
        self.reason = "OK" if 200 <= status < 300 else "Error"
        self._body = body
        self._buf = io.BytesIO(body)
        self.headers = headers
        self.release_conn_called = False

    @property
    def data(self) -> bytes:
        # urllib3.HTTPResponse.data preloads the body. SDK RESTResponse.read()
        # reads from this attribute.
        return self._body

    def read(self, amt: Optional[int] = -1) -> bytes:
        if amt is None or amt < 0:
            return self._buf.read()
        return self._buf.read(amt)

    def readable(self) -> bool:
        return True

    def release_conn(self) -> None:
        self.release_conn_called = True


def _install_fake_response(
    monkeypatch: pytest.MonkeyPatch,
    response: _FakeUrllib3Response,
    captured: List[Dict[str, Any]],
) -> None:
    """Replace RESTClientObject.request with a stub that records the call."""

    from hotdata import rest

    def fake_request(
        self: Any,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        body: Any = None,
        post_params: Any = None,
        _request_timeout: Any = None,
    ) -> rest.RESTResponse:
        captured.append(
            {
                "method": method,
                "url": url,
                "headers": dict(headers or {}),
            }
        )
        return rest.RESTResponse(response)

    monkeypatch.setattr(rest.RESTClientObject, "request", fake_request)


def _make_results_api() -> Tuple[ResultsApi, ApiClient]:
    config = Configuration(
        host="https://api.hotdata.test",
        api_key="test-key",
        workspace_id="ws_test",
    )
    client = ApiClient(config)
    return ResultsApi(client), client


def _sample_table() -> Any:
    return pa.table(
        {
            "id": pa.array([1, 2, 3], type=pa.int64()),
            "label": pa.array(["a", "b", "c"], type=pa.string()),
        }
    )


# --- Happy path -----------------------------------------------------------


def test_get_result_arrow_returns_table(monkeypatch: pytest.MonkeyPatch) -> None:
    table = _sample_table()
    fake = _FakeUrllib3Response(
        status=200,
        body=_arrow_bytes(table),
        headers={"content-type": ARROW_STREAM_MEDIA_TYPE},
    )
    captured: List[Dict[str, Any]] = []
    _install_fake_response(monkeypatch, fake, captured)

    results, _ = _make_results_api()
    got = results.get_result_arrow("res_123")

    assert got.equals(table)
    assert fake.release_conn_called

    # Single request was made.
    assert len(captured) == 1
    call = captured[0]
    assert call["method"] == "GET"
    # Path templating preserved.
    assert "/v1/results/res_123" in call["url"]
    # format=arrow query param sent.
    assert "format=arrow" in call["url"]
    # Accept header overrides the JSON default.
    assert call["headers"]["Accept"] == ARROW_STREAM_MEDIA_TYPE


def test_get_result_arrow_forwards_offset_and_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = _FakeUrllib3Response(
        status=200,
        body=_arrow_bytes(_sample_table()),
        headers={"content-type": ARROW_STREAM_MEDIA_TYPE},
    )
    captured: List[Dict[str, Any]] = []
    _install_fake_response(monkeypatch, fake, captured)

    results, _ = _make_results_api()
    results.get_result_arrow("res_123", offset=10, limit=100)

    url = captured[0]["url"]
    assert "offset=10" in url
    assert "limit=100" in url


def test_stream_result_arrow_yields_reader(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    table = _sample_table()
    fake = _FakeUrllib3Response(
        status=200,
        body=_arrow_bytes(table),
        headers={"content-type": ARROW_STREAM_MEDIA_TYPE},
    )
    _install_fake_response(monkeypatch, fake, [])

    results, _ = _make_results_api()
    with results.stream_result_arrow("res_123") as reader:
        batches = list(reader)
        assert batches, "expected at least one RecordBatch"
        roundtrip = pa.Table.from_batches(batches, schema=reader.schema)
        assert roundtrip.equals(table)

    # Connection is released after the context exits.
    assert fake.release_conn_called


# --- Non-200 paths --------------------------------------------------------


def test_get_result_arrow_raises_when_not_ready(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = json.dumps(
        {
            "result_id": "res_pending",
            "status": "processing",
            "row_count": 0,
        }
    ).encode()
    fake = _FakeUrllib3Response(
        status=202,
        body=body,
        headers={"content-type": "application/json"},
    )
    _install_fake_response(monkeypatch, fake, [])

    results, _ = _make_results_api()
    with pytest.raises(ResultNotReadyError) as ei:
        results.get_result_arrow("res_pending")

    assert ei.value.status == "processing"
    assert ei.value.result_id == "res_pending"
    assert fake.release_conn_called


def test_get_result_arrow_raises_api_exception_on_404(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = json.dumps({"error": {"message": "not found", "code": "not_found"}}).encode()
    fake = _FakeUrllib3Response(
        status=404,
        body=body,
        headers={"content-type": "application/json"},
    )
    _install_fake_response(monkeypatch, fake, [])

    results, _ = _make_results_api()
    with pytest.raises(ApiException) as ei:
        results.get_result_arrow("res_missing")

    assert ei.value.status == 404
    assert fake.release_conn_called


def test_get_result_arrow_raises_api_exception_on_409_failed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = json.dumps(
        {
            "result_id": "res_failed",
            "status": "failed",
            "error_message": "boom",
            "row_count": 0,
        }
    ).encode()
    fake = _FakeUrllib3Response(
        status=409,
        body=body,
        headers={"content-type": "application/json"},
    )
    _install_fake_response(monkeypatch, fake, [])

    results, _ = _make_results_api()
    with pytest.raises(ApiException) as ei:
        results.get_result_arrow("res_failed")

    assert ei.value.status == 409


# --- Missing pyarrow ------------------------------------------------------


def test_helpful_error_when_pyarrow_missing() -> None:
    """``_import_pyarrow`` re-raises ImportError with an install hint."""
    from hotdata import arrow as arrow_module

    with patch.dict("sys.modules", {"pyarrow.ipc": None}):
        # patch.dict with None value forces ImportError on `import pyarrow.ipc`.
        with pytest.raises(ImportError) as ei:
            arrow_module._import_pyarrow()
        assert "hotdata[arrow]" in str(ei.value)
