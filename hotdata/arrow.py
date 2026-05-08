"""Arrow IPC helpers for ``GET /v1/results/{id}``.

The auto-generated :class:`hotdata.api.results_api.ResultsApi` understands the
``format=arrow`` query parameter but cannot decode the
``application/vnd.apache.arrow.stream`` response body — openapi-generator picks
the JSON content variant for status 200 and routes Arrow bytes through the
JSON deserializer, which raises ``Unsupported content type``.

This module wraps the generated client with a thin subclass that:

* sets ``Accept: application/vnd.apache.arrow.stream`` and ``?format=arrow``,
* uses the generator's ``*_without_preload_content`` plumbing to hold the
  underlying ``urllib3.HTTPResponse`` open as a byte stream,
* hands that stream to ``pyarrow.ipc.open_stream`` so callers get a
  :class:`pyarrow.Table` (or a :class:`pyarrow.RecordBatchStreamReader` for
  the streaming variant).

Install with ``pip install 'hotdata[arrow]'`` to pull in pyarrow.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Dict, Iterator, Optional

from hotdata.api.results_api import ResultsApi as _GeneratedResultsApi
from hotdata.models.results_format_query import ResultsFormatQuery

if TYPE_CHECKING:  # pragma: no cover - import-time only for type checkers
    import pyarrow as pa  # type: ignore[import-untyped]


ARROW_STREAM_MEDIA_TYPE = "application/vnd.apache.arrow.stream"


class ResultNotReadyError(Exception):
    """Raised when the result exists but is not yet ``ready``.

    The server replies with HTTP 202 while a result is ``pending`` or
    ``processing``. Poll :meth:`ResultsApi.get_result` until ``status='ready'``
    before fetching as Arrow.
    """

    def __init__(self, status: str, result_id: str) -> None:
        self.status = status
        self.result_id = result_id
        super().__init__(
            f"Result {result_id} is not ready (status={status!r}); "
            "poll get_result until status='ready' before fetching as Arrow."
        )


def _import_pyarrow() -> Any:
    try:
        import pyarrow.ipc as ipc  # type: ignore[import-untyped]
    except ImportError as exc:  # pragma: no cover - exercised via tests
        raise ImportError(
            "pyarrow is required to fetch results as Arrow. "
            "Install with: pip install 'hotdata[arrow]'"
        ) from exc
    return ipc


class ResultsApi(_GeneratedResultsApi):
    """Drop-in replacement for :class:`hotdata.api.results_api.ResultsApi`
    that adds Arrow IPC fetch helpers.

    All methods on the base class continue to work unchanged.
    """

    def get_result_arrow(
        self,
        id: str,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        _request_timeout: Any = None,
    ) -> "pa.Table":
        """Fetch a ready result as a :class:`pyarrow.Table`.

        Buffers the full Arrow IPC stream into memory before returning. Use
        :meth:`stream_result_arrow` for large results where you want to
        iterate batches without materializing the whole table.

        :param id: Result ID.
        :param offset: Rows to skip (default: 0).
        :param limit: Maximum rows to return (default: unbounded).
        :raises ResultNotReadyError: result is still pending or processing.
        :raises hotdata.exceptions.ApiException: for other HTTP errors
            (400 invalid params, 404 not found, 409 failed result).
        """
        ipc = _import_pyarrow()
        response = self._call_arrow(id=id, offset=offset, limit=limit,
                                    _request_timeout=_request_timeout)
        try:
            return ipc.open_stream(response).read_all()
        finally:
            response.release_conn()

    @contextmanager
    def stream_result_arrow(
        self,
        id: str,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        _request_timeout: Any = None,
    ) -> Iterator["pa.RecordBatchStreamReader"]:
        """Yield a :class:`pyarrow.RecordBatchStreamReader` for a ready result.

        The HTTP connection is released when the context exits. Iterate the
        reader to consume :class:`pyarrow.RecordBatch` messages, or call
        ``reader.read_all()`` for a full :class:`pyarrow.Table`.

        Example::

            with results.stream_result_arrow(result_id) as reader:
                for batch in reader:
                    process(batch)

        :raises ResultNotReadyError: result is still pending or processing.
        :raises hotdata.exceptions.ApiException: for other HTTP errors.
        """
        ipc = _import_pyarrow()
        response = self._call_arrow(id=id, offset=offset, limit=limit,
                                    _request_timeout=_request_timeout)
        try:
            yield ipc.open_stream(response)
        finally:
            response.release_conn()

    def _call_arrow(
        self,
        *,
        id: str,
        offset: Optional[int],
        limit: Optional[int],
        _request_timeout: Any,
    ) -> Any:
        # Build the request via the generator's private serialize helper so
        # path/query/auth handling stays in lockstep with the generated client.
        # Override only what we need: the Accept header and the format query.
        headers: Dict[str, Any] = {"Accept": ARROW_STREAM_MEDIA_TYPE}
        params = self._get_result_serialize(
            id=id,
            offset=offset,
            limit=limit,
            format=ResultsFormatQuery.ARROW,
            _request_auth=None,
            _content_type=None,
            _headers=headers,
            _host_index=0,
        )
        response_data = self.api_client.call_api(
            *params,
            _request_timeout=_request_timeout,
        )

        if response_data.status == 200:
            # Hand the raw urllib3.HTTPResponse to the caller. preload_content
            # was False on the way in, so the body has not been consumed.
            return response_data.response

        # Non-200: drain, deserialize as JSON, then raise. response_deserialize
        # raises ApiException for status >= 400 itself; only 202 falls through.
        try:
            response_data.read()
            body = self.api_client.response_deserialize(
                response_data=response_data,
                response_types_map={
                    "202": "GetResultResponse",
                    "400": "ApiErrorResponse",
                    "404": "ApiErrorResponse",
                    "409": "GetResultResponse",
                },
            ).data
        finally:
            response_data.response.release_conn()

        raise ResultNotReadyError(
            status=getattr(body, "status", "pending"),
            result_id=getattr(body, "result_id", id),
        )


__all__ = [
    "ARROW_STREAM_MEDIA_TYPE",
    "ResultNotReadyError",
    "ResultsApi",
]
