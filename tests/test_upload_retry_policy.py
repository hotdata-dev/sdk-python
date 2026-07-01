"""Tests for the part-PUT retry policy + per-part timeout + error classification
(Items 2, 3, 5).

The inner retry tier is a narrowed ``urllib3.Retry`` (``ConnectionResetRetry``
base) on the storage pool, reached via ``pool.urlopen``:

* 429 retried (honoring ``Retry-After``); pre-response connection resets retried
  on any method (incl. the watchdog's ``ProtocolError(RemoteDisconnected)``);
* storage **5xx EXCLUDED** from the forcelist — it propagates to the OUTER
  re-sweep (the tier boundary, Item 5 / Flag #5);
* ``backoff_max`` ~120s caps a pathological ``Retry-After`` (the deadline analog).

``_part_put_timeout`` is the size-scaled per-attempt transfer cap the watchdog
enforces. ``_is_retryable`` is the allowlist the outer re-sweep consults.
"""

from __future__ import annotations

import errno
from http.client import RemoteDisconnected

import pytest
from urllib3.exceptions import ProtocolError
from urllib3.util.retry import Retry

from hotdata._retry import ConnectionResetRetry
from hotdata.uploads import (
    MIB,
    MalformedSessionError,
    MissingETagError,
    SizeLimitError,
    StorageError,
    StorageTransportError,
    UploadError,
    _is_retryable,
    _parse_etag,
    _part_put_timeout,
    default_part_retry,
)
from hotdata.exceptions import ApiException


# --- default_part_retry narrowing (Item 5) --------------------------------


def test_default_part_retry_excludes_5xx_keeps_429() -> None:
    retry = default_part_retry()
    forcelist = set(retry.status_forcelist or ())
    assert 429 in forcelist
    for code in (500, 502, 503, 504):
        assert code not in forcelist, f"{code} must propagate to the outer re-sweep"


def test_default_part_retry_is_connection_reset_retry() -> None:
    # Based on ConnectionResetRetry so a pre-response reset (and the watchdog's
    # ProtocolError) is retried on PUT, not method-gated away.
    assert isinstance(default_part_retry(), ConnectionResetRetry)


def test_default_part_retry_does_not_raise_on_status() -> None:
    assert default_part_retry().raise_on_status is False


def test_default_part_retry_honors_retry_after() -> None:
    assert default_part_retry().respect_retry_after_header is True


def test_default_part_retry_does_not_follow_redirects() -> None:
    # A 3xx on a presigned PUT would re-issue to a new URL and invalidate the
    # signature; never chase it (Codex #6).
    retry = default_part_retry()
    assert retry.redirect is False or retry.redirect == 0


def test_default_part_retry_caps_backoff_near_120s() -> None:
    # backoff_max is the deadline analog: a pathological Retry-After/backoff is
    # capped so the round-join can't stall on an unbounded sleep.
    retry = default_part_retry()
    # urllib3 >=2 exposes the cap as `backoff_max`; 1.26 as `DEFAULT_BACKOFF_MAX`
    # (the value `get_backoff_time` actually reads). Either way it must be <=120.
    backoff_max = getattr(retry, "backoff_max", None)
    if backoff_max is None:
        backoff_max = retry.DEFAULT_BACKOFF_MAX
    assert backoff_max <= 120


# --- the watchdog ProtocolError is classified as a pre-response reset ------


def test_retry_after_capped_at_120s() -> None:
    """A server ``Retry-After`` is honored but CAPPED at 120s (the per-part
    retry-window deadline analog) so the re-sweep's round-boundary join can't
    stall on a multi-minute server value. ``backoff_max`` only bounds the
    exponential path; the cap lives in ``get_retry_after``.
    """
    retry = default_part_retry()

    class _Resp:
        def __init__(self, retry_after: str):
            self.headers = {"Retry-After": retry_after}

        def getheader(self, name, default=None):
            return self.headers.get(name, default)

    # A hostile hour-long Retry-After is clamped to 120s.
    assert retry.get_retry_after(_Resp("3600")) == 120
    # A reasonable value is honored as-is.
    assert retry.get_retry_after(_Resp("5")) == 5


def test_no_retry_after_passes_through_as_none() -> None:
    # No Retry-After header → None (the exponential backoff path is unaffected).
    retry = default_part_retry()

    class _NoHeader:
        headers: dict = {}

        def getheader(self, name, default=None):
            return default

    assert retry.get_retry_after(_NoHeader()) is None


def test_connection_reset_retry_classifies_watchdog_protocolerror() -> None:
    """The decisive Item-3/Item-5 check (architect-flagged): the watchdog's
    ``sock.shutdown`` surfaces through ``urlopen`` as
    ``ProtocolError(RemoteDisconnected)`` — the SAME shape ConnectionResetRetry
    already treats as a (retryable) connection error. If this regresses, a
    watchdog-cancelled part would NOT be re-swept.
    """
    retry = default_part_retry()
    watchdog_err = ProtocolError(
        "Connection aborted.",
        RemoteDisconnected("Remote end closed connection without response"),
    )
    assert retry._is_connection_error(watchdog_err)
    # And a plain reset (stale pooled socket) too.
    reset_err = ProtocolError("Connection aborted.", ConnectionResetError(errno.ECONNRESET, "reset"))
    assert retry._is_connection_error(reset_err)


# --- _part_put_timeout: size-scaled per-attempt transfer cap (Item 3) ------


def test_part_put_timeout_scales_and_caps() -> None:
    assert _part_put_timeout(8 * MIB) == pytest.approx(188.0)
    assert _part_put_timeout(64 * MIB) == pytest.approx(60.0 + 1024.0)
    assert _part_put_timeout(0) == pytest.approx(60.0)
    # Monotonic non-decreasing below the cap.
    assert _part_put_timeout(MIB) <= _part_put_timeout(2 * MIB) <= _part_put_timeout(8 * MIB)
    # Cap at 30 minutes for very large parts.
    assert _part_put_timeout(5 * 1024 * MIB) == pytest.approx(1800.0)
    assert _part_put_timeout(2**63) == pytest.approx(1800.0)


# --- _is_retryable allowlist (Item 2) -------------------------------------


def test_is_retryable_allowlist_true_cases() -> None:
    assert _is_retryable(StorageTransportError(url="u", part_number=1))
    assert _is_retryable(MissingETagError(part_number=1))
    assert _is_retryable(StorageError(status=500, part_number=1, body="x"))
    assert _is_retryable(StorageError(status=403, part_number=1, body="x"))  # eager URL expiry
    assert _is_retryable(ApiException(status=503))  # mint transient


def test_is_retryable_allowlist_false_cases() -> None:
    # Deterministic / contract / unexpected — NOT retried (no wasted rounds, no
    # duplicate PUT on a callback bug).
    assert not _is_retryable(MalformedSessionError("bad"))
    assert not _is_retryable(SizeLimitError(what="declared_size_bytes", value=2**63))
    assert not _is_retryable(UploadError("deterministic short read"))  # generic
    assert not _is_retryable(ValueError("unexpected"))
    assert not _is_retryable(RuntimeError("callback blew up"))


# --- _parse_etag: reject missing AND blank (Item 7) -----------------------


class _Headers:
    def __init__(self, data):
        self._data = {k.lower(): v for k, v in data.items()}

    def get(self, key, default=None):
        return self._data.get(key.lower(), default)


def test_parse_etag_passes_quoted_value_verbatim() -> None:
    assert _parse_etag(_Headers({"ETag": '"abc123"'}), part_number=1) == '"abc123"'


def test_parse_etag_rejects_missing() -> None:
    with pytest.raises(MissingETagError):
        _parse_etag(_Headers({}), part_number=2)


def test_parse_etag_rejects_empty_and_whitespace() -> None:
    with pytest.raises(MissingETagError):
        _parse_etag(_Headers({"ETag": ""}), part_number=3)
    with pytest.raises(MissingETagError):
        _parse_etag(_Headers({"ETag": "   "}), part_number=4)
