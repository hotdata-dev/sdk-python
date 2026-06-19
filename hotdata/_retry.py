"""Transparent retry of pre-response connection resets (#118).

A pooled keep-alive connection can be reused after an intermediary (load
balancer / reverse proxy) has already dropped it for exceeding its idle
timeout. The client is not notified, so the next request that reuses that
socket fails immediately with::

    urllib3.exceptions.ProtocolError:
        ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))

urllib3 classifies *every* :class:`~urllib3.exceptions.ProtocolError` as a
*read* error (see ``Retry._is_read_error``) — it conservatively assumes the
server may have begun processing the request. Read retries are gated by
``allowed_methods``, which does not include ``POST``, so a ``POST`` that hits a
dead pooled connection is re-raised to the caller instead of being retried.

But a reset that happens *before any response bytes arrive* means the request
never reached the server — the connection was already gone when urllib3 tried
to send. That is safe to retry on **any** method, ``POST`` included, because the
server did no work and a retry cannot double-execute.

:class:`ConnectionResetRetry` reclassifies exactly that case — a
``ProtocolError`` whose underlying cause is a connection-level ``OSError`` — as
a *connection* error. urllib3's ``Retry.increment`` handles connection errors
before read errors and without the ``allowed_methods`` gate, so the reset is
retried on a fresh connection regardless of method. Read **timeouts**
(:class:`~urllib3.exceptions.ReadTimeoutError`) and status retries are left
untouched and stay idempotent-only, so a ``POST`` that may have reached the
server is never blindly replayed.
"""

from __future__ import annotations

from urllib3.exceptions import ProtocolError, ProxyError
from urllib3.util.retry import Retry

# Bounded attempts for the transparent connection-reset retry. Stale-pool resets
# clear on the first fresh connection, so a small ceiling is plenty; it also
# bounds the blast radius if a host is genuinely refusing connections.
DEFAULT_TOTAL_RETRIES = 3

# A small exponential backoff between attempts. The first retry on a fresh
# connection almost always succeeds, so the delay stays sub-second; it exists
# only to avoid hammering a host that is briefly flapping.
DEFAULT_BACKOFF_FACTOR = 0.1


def _is_pre_response_connection_reset(error: BaseException) -> bool:
    """True for a connection reset/abort that occurred before any response.

    urllib3 wraps a low-level socket failure raised while sending the request as
    ``ProtocolError("Connection aborted.", <cause>)``, where ``<cause>`` is the
    originating :class:`OSError` (``ConnectionResetError``,
    ``ConnectionAbortedError``, ``BrokenPipeError``, …). Those builtin
    connection errors all subclass :class:`ConnectionError`, so the cause's type
    is a precise, message-independent signal that the failure was at the socket
    layer before a response existed — distinct from a read **timeout**, which
    urllib3 raises as a ``ReadTimeoutError`` (not a ``ProtocolError``) and which
    we deliberately leave method-gated.
    """
    if isinstance(error, ProxyError):
        error = error.original_error
    if not isinstance(error, ProtocolError):
        return False
    cause = error.args[1] if len(error.args) > 1 else None
    return isinstance(cause, ConnectionError)


class ConnectionResetRetry(Retry):
    """A :class:`urllib3.util.retry.Retry` that retries pre-response connection
    resets on any HTTP method, while leaving read/status retries idempotent-only.

    Behaves exactly like ``Retry`` except a connection reset/abort that happened
    before any response bytes were received (see
    :func:`_is_pre_response_connection_reset`) is treated as a *connection*
    error rather than a *read* error. urllib3's ``increment`` retries connection
    errors without consulting ``allowed_methods``, so the reset is retried on a
    fresh connection for ``POST`` too — safe because the server did no work.
    """

    def _is_connection_error(self, err: Exception) -> bool:
        if super()._is_connection_error(err):
            return True
        return _is_pre_response_connection_reset(err)


def default_retry() -> ConnectionResetRetry:
    """The SDK's default retry policy.

    Matches urllib3's defaults (idempotent-only read/status retries, a bounded
    total, no retry on response status codes) and adds transparent retry of
    pre-response connection resets on every method. ``Configuration`` installs
    this when the caller does not supply their own ``retries``.
    """
    return ConnectionResetRetry(
        total=DEFAULT_TOTAL_RETRIES,
        backoff_factor=DEFAULT_BACKOFF_FACTOR,
        # Don't retry on response status codes by default: a status code means
        # the request reached the server, and 429 admission-shedding already has
        # dedicated handling in hotdata.query. Connection-reset retry is purely a
        # transport-layer concern.
        status=0,
        raise_on_status=False,
    )


__all__ = [
    "ConnectionResetRetry",
    "DEFAULT_BACKOFF_FACTOR",
    "DEFAULT_TOTAL_RETRIES",
    "default_retry",
]
