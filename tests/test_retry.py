"""Tests for transparent pre-response connection-reset retry (#118).

A pooled keep-alive connection reused after an intermediary has dropped it for
idle-timeout fails immediately with::

    ProtocolError('Connection aborted.', ConnectionResetError(54, 'reset by peer'))

before the request reaches the server. That is safe to retry on any method,
including POST, because the server did no work. These tests pin three things:

* the reset is retried on a fresh connection regardless of method (the fix);
* read **timeouts** stay idempotent-only — a POST that may have reached the
  server is never blindly replayed;
* ``Configuration`` installs this policy by default but an explicit ``retries``
  still overrides it.

The end-to-end tests drive urllib3's real ``HTTPConnectionPool.urlopen`` retry
machinery (the layer below ``RESTClientObject``, where the retry actually
happens) with ``_make_request`` stubbed to fail once then succeed.
"""

from __future__ import annotations

from unittest import mock

import pytest
from urllib3 import HTTPConnectionPool, HTTPResponse
from urllib3.exceptions import (
    ConnectTimeoutError,
    MaxRetryError,
    ProtocolError,
    ProxyError,
    ReadTimeoutError,
)
from urllib3.util.retry import Retry

from hotdata._retry import (
    ConnectionResetRetry,
    _is_pre_response_connection_reset,
    default_retry,
)
from hotdata.configuration import Configuration


def _reset_error() -> ProtocolError:
    """The exact error urllib3 raises for a reset on a stale pooled socket."""
    return ProtocolError(
        "Connection aborted.", ConnectionResetError(54, "Connection reset by peer")
    )


def _read_timeout() -> ReadTimeoutError:
    """A read timeout — raised after the request was sent, so retrying it on a
    non-idempotent method risks double execution."""
    pool = HTTPConnectionPool("example.invalid", 80)
    return ReadTimeoutError(pool, "/v1/query", "read timed out")


def _drive(method: str, error: Exception, retry: Retry, *, fail_times: int = 1):
    """Run ``method`` through a real urllib3 pool whose ``_make_request`` raises
    ``error`` for the first ``fail_times`` attempts, then returns 200.

    Returns ``(result_or_exception, make_request_call_count)``. ``_get_conn`` /
    ``_put_conn`` are stubbed so no socket is opened; only the retry control flow
    is exercised.
    """
    pool = HTTPConnectionPool("example.invalid", 80)
    calls = {"n": 0}

    def fake_make_request(conn, m, url, **kw):
        calls["n"] += 1
        if calls["n"] <= fail_times:
            raise error
        return HTTPResponse(
            body=b"", status=200, headers={}, preload_content=False, request_method=m
        )

    with mock.patch.object(pool, "_get_conn", return_value=mock.Mock()), \
            mock.patch.object(pool, "_put_conn"), \
            mock.patch.object(pool, "_make_request", side_effect=fake_make_request):
        try:
            resp = pool.urlopen(method, "/v1/query", retries=retry, release_conn=False)
            return resp, calls["n"]
        except Exception as exc:  # noqa: BLE001 - the test inspects the type
            return exc, calls["n"]


# -- the bug: urllib3's default reraises a POST reset ----------------------------


def test_stock_urllib3_retry_does_not_retry_post_reset():
    """Reproduces #118: the stock policy retries GET but reraises POST."""
    get_result, get_calls = _drive("GET", _reset_error(), Retry(total=3))
    assert isinstance(get_result, HTTPResponse) and get_calls == 2

    post_result, post_calls = _drive("POST", _reset_error(), Retry(total=3))
    assert isinstance(post_result, ProtocolError)
    assert post_calls == 1  # never retried


# -- the fix: pre-response resets retry on every method --------------------------


@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE", "GET"])
def test_connection_reset_retried_on_all_methods(method):
    result, calls = _drive(method, _reset_error(), default_retry())
    assert isinstance(result, HTTPResponse) and result.status == 200
    assert calls == 2  # failed once, succeeded on the fresh connection


def test_reset_retry_is_bounded_and_eventually_raises():
    """The reset retry is bounded by ``total``; once exhausted it surfaces."""
    retry = ConnectionResetRetry(total=2, backoff_factor=0)
    result, calls = _drive("POST", _reset_error(), retry, fail_times=99)
    assert isinstance(result, MaxRetryError)
    assert calls == 3  # initial attempt + 2 retries


# -- read/status retries stay idempotent-only ------------------------------------


def test_read_timeout_not_retried_on_post():
    """A read timeout may mean the server began processing — POST must not
    replay it, so the idempotent-only gate is preserved."""
    result, calls = _drive("POST", _read_timeout(), default_retry())
    assert isinstance(result, ReadTimeoutError)
    assert calls == 1


def test_read_timeout_still_retried_on_get():
    result, calls = _drive("GET", _read_timeout(), default_retry())
    assert isinstance(result, HTTPResponse) and calls == 2


def test_default_retry_does_not_retry_status_codes():
    """A 503 means the request reached the server; the default does not retry
    status codes (429 has dedicated handling in hotdata.query)."""
    assert default_retry().status == 0
    assert default_retry().status_forcelist in (None, frozenset(), set())


# -- the pre-response detector ---------------------------------------------------


@pytest.mark.parametrize(
    "cause",
    [
        ConnectionResetError(54, "reset by peer"),
        ConnectionAbortedError(53, "aborted"),
        BrokenPipeError(32, "broken pipe"),
    ],
)
def test_detector_matches_connection_level_causes(cause):
    assert _is_pre_response_connection_reset(ProtocolError("Connection aborted.", cause))


def test_detector_unwraps_proxy_error():
    inner = ProtocolError("Connection aborted.", ConnectionResetError(54, "reset"))
    assert _is_pre_response_connection_reset(ProxyError("proxy", inner))


@pytest.mark.parametrize(
    "error",
    [
        ProtocolError("Response ended prematurely"),  # no wrapped cause
        ProtocolError("boom", ValueError("not a socket error")),
        ValueError("unrelated"),
    ],
)
def test_detector_rejects_non_connection_errors(error):
    assert not _is_pre_response_connection_reset(error)


def test_classifier_treats_reset_as_connection_error():
    retry = ConnectionResetRetry(total=3)
    # Reclassified: a reset is a connection error (not method-gated)...
    assert retry._is_connection_error(_reset_error())
    # ...while a connect timeout is still a connection error (super's behavior)...
    assert retry._is_connection_error(ConnectTimeoutError())
    # ...and a read timeout is not.
    assert not retry._is_connection_error(_read_timeout())


# -- Configuration wiring --------------------------------------------------------


def test_configuration_installs_reset_retry_by_default():
    cfg = Configuration()
    assert isinstance(cfg.retries, ConnectionResetRetry)


def test_explicit_retries_overrides_default():
    cfg = Configuration(retries=0)
    assert cfg.retries == 0

    custom = Retry(total=7)
    cfg2 = Configuration(retries=custom)
    assert cfg2.retries is custom


def test_default_retry_flows_into_rest_pool_args():
    """The installed policy must actually reach urllib3's pool manager."""
    from hotdata.rest import RESTClientObject

    cfg = Configuration()
    with mock.patch("urllib3.PoolManager") as pm:
        RESTClientObject(cfg)
    _, kwargs = pm.call_args
    assert kwargs["retries"] is cfg.retries
    assert isinstance(kwargs["retries"], ConnectionResetRetry)
