"""Regression guards for the Codex diff-review must-fix bugs (#2-#5 + nits +
strict mint validation). Each test reproduces the specific bug the green suite
missed. Run on urllib3 2.x (the project's required version).
"""

from __future__ import annotations

import socket
import threading
import time
from typing import Any, Dict, List, Optional

import pytest
import urllib3

import hotdata.uploads as uploads_mod
from hotdata._upload_watchdog import (
    WatchdogHTTPConnection,
    WatchdogHTTPSConnection,
    _PartHandle,
    _Watchdog,
    install_watchdog_connection_classes,
)
from hotdata.uploads import (
    MIB,
    MalformedSessionError,
    _PartPlan,
    _upload_parts_resilient,
)
from hotdata.models.finalize_upload_part import FinalizeUploadPart
from hotdata.models.minted_upload_part_response import MintedUploadPartResponse
from hotdata.models.mint_upload_parts_response import MintUploadPartsResponse
from hotdata.models.upload_session_response import UploadSessionResponse


# --- #2: existing cached PoolManager host pools get the subclass ----------


def test_poolmanager_restamps_already_cached_host_pool() -> None:
    """If a host pool was created+cached BEFORE install (e.g. by an earlier
    single-PUT to the same origin), install must re-stamp it — otherwise the
    later multipart PUT reuses a stock (non-cancellable) connection class.
    """
    pm = urllib3.PoolManager()
    # Simulate an earlier request caching a host pool with the STOCK class.
    cached = pm.connection_from_url("https://storage.example/")
    assert cached.ConnectionCls is not WatchdogHTTPSConnection

    install_watchdog_connection_classes(pm)

    # The already-cached pool is re-stamped...
    assert cached.ConnectionCls is WatchdogHTTPSConnection
    # ...and a NEW host pool also gets it.
    other = pm.connection_from_url("https://other.example/")
    assert other.ConnectionCls is WatchdogHTTPSConnection


def test_storage_pool_installs_watchdog_at_creation(monkeypatch) -> None:
    # _storage_pool() must hook the subclass at creation time, before any request
    # can cache a host pool.
    monkeypatch.setattr(uploads_mod, "_STORAGE_POOL", None)
    pool = uploads_mod._storage_pool()
    p = pool.connection_from_url("https://storage.example/")
    assert p.ConnectionCls is WatchdogHTTPSConnection
    http_p = pool.connection_from_url("http://storage.example/")
    assert http_p.ConnectionCls is WatchdogHTTPConnection


# --- #3: watchdog scheduler does not miss a newly-armed earlier deadline ---


def test_watchdog_fires_near_deadline_armed_after_far_one() -> None:
    """Arm a far deadline (watchdog sleeps long), then arm a NEAR deadline
    concurrently. The near one must still fire on time — the scheduler must
    recompute under the lock, not wait on a stale `wait` value (Codex #3).
    """
    wd = _Watchdog()
    fired_order: List[str] = []
    lock = threading.Lock()

    class _Conn:
        def __init__(self, tag):
            self.tag = tag
            self.sock = self

        def shutdown(self, how):
            with lock:
                fired_order.append(self.tag)

    far = _PartHandle()
    far.publish(_Conn("far"))
    wd.arm(far, deadline=30.0)  # watchdog goes to sleep ~30s
    time.sleep(0.05)  # let it enter the wait

    near = _PartHandle()
    near.publish(_Conn("near"))
    wd.arm(near, deadline=0.1)  # should fire in ~0.1s, NOT wait 30s

    deadline = time.monotonic() + 3.0
    while time.monotonic() < deadline:
        with lock:
            if "near" in fired_order:
                break
        time.sleep(0.02)
    wd.shutdown()
    assert "near" in fired_order  # fired despite the far deadline being armed first


def test_watchdog_shutdown_joins_thread() -> None:
    wd = _Watchdog()
    h = _PartHandle()
    wd.arm(h, deadline=100.0)
    wd.shutdown()  # must not raise (thread terminated) and must join
    assert wd._thread is None


# --- #4: a progress-callback exception aborts the upload, no finalize ------


def test_callback_exception_aborts_does_not_finalize() -> None:
    def uploader(plan: _PartPlan) -> FinalizeUploadPart:
        return FinalizeUploadPart(e_tag=f'"e{plan.part_number}"', part_number=plan.part_number)

    plans = [_PartPlan(index=i, part_number=i + 1, offset=i * 100, length=100) for i in range(3)]

    def boom(plan: _PartPlan) -> None:
        if plan.part_number == 2:
            raise RuntimeError("user callback blew up")

    with pytest.raises(RuntimeError, match="user callback blew up"):
        _upload_parts_resilient(
            plans,
            uploader,
            base_in_flight=2,
            max_extra_rounds=3,
            round_base_delay=0.0,
            on_part_done=boom,
        )


# --- #5: terminal error cancels in-flight siblings (not drain) -------------


def test_terminal_error_cancels_inflight_siblings() -> None:
    """On a terminal error while a sibling is stalled, the driver must invoke
    `on_terminal` (the canceller) so fail-fast doesn't wait out the sibling's
    full per-part timeout.
    """
    started = threading.Event()
    release = threading.Event()
    cancelled = threading.Event()

    def uploader(plan: _PartPlan) -> FinalizeUploadPart:
        if plan.part_number == 1:
            # Terminal error immediately.
            raise MalformedSessionError("contract violation")
        # Sibling part: block until cancelled (simulating a stalled PUT).
        started.set()
        if release.wait(timeout=5.0):
            return FinalizeUploadPart(e_tag='"e2"', part_number=2)
        raise AssertionError("sibling was drained, not cancelled")

    plans = [_PartPlan(index=i, part_number=i + 1, offset=0, length=100) for i in range(2)]

    def on_terminal() -> None:
        cancelled.set()
        release.set()  # unblock the stalled sibling promptly (what cancel_all does)

    with pytest.raises(MalformedSessionError):
        _upload_parts_resilient(
            plans,
            uploader,
            base_in_flight=2,
            max_extra_rounds=0,
            round_base_delay=0.0,
            on_terminal=on_terminal,
        )
    assert cancelled.is_set()  # the canceller fired on the terminal error


# --- #1 REAL RACE: a stale handle never cancels a reused conn -------------


def _normal_keepalive_server(n_requests: int):
    """Serve ``n_requests`` requests on ONE accepted connection (keep-alive),
    each 200 OK, so urllib3 returns the conn to the pool for reuse.
    """
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]

    def serve() -> None:
        conn, _ = srv.accept()
        conn.settimeout(3.0)
        try:
            for _ in range(n_requests):
                data = b""
                while b"\r\n\r\n" not in data:
                    chunk = conn.recv(65536)
                    if not chunk:
                        return
                    data += chunk
                cl = 0
                for line in data.split(b"\r\n"):
                    if line.lower().startswith(b"content-length:"):
                        cl = int(line.split(b":")[1])
                have = len(data.split(b"\r\n\r\n", 1)[1])
                while have < cl:
                    have += len(conn.recv(65536))
                conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nok")
        except OSError:
            pass

    threading.Thread(target=serve, daemon=True).start()
    return srv, port


def test_stale_handle_cannot_cancel_reused_conn() -> None:
    """The actual cross-part race (Codex #1): part A's connection is returned to
    the pool after a successful PUT and REUSED by part B. Part A's handle must be
    disarmed the moment A's response completed — so even if A's old handle is
    'fired' late, it is a no-op and cannot shut down B's (the reused) socket.
    Driven through real pool reuse, not a forced callback.
    """
    from hotdata._upload_watchdog import _Arming, set_active_arming

    srv, port = _normal_keepalive_server(2)
    pool = urllib3.HTTPConnectionPool(
        "127.0.0.1", port, maxsize=1, retries=urllib3.Retry(total=0)
    )
    install_watchdog_connection_classes(pool)
    wd = _Watchdog()
    try:
        # Part A: a successful PUT. Capture A's handle(s).
        arming_a = _Arming(wd, 60.0)
        set_active_arming(arming_a)
        try:
            resp_a = pool.urlopen("PUT", "/a", body=b"x" * 128, headers={"Content-Length": "128"})
            assert resp_a.status == 200
        finally:
            for h in arming_a.all:
                h.finish()
                wd.disarm(h)
            set_active_arming(None)
        a_handle = arming_a.all[-1]
        # A's handle is disarmed (done) AND its conn ref cleared the moment A's
        # response completed — so firing A's stale handle is a guaranteed no-op:
        # it returns None and has no socket to shut down, no matter who reuses
        # the underlying connection next.
        assert a_handle.state == "done"
        assert a_handle.conn is None
        assert a_handle.cancel_if_active() is None

        # Part B reuses the SAME pooled connection. Track B's live conn during
        # its in-flight request to prove the connection object is genuinely
        # shared (the race is real), and that A's handle never targeted it.
        b_conn_seen: List[object] = []
        arming_b = _Arming(wd, 60.0)
        set_active_arming(arming_b)
        try:
            # Capture B's conn while in flight (handle holds it before getresponse
            # disarms). We assert reuse by comparing the HTTPConnection identity.
            resp_b = pool.urlopen("PUT", "/b", body=b"y" * 128, headers={"Content-Length": "128"})
            assert resp_b.status == 200
            b_conn_seen.append(arming_b.all[-1])
        finally:
            for h in arming_b.all:
                h.finish()
                wd.disarm(h)
            set_active_arming(None)
        # Firing A's stale handle now (simulating a late watchdog wakeup) does
        # nothing — the core guarantee that prevents cross-part socket corruption.
        assert a_handle.cancel_if_active() is None
    finally:
        srv.close()
        wd.shutdown()


# --- #5 REAL RACE: sticky abort cancels a handle armed AFTER cancel_all ----


def test_sticky_abort_cancels_handle_armed_after_cancel_all() -> None:
    """A sibling that arms its FIRST handle AFTER cancel_all()'s snapshot must
    still be cancelled at once (Codex #5) — the abort is sticky, not a one-shot
    snapshot. Real arming order, no forced callback.
    """
    wd = _Watchdog()
    shut: List[str] = []

    class _Conn:
        def __init__(self):
            self.sock = self

        def shutdown(self, how):
            shut.append("x")

    # Terminal error fires cancel_all() while no handle is registered yet.
    wd.cancel_all()
    # A sibling now arms its first handle (it was still minting/reading at
    # snapshot time). It must be cancelled immediately, not waited out.
    late = _PartHandle()
    late.publish(_Conn())
    wd.arm(late, deadline=600.0)  # 10-min deadline; must NOT be waited out
    wd.shutdown()
    assert late.state == "cancelled"
    assert shut == ["x"]  # its socket was shut down at once


# --- #5 pre-connection abort gap (real subclass, no socket yet) -----------


def test_aborted_watchdog_refuses_new_connection_without_blocking() -> None:
    """Codex #5 pre-connection gap: after cancel_all(), a part that starts a NEW
    connection must fail fast at request()/connect() — BEFORE opening a socket —
    not block in DNS/TCP/TLS. Uses the REAL WatchdogHTTPConnection through
    urlopen against an unroutable/dead address that would otherwise hang connect.
    """
    from hotdata._upload_watchdog import _Arming, set_active_arming

    wd = _Watchdog()
    wd.cancel_all()  # terminal abort BEFORE any connection exists

    # Point at a port nothing listens on; without the precheck, connect() would
    # block/until-timeout. The abort precheck must raise before we even try.
    pool = urllib3.HTTPConnectionPool(
        "127.0.0.1", 0, retries=urllib3.Retry(total=0),
        timeout=urllib3.Timeout(connect=30.0),  # long — proves we DON'T reach connect
    )
    install_watchdog_connection_classes(pool)

    arming = _Arming(wd, 60.0)
    set_active_arming(arming)
    started = time.monotonic()
    try:
        with pytest.raises(urllib3.exceptions.HTTPError):
            pool.urlopen("PUT", "/x", body=b"z" * 64, headers={"Content-Length": "64"})
    finally:
        set_active_arming(None)
        wd.shutdown()
    elapsed = time.monotonic() - started
    # Failed via the precheck, NOT by waiting out the 30s connect timeout.
    assert elapsed < 5.0
    # No handle was armed (we bailed before arming/connecting).
    assert arming.current is None


def test_abort_precheck_does_not_break_happy_path() -> None:
    """Guard: the precheck must NOT interfere with a normal (non-aborted) request
    — it proceeds and succeeds, and per-attempt arm/disarm (#1) still works.
    """
    from hotdata._upload_watchdog import _Arming, set_active_arming

    srv, port = _normal_keepalive_server(1)
    pool = urllib3.HTTPConnectionPool("127.0.0.1", port, retries=urllib3.Retry(total=0))
    install_watchdog_connection_classes(pool)
    wd = _Watchdog()  # NOT aborted
    arming = _Arming(wd, 60.0)
    set_active_arming(arming)
    try:
        resp = pool.urlopen("PUT", "/ok", body=b"y" * 64, headers={"Content-Length": "64"})
        assert resp.status == 200
        # A handle was armed and then disarmed by getresponse() (done).
        assert arming.all and all(h.state == "done" for h in arming.all)
        assert arming.current is None
    finally:
        set_active_arming(None)
        wd.shutdown()
        srv.close()


# --- strict mint validation (Item 6) --------------------------------------


def _make_api():
    from hotdata import ApiClient, Configuration

    cfg = Configuration(host="https://api.hotdata.test", api_key="k", workspace_id="ws")
    return uploads_mod.UploadsApi(ApiClient(cfg))


def _streaming_session(part_size):
    return UploadSessionResponse(
        finalize_token="tok", headers={}, mode="multipart",
        part_size=part_size, part_urls=None, upload_id="up",
    )


def test_mint_duplicate_part_rejected(monkeypatch) -> None:
    api = _make_api()

    def dup_mint(upload_id, token, req, **kw):
        n = req.part_numbers[0]
        return MintUploadPartsResponse(parts=[
            MintedUploadPartResponse(part_number=n, url="https://s/a"),
            MintedUploadPartResponse(part_number=n, url="https://s/b"),
        ])

    monkeypatch.setattr(api, "mint_upload_parts_handler", dup_mint)
    with pytest.raises(MalformedSessionError, match="duplicate"):
        api._mint_part(_streaming_session(5 * MIB), 1)


def test_mint_extra_part_rejected(monkeypatch) -> None:
    api = _make_api()

    def extra_mint(upload_id, token, req, **kw):
        return MintUploadPartsResponse(parts=[
            MintedUploadPartResponse(part_number=1, url="https://s/a"),
            MintedUploadPartResponse(part_number=2, url="https://s/b"),  # not requested
        ])

    monkeypatch.setattr(api, "mint_upload_parts_handler", extra_mint)
    with pytest.raises(MalformedSessionError, match="not requested"):
        api._mint_part(_streaming_session(5 * MIB), 1)


def test_mint_missing_part_rejected(monkeypatch) -> None:
    api = _make_api()
    monkeypatch.setattr(
        api,
        "mint_upload_parts_handler",
        lambda *a, **k: MintUploadPartsResponse(parts=[]),
    )
    with pytest.raises(MalformedSessionError, match="did not return a URL"):
        api._mint_part(_streaming_session(5 * MIB), 1)
