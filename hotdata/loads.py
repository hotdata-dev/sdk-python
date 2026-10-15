"""Retry of table loads that collide with another load on the same table.

The server serialises loads per table. While one load holds a table, a second
``POST .../loads`` against the same table is rejected with HTTP 409, error code
``RESOURCE_LOCKED`` and a ``Retry-After`` header::

    HTTP/1.1 409 Conflict
    Retry-After: 5

    {"error": {"code": "RESOURCE_LOCKED",
               "message": "another operation is already running for ...; retry shortly"}}

The generated clients raise :class:`~hotdata.exceptions.ConflictException` and
leave the retry to the caller. This module wraps the load methods so that case
is retried automatically, mirroring the 429 handling in :mod:`hotdata.query`:

* only a 409 whose error **code** is ``RESOURCE_LOCKED`` is retried. Every
  other 409 (``CONFLICT``, ``IDEMPOTENCY_KEY_CONFLICT``, a load against an
  upload that is already being loaded, ...) is raised unchanged — those are
  not transient;
* ``Retry-After`` is honoured when present, otherwise bounded exponential
  backoff; jitter is always added so waiting writers do not stampede the
  freed lock;
* the whole wait is capped by :attr:`LoadRetryPolicy.deadline_s` (60s by
  default). Past it, or past ``max_retries``, :class:`TableLockedError` is
  raised with the last server response attached.

Two generated classes carry a ``/loads`` operation and get a drop-in subclass
here: :class:`DatabasesApi` (``load_database_table``) and
:class:`ConnectionsApi` (``load_managed_table``). Only the plain methods
retry; the generated ``*_with_http_info`` / ``*_without_preload_content``
variants are left untouched. ``from hotdata import DatabasesApi`` /
``ConnectionsApi`` resolves to these classes; the raw generated ones remain
importable from ``hotdata.api.*``.
"""

from __future__ import annotations

import json
import logging
import random
import time
from dataclasses import dataclass
from typing import Any, Callable, Optional, TypeVar

from hotdata.api.connections_api import ConnectionsApi as _GeneratedConnectionsApi
from hotdata.api.databases_api import DatabasesApi as _GeneratedDatabasesApi
from hotdata.exceptions import ApiException
from hotdata.query import _parse_retry_after

_HTTP_CONFLICT = 409
RESOURCE_LOCKED_ERROR_CODE = "RESOURCE_LOCKED"

_log = logging.getLogger("hotdata.loads")

_T = TypeVar("_T")


@dataclass(frozen=True)
class LoadRetryPolicy:
    """Controls 409 (``RESOURCE_LOCKED``) retry of table loads.

    :param max_retries: Maximum retry attempts after the initial request.
    :param base_backoff_s: Base delay for exponential backoff when the server
        sends no ``Retry-After`` header.
    :param max_backoff_s: Cap on any single computed backoff delay. A
        ``Retry-After`` larger than the cap is still honoured.
    :param deadline_s: Overall budget across all attempts; once exceeded (or a
        computed delay would push past it) retries stop.
    :param jitter: Fraction of the delay added as random jitter, so several
        writers waiting on the same table do not retry in lockstep.
    """

    max_retries: int = 10
    base_backoff_s: float = 1.0
    max_backoff_s: float = 15.0
    deadline_s: float = 60.0
    jitter: float = 0.5


class TableLockedError(ApiException):
    """Raised when a load keeps getting HTTP 409 ``RESOURCE_LOCKED`` (another
    load holds the table) and the retry budget or attempt count is exhausted.

    ``attempts`` records how many requests were made; ``body`` / ``headers`` /
    ``data`` carry the last server response.
    """

    def __init__(self, *, attempts: int, reason: str, last_exc: ApiException) -> None:
        self.attempts = attempts
        super().__init__(status=_HTTP_CONFLICT, reason=reason)
        self.body = getattr(last_exc, "body", None)
        self.data = getattr(last_exc, "data", None)
        self.headers = getattr(last_exc, "headers", None)


def error_code(exc: ApiException) -> Optional[str]:
    """The ``error.code`` of an API error response, or ``None``.

    Prefers the deserialised ``exc.data`` (an ``ApiErrorResponse`` when the
    operation declares one for that status) and falls back to parsing the raw
    JSON body, so the check does not depend on which the generated client
    populated.
    """
    data = getattr(exc, "data", None)
    detail = getattr(data, "error", None)
    code = getattr(detail, "code", None)
    if isinstance(code, str):
        return code
    body = getattr(exc, "body", None)
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError:
            return None
    if not isinstance(body, str) or not body:
        return None
    try:
        parsed = json.loads(body)
    except ValueError:
        return None
    if not isinstance(parsed, dict):
        return None
    detail = parsed.get("error")
    if not isinstance(detail, dict):
        return None
    code = detail.get("code")
    return code if isinstance(code, str) else None


def is_resource_locked(exc: BaseException) -> bool:
    """True for a 409 whose error code is ``RESOURCE_LOCKED``.

    Matches on the code, never the message: ``CONFLICT`` and
    ``IDEMPOTENCY_KEY_CONFLICT`` are also delivered as 409 and must not be
    retried.
    """
    if not isinstance(exc, ApiException) or exc.status != _HTTP_CONFLICT:
        return False
    return error_code(exc) == RESOURCE_LOCKED_ERROR_CODE


class _LoadRetryMixin:
    """Shared retry loop for the ``/loads`` operations."""

    load_retry: LoadRetryPolicy

    def _backoff_delay(self, exc: ApiException, attempt: int) -> float:
        policy = self.load_retry
        retry_after = _parse_retry_after(getattr(exc, "headers", None))
        if retry_after is not None:
            # Honour the server's hint; jitter only ever adds on top, and the
            # per-delay cap does not apply (the deadline is the only bound).
            return retry_after + retry_after * policy.jitter * random.random()
        base = policy.base_backoff_s * (2 ** (attempt - 1))
        return min(base + base * policy.jitter * random.random(), policy.max_backoff_s)

    def _call_with_lock_retry(
        self, what: str, fn: Callable[..., _T], *args: Any, **kwargs: Any
    ) -> _T:
        policy = self.load_retry
        deadline = time.monotonic() + policy.deadline_s
        attempts = 0
        while True:
            attempts += 1
            try:
                return fn(*args, **kwargs)
            except ApiException as exc:
                if not is_resource_locked(exc):
                    raise
                if attempts > policy.max_retries:
                    raise TableLockedError(
                        attempts=attempts,
                        reason=(
                            f"{what}: table still locked after {policy.max_retries} "
                            "retries (HTTP 409 RESOURCE_LOCKED)"
                        ),
                        last_exc=exc,
                    ) from exc
                delay = self._backoff_delay(exc, attempts)
                if time.monotonic() + delay > deadline:
                    raise TableLockedError(
                        attempts=attempts,
                        reason=(
                            f"{what}: table still locked after the "
                            f"{policy.deadline_s}s retry budget (HTTP 409 RESOURCE_LOCKED)"
                        ),
                        last_exc=exc,
                    ) from exc
                _log.info(
                    "%s: another load holds the table (409 RESOURCE_LOCKED); "
                    "retrying in %.1fs (attempt %d/%d)",
                    what,
                    delay,
                    attempts,
                    policy.max_retries,
                )
                time.sleep(delay)


class DatabasesApi(_LoadRetryMixin, _GeneratedDatabasesApi):
    """Drop-in replacement for :class:`hotdata.api.databases_api.DatabasesApi`
    whose :meth:`load_database_table` retries while another load holds the
    table (HTTP 409 ``RESOURCE_LOCKED``). All other methods work unchanged.

    :param load_retry: Retry policy for locked tables; defaults to
        :class:`LoadRetryPolicy`.
    """

    def __init__(
        self, api_client: Any = None, *, load_retry: Optional[LoadRetryPolicy] = None
    ) -> None:
        super().__init__(api_client)
        self.load_retry = load_retry or LoadRetryPolicy()

    def load_database_table(self, *args: Any, **kwargs: Any) -> Any:
        """Load a database table, retrying while another load holds it.

        Same signature and result as the generated
        :meth:`~hotdata.api.databases_api.DatabasesApi.load_database_table`.
        A 409 with error code ``RESOURCE_LOCKED`` is retried per
        :attr:`load_retry` (honouring ``Retry-After``); any other error,
        including a 409 ``CONFLICT`` / ``IDEMPOTENCY_KEY_CONFLICT``, is raised
        unchanged.

        :raises TableLockedError: the table stayed locked past the retry budget.
        """
        return self._call_with_lock_retry(
            "load_database_table", super().load_database_table, *args, **kwargs
        )


class ConnectionsApi(_LoadRetryMixin, _GeneratedConnectionsApi):
    """Drop-in replacement for :class:`hotdata.api.connections_api.ConnectionsApi`
    whose :meth:`load_managed_table` retries while another load holds the
    table (HTTP 409 ``RESOURCE_LOCKED``). All other methods work unchanged.

    :param load_retry: Retry policy for locked tables; defaults to
        :class:`LoadRetryPolicy`.
    """

    def __init__(
        self, api_client: Any = None, *, load_retry: Optional[LoadRetryPolicy] = None
    ) -> None:
        super().__init__(api_client)
        self.load_retry = load_retry or LoadRetryPolicy()

    def load_managed_table(self, *args: Any, **kwargs: Any) -> Any:
        """Load a managed table, retrying while another load holds it.

        Same signature and result as the generated
        :meth:`~hotdata.api.connections_api.ConnectionsApi.load_managed_table`.
        A 409 with error code ``RESOURCE_LOCKED`` is retried per
        :attr:`load_retry` (honouring ``Retry-After``); any other error,
        including a 409 ``CONFLICT`` / ``IDEMPOTENCY_KEY_CONFLICT``, is raised
        unchanged.

        :raises TableLockedError: the table stayed locked past the retry budget.
        """
        return self._call_with_lock_retry(
            "load_managed_table", super().load_managed_table, *args, **kwargs
        )


__all__ = [
    "RESOURCE_LOCKED_ERROR_CODE",
    "ConnectionsApi",
    "DatabasesApi",
    "LoadRetryPolicy",
    "TableLockedError",
    "error_code",
    "is_resource_locked",
]
