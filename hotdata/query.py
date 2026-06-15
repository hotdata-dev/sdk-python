"""High-level helpers for ``POST /v1/query`` (#640 / #688).

The auto-generated :class:`hotdata.api.query_api.QueryApi` speaks the raw
contract; this module wraps it with a thin subclass that absorbs two behaviors
the bounded-memory query contract introduces, transparently:

* **429 admission-shedding retry.** Under concurrent load the server may shed a
  query with HTTP 429 + ``Retry-After`` (error code ``OVERLOADED``; PR #686
  turns the admission cap on by default). :meth:`QueryApi.query` retries
  automatically — honoring ``Retry-After`` when present, otherwise bounded
  exponential backoff with jitter — under an overall deadline budget. When the
  budget or retry count is exhausted it raises :class:`ServerOverloadedError`,
  which is distinct from a generic 503 so callers can branch on overload.

* **Transparent truncation auto-follow.** A large result comes back with
  ``truncated=True`` and only a bounded preview in ``rows``; the full result is
  persisted out-of-band under ``result_id`` (#640). :meth:`QueryApi.query`
  polls that result to ``ready`` and materializes the full row set into the
  returned :class:`~hotdata.models.query_response.QueryResponse`. A configurable
  ``max_auto_rows`` guard means an unbounded result is never silently pulled
  into client memory — past the guard it raises :class:`ResultTooLargeError`,
  pointing callers at the streaming Arrow API (:mod:`hotdata.arrow`).

Use this ``QueryApi`` in place of :class:`hotdata.api.query_api.QueryApi`; every
other method on the base class works unchanged. Auto-follow and retry are both
configurable per-instance (constructor) and per-call (keyword arguments), and
auto-follow can be turned off entirely to get just the preview.
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from hotdata.api.query_api import QueryApi as _GeneratedQueryApi
from hotdata.api.query_runs_api import QueryRunsApi as _QueryRunsApi
from hotdata.api.results_api import ResultsApi as _ResultsApi
from hotdata.exceptions import ApiException
from hotdata.models.query_request import QueryRequest
from hotdata.models.query_response import QueryResponse
from hotdata.models.results_format_query import ResultsFormatQuery

# HTTP 429: too many concurrent queries (admission shedding). The server tags
# the body with error code OVERLOADED; we key retry off the status code since
# 429 is unambiguous and the body is not always parsed before we see it.
_HTTP_TOO_MANY_REQUESTS = 429
OVERLOADED_ERROR_CODE = "OVERLOADED"

# Default ceiling on rows auto-materialized into memory when following a
# truncated result. Mirrors the server's own bounded-memory concern: large
# enough that ordinary results follow transparently, small enough that an
# accidental ``SELECT *`` over a huge table fails loudly instead of OOMing the
# client. Pass ``max_auto_rows=None`` to opt into unbounded materialization.
DEFAULT_MAX_AUTO_ROWS = 1_000_000

# Sentinel so a per-call ``max_auto_rows=None`` (opt into unbounded) is
# distinguishable from "not passed, use the instance default".
_UNSET: Any = object()


@dataclass(frozen=True)
class RetryPolicy:
    """Controls 429 (``OVERLOADED``) retry behavior.

    :param max_retries: Maximum retry attempts after the initial request.
    :param base_backoff_s: Base delay for exponential backoff when the server
        sends no ``Retry-After`` header.
    :param max_backoff_s: Cap on any single backoff delay.
    :param deadline_s: Overall budget across all attempts; once exceeded (or a
        computed delay would push past it) retries stop.
    :param jitter: Fraction of the base delay added as random jitter, to avoid
        a thundering herd of retries hitting the freed admission slot at once.
    """

    max_retries: int = 5
    base_backoff_s: float = 0.5
    max_backoff_s: float = 30.0
    deadline_s: float = 120.0
    jitter: float = 0.5


@dataclass(frozen=True)
class PollPolicy:
    """Controls result-lifecycle polling and full-result pagination.

    :param base_backoff_s: Initial poll interval; doubles each poll up to
        ``max_backoff_s``.
    :param max_backoff_s: Cap on the poll interval.
    :param deadline_s: Overall budget for a result to reach ``ready``.
    :param page_size: Rows fetched per page when paginating the full result.
    """

    base_backoff_s: float = 0.5
    max_backoff_s: float = 5.0
    deadline_s: float = 120.0
    page_size: int = 50_000


class ServerOverloadedError(ApiException):
    """Raised when ``POST /v1/query`` is shed with HTTP 429 (``OVERLOADED``,
    #686) and the retry budget or attempt count is exhausted.

    Distinct from a generic 503 / ``RESOURCE_EXHAUSTED`` so callers can treat
    transient admission shedding differently from a hard resource error. The
    ``attempts`` attribute records how many requests were made.
    """

    def __init__(self, *, attempts: int, reason: str, last_exc: ApiException) -> None:
        self.attempts = attempts
        super().__init__(status=_HTTP_TOO_MANY_REQUESTS, reason=reason)
        self.body = getattr(last_exc, "body", None)
        self.headers = getattr(last_exc, "headers", None)


class ResultFailedError(Exception):
    """Raised when a followed result reaches terminal status ``failed``."""

    def __init__(self, *, result_id: str, error_message: Optional[str]) -> None:
        self.result_id = result_id
        self.error_message = error_message
        super().__init__(
            f"Result {result_id} failed"
            + (f": {error_message}" if error_message else "")
        )


class ResultTimeoutError(Exception):
    """Raised when a result does not reach ``ready`` within the poll deadline."""

    def __init__(self, *, result_id: str, status: str, deadline_s: float) -> None:
        self.result_id = result_id
        self.status = status
        self.deadline_s = deadline_s
        super().__init__(
            f"Result {result_id} did not become ready within {deadline_s}s "
            f"(last status={status!r})."
        )


class ResultTooLargeError(Exception):
    """Raised when auto-follow would materialize more rows than the guard
    allows. Fetch the result incrementally via :mod:`hotdata.arrow` (Arrow
    streaming) or raise ``max_auto_rows`` if you truly want it all in memory.
    """

    def __init__(self, *, result_id: str, total: Optional[int], limit: int) -> None:
        self.result_id = result_id
        self.total = total
        self.limit = limit
        total_desc = f"{total} rows" if total is not None else "an unknown number of rows"
        super().__init__(
            f"Result {result_id} has {total_desc}, exceeding the auto-materialize "
            f"limit of {limit}. Stream it with hotdata.arrow.ResultsApi, or pass a "
            f"higher (or None) max_auto_rows to override."
        )


class ResultUnavailableError(Exception):
    """Raised when a result is truncated but no ``result_id`` is available to
    follow (persistence failed — see the response ``warning`` field).
    """

    def __init__(self, *, warning: Optional[str]) -> None:
        self.warning = warning
        super().__init__(
            "Query result is truncated but no result_id is available to fetch "
            "the full result"
            + (f": {warning}" if warning else "")
            + ". Re-run with auto_follow=False to use the preview."
        )


def _parse_retry_after(headers: Any) -> Optional[float]:
    """Return the ``Retry-After`` delay in seconds, or ``None``.

    Honors the integer-seconds form (the server sends ``Retry-After: 1``). The
    HTTP-date form is not emitted by this API, so it is intentionally ignored
    rather than parsed.
    """
    if not headers:
        return None
    # urllib3's HTTPHeaderDict is case-insensitive; a plain dict from a
    # hand-built exception may not be, so try the canonical casing too.
    value = None
    getter = getattr(headers, "get", None)
    if callable(getter):
        value = headers.get("Retry-After") or headers.get("retry-after")
    if value is None:
        return None
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        return None
    return seconds if seconds >= 0 else None


class QueryApi(_GeneratedQueryApi):
    """Drop-in replacement for :class:`hotdata.api.query_api.QueryApi` that adds
    429 retry and transparent truncation auto-follow. All base-class methods
    work unchanged.
    """

    def __init__(
        self,
        api_client: Any = None,
        *,
        retry: Optional[RetryPolicy] = None,
        poll: Optional[PollPolicy] = None,
        auto_follow: bool = True,
        max_auto_rows: Optional[int] = DEFAULT_MAX_AUTO_ROWS,
    ) -> None:
        super().__init__(api_client)
        self.retry = retry or RetryPolicy()
        self.poll = poll or PollPolicy()
        self.auto_follow = auto_follow
        self.max_auto_rows = max_auto_rows

    def query(
        self,
        query_request: QueryRequest,
        x_database_id: Optional[str] = None,
        _request_timeout: Union[None, float, Tuple[float, float]] = None,
        _request_auth: Optional[Dict[str, Any]] = None,
        _content_type: Optional[str] = None,
        _headers: Optional[Dict[str, Any]] = None,
        _host_index: int = 0,
        *,
        auto_follow: Optional[bool] = None,
        max_auto_rows: Any = _UNSET,
    ) -> QueryResponse:
        """Execute a query, retrying on 429 and auto-following truncation.

        Behaves like the generated :meth:`query` but:

        * retries HTTP 429 (``OVERLOADED``) per the instance :class:`RetryPolicy`;
        * when the response is ``truncated`` and ``auto_follow`` is on, polls the
          out-of-band result to ``ready`` and replaces ``rows`` with the full
          result set (``truncated`` / ``total_row_count`` are left intact so the
          caller can still tell it *was* truncated).

        :param auto_follow: Override the instance default for this call. ``False``
            returns the bounded preview unchanged.
        :param max_auto_rows: Override the instance row guard for this call.
            ``None`` opts into unbounded materialization.
        :raises ServerOverloadedError: 429 retries exhausted.
        :raises ResultFailedError: the followed result failed.
        :raises ResultTimeoutError: the result never became ready.
        :raises ResultTooLargeError: the full result exceeds the row guard.
        :raises ResultUnavailableError: truncated with no ``result_id`` to follow.
        """
        follow = self.auto_follow if auto_follow is None else auto_follow
        guard = self.max_auto_rows if max_auto_rows is _UNSET else max_auto_rows

        response = self._query_with_retry(
            query_request,
            x_database_id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        if not follow or not response.truncated:
            return response
        return self._materialize_full(response, guard)

    def wait_for_result(
        self,
        result_id: str,
        *,
        results_api: Optional[_ResultsApi] = None,
    ) -> Any:
        """Poll ``GET /v1/results/{id}`` until the result is ``ready``.

        Returns the ready :class:`~hotdata.models.get_result_response.GetResultResponse`.
        Shared by auto-follow and available for direct use.

        :raises ResultFailedError: status reached ``failed``.
        :raises ResultTimeoutError: ``ready`` not reached within the poll deadline.
        """
        api = results_api or _ResultsApi(self.api_client)
        policy = self.poll
        deadline = time.monotonic() + policy.deadline_s
        delay = policy.base_backoff_s
        last_status = "pending"
        while True:
            result = api.get_result(result_id)
            last_status = result.status
            if last_status == "ready":
                return result
            if last_status == "failed":
                raise ResultFailedError(
                    result_id=result_id, error_message=result.error_message
                )
            # pending / processing: back off and poll again, within budget.
            if time.monotonic() + delay > deadline:
                raise ResultTimeoutError(
                    result_id=result_id,
                    status=last_status,
                    deadline_s=policy.deadline_s,
                )
            time.sleep(delay)
            delay = min(delay * 2, policy.max_backoff_s)

    # -- internals ---------------------------------------------------------

    def _query_with_retry(self, *args: Any, **kwargs: Any) -> QueryResponse:
        policy = self.retry
        deadline = time.monotonic() + policy.deadline_s
        attempts = 0
        while True:
            attempts += 1
            try:
                return super().query(*args, **kwargs)
            except ApiException as exc:
                if exc.status != _HTTP_TOO_MANY_REQUESTS:
                    raise
                if attempts > policy.max_retries:
                    raise ServerOverloadedError(
                        attempts=attempts,
                        reason=(
                            f"server overloaded: {policy.max_retries} retries "
                            "exhausted (HTTP 429 OVERLOADED)"
                        ),
                        last_exc=exc,
                    ) from exc
                delay = self._backoff_delay(exc, attempts)
                if time.monotonic() + delay > deadline:
                    raise ServerOverloadedError(
                        attempts=attempts,
                        reason=(
                            f"server overloaded: retry budget of {policy.deadline_s}s "
                            "exhausted (HTTP 429 OVERLOADED)"
                        ),
                        last_exc=exc,
                    ) from exc
                time.sleep(delay)

    def _backoff_delay(self, exc: ApiException, attempt: int) -> float:
        """Delay before the next retry: honor ``Retry-After`` when present,
        else exponential backoff. Jitter is always added on top so retries do
        not synchronize on the freed admission slot.
        """
        policy = self.retry
        retry_after = _parse_retry_after(getattr(exc, "headers", None))
        if retry_after is not None:
            base = retry_after
        else:
            base = policy.base_backoff_s * (2 ** (attempt - 1))
        jitter = base * policy.jitter * random.random()
        return min(base + jitter, policy.max_backoff_s)

    def _materialize_full(
        self, preview: QueryResponse, max_auto_rows: Optional[int]
    ) -> QueryResponse:
        if preview.result_id is None:
            raise ResultUnavailableError(warning=preview.warning)

        results_api = _ResultsApi(self.api_client)
        self.wait_for_result(preview.result_id, results_api=results_api)

        total = self._authoritative_total(preview)
        if max_auto_rows is not None and total is not None and total > max_auto_rows:
            raise ResultTooLargeError(
                result_id=preview.result_id, total=total, limit=max_auto_rows
            )

        rows = self._fetch_all_rows(
            preview.result_id, total, max_auto_rows, results_api
        )
        # Replace the bounded preview with the full row set. truncated /
        # total_row_count stay as the server reported them so the caller can
        # still see that the inline body had been truncated.
        preview.rows = rows
        if preview.total_row_count is None and total is not None:
            preview.total_row_count = total
        return preview

    def _authoritative_total(self, preview: QueryResponse) -> Optional[int]:
        """The grand total row count. ``total_row_count`` is null while a
        truncated result is still persisting, so fall back to the query-run
        record, which carries the authoritative count once the run succeeds.
        """
        if preview.total_row_count is not None:
            return preview.total_row_count
        try:
            run = _QueryRunsApi(self.api_client).get_query_run(preview.query_run_id)
        except ApiException:
            return None
        return run.row_count

    def _fetch_all_rows(
        self,
        result_id: str,
        total: Optional[int],
        max_auto_rows: Optional[int],
        results_api: _ResultsApi,
    ) -> List[List[Any]]:
        page_size = self.poll.page_size
        rows: List[List[Any]] = []
        offset = 0
        while True:
            page = results_api.get_result(
                result_id,
                offset=offset,
                limit=page_size,
                format=ResultsFormatQuery.JSON,
            )
            batch = page.rows or []
            rows.extend(batch)
            # Enforce the guard during pagination too, in case the total was
            # unknown up front (total_row_count null, query-run lookup failed).
            if max_auto_rows is not None and len(rows) > max_auto_rows:
                raise ResultTooLargeError(
                    result_id=result_id, total=total, limit=max_auto_rows
                )
            offset += len(batch)
            if total is not None and offset >= total:
                break
            if len(batch) < page_size:
                break
        return rows


__all__ = [
    "DEFAULT_MAX_AUTO_ROWS",
    "OVERLOADED_ERROR_CODE",
    "PollPolicy",
    "QueryApi",
    "ResultFailedError",
    "ResultTimeoutError",
    "ResultTooLargeError",
    "ResultUnavailableError",
    "RetryPolicy",
    "ServerOverloadedError",
]
