"""Tests for the per-part stall-cancellation watchdog (Item 3).

The watchdog must terminate a storage PUT that black-holes (the far end accepts
the connection but stops reading the request body, or never sends a response) so
the part fails INTO the outer re-sweep rather than hanging the upload forever.

The proven mechanism (spike ``conn_subclass_v2.py`` / ``subclass-spike-findings.md``
Spike 2b): a ``WatchdogHTTPConnection`` subclass injected via ``pool.ConnectionCls``
publishes its live ``.sock`` to a per-part handle on both ``connect()`` and
``request()``; the per-part *worker* owns the handle lifecycle around the whole
``pool.urlopen()`` call (arm before, ``finish()`` in ``finally``); on deadline the
watchdog calls ``sock.shutdown(SHUT_RDWR)`` (never ``close()`` — fd-reuse safety).

These tests use REAL sockets (a buffered fake cannot reproduce the kernel
send-buffer wedge), driven through urllib3's real ``urlopen``.
"""

from __future__ import annotations

import socket
import threading
import time
from typing import Dict, Optional, Tuple

import pytest
import urllib3

from hotdata._upload_watchdog import (
    _Arming,
    _PartHandle,
    _Watchdog,
    install_watchdog_connection_classes,
    set_active_arming,
)


# --- real-socket servers --------------------------------------------------


def _normal_server() -> Tuple[socket.socket, int]:
    """A server that reads the full request body then replies 200."""
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]

    def serve() -> None:
        conn, _ = srv.accept()
        conn.settimeout(2.0)
        data = b""
        try:
            while b"\r\n\r\n" not in data:
                chunk = conn.recv(65536)
                if not chunk:
                    break
                data += chunk
            content_length = 0
            for line in data.split(b"\r\n"):
                if line.lower().startswith(b"content-length:"):
                    content_length = int(line.split(b":")[1])
            have = len(data.split(b"\r\n\r\n", 1)[1]) if b"\r\n\r\n" in data else 0
            while have < content_length:
                chunk = conn.recv(65536)
                if not chunk:
                    break
                have += len(chunk)
            conn.sendall(b'HTTP/1.1 200 OK\r\nETag: "ok-etag"\r\nContent-Length: 2\r\n\r\nok')
        except OSError:
            pass
        finally:
            time.sleep(0.05)
            conn.close()

    threading.Thread(target=serve, daemon=True).start()
    return srv, port


def _stall_server(read_body: bool) -> Tuple[socket.socket, int, Dict[str, object]]:
    """A black-hole server. ``read_body=False`` never reads (SEND stall: the
    client wedges in the body write once the kernel send buffer fills);
    ``read_body=True`` drains the body but never replies (RESPONSE-read stall).
    """
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]
    hold: Dict[str, object] = {}

    def serve() -> None:
        conn, _ = srv.accept()
        hold["conn"] = conn
        if read_body:
            conn.settimeout(0.2)
            while not hold.get("stop"):
                try:
                    if not conn.recv(65536):
                        break
                except socket.timeout:
                    continue
                except OSError:
                    break
        else:
            while not hold.get("stop"):
                time.sleep(0.05)
        try:
            conn.close()
        except OSError:
            pass

    threading.Thread(target=serve, daemon=True).start()
    return srv, port, hold


def _pool(port: int) -> urllib3.HTTPConnectionPool:
    pool = urllib3.HTTPConnectionPool(
        "127.0.0.1", port, maxsize=2, retries=urllib3.Retry(total=0)
    )
    install_watchdog_connection_classes(pool)
    return pool


def _worker_put(
    pool: urllib3.HTTPConnectionPool,
    path: str,
    body: bytes,
    deadline: float,
    watchdog: object = None,
) -> Tuple[str, object, float, _Arming]:
    """Mirror the real per-part worker: stash an _Arming around urlopen (the
    connection subclass arms a fresh handle per attempt), disarm in finally.
    Returns the arming so the test can inspect each attempt's handle state.
    """
    own_watchdog = watchdog is None
    watchdog = watchdog or _Watchdog()
    arming = _Arming(watchdog, deadline)
    set_active_arming(arming)
    started = time.monotonic()
    try:
        resp = pool.urlopen(
            "PUT", path, body=body, headers={"Content-Length": str(len(body))}
        )
        return ("ok", resp.status, time.monotonic() - started, arming)
    except BaseException as exc:  # noqa: BLE001 - the test inspects the type
        return ("raised", exc, time.monotonic() - started, arming)
    finally:
        for handle in arming.all:
            handle.finish()
            watchdog.disarm(handle)
        set_active_arming(None)
        if own_watchdog:
            watchdog.shutdown()


# --- happy path -----------------------------------------------------------


def test_happy_path_through_urlopen_no_fire() -> None:
    srv, port = _normal_server()
    try:
        outcome, status, elapsed, arming = _worker_put(
            _pool(port), "/part/1?sig=abc", b"y" * 4096, deadline=5.0
        )
    finally:
        srv.close()
    assert outcome == "ok"
    assert status == 200
    # An attempt's handle was armed and the worker marked it done; never cancelled.
    assert arming.all
    assert all(h.state == "done" for h in arming.all)


# --- send-side black hole (request-body write wedges) ---------------------


def test_send_buffer_stall_cancelled() -> None:
    srv, port, hold = _stall_server(read_body=False)
    try:
        # 64 MiB body so the kernel send buffer fills and the worker wedges in send().
        outcome, exc, elapsed, arming = _worker_put(
            _pool(port), "/part/1?sig=b", b"z" * (64 * 1024 * 1024), deadline=1.0
        )
    finally:
        hold["stop"] = True
        srv.close()
    assert outcome == "raised"
    # urllib3 wraps the shutdown-induced failure as a ProtocolError.
    assert isinstance(exc, urllib3.exceptions.HTTPError)
    assert any(h.state == "cancelled" for h in arming.all)
    # Cancelled promptly after the ~1s deadline, not hung.
    assert elapsed < 5.0


# --- response-read black hole (server drains body, never replies) ---------


def test_response_read_stall_cancelled() -> None:
    srv, port, hold = _stall_server(read_body=True)
    try:
        outcome, exc, elapsed, arming = _worker_put(
            _pool(port), "/part/1?sig=c", b"w" * 8192, deadline=1.0
        )
    finally:
        hold["stop"] = True
        srv.close()
    assert outcome == "raised"
    assert isinstance(exc, urllib3.exceptions.HTTPError)
    assert any(h.state == "cancelled" for h in arming.all)
    assert elapsed < 5.0


# --- Codex #1: reused keep-alive conn is still protected ------------------


def _keepalive_then_stall_server() -> Tuple[socket.socket, int, Dict[str, object]]:
    """ONE server on ONE connection: serves the FIRST request normally
    (keep-alive, so urllib3 returns the conn to the pool), then on the SECOND
    request reads nothing — black-holing the body write on the REUSED conn.
    """
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]
    hold: Dict[str, object] = {}

    def serve() -> None:
        conn, _ = srv.accept()
        hold["conn"] = conn
        # First request: read headers + body, reply 200 with keep-alive.
        conn.settimeout(2.0)
        data = b""
        try:
            while b"\r\n\r\n" not in data:
                data += conn.recv(65536)
            cl = 0
            for line in data.split(b"\r\n"):
                if line.lower().startswith(b"content-length:"):
                    cl = int(line.split(b":")[1])
            have = len(data.split(b"\r\n\r\n", 1)[1])
            while have < cl:
                have += len(conn.recv(65536))
            conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nok")
        except OSError:
            return
        # Second request on the SAME conn: never read → send-stall.
        while not hold.get("stop"):
            time.sleep(0.05)
        try:
            conn.close()
        except OSError:
            pass

    threading.Thread(target=serve, daemon=True).start()
    return srv, port, hold


def test_reused_pooled_conn_send_stall_is_cancelled() -> None:
    """A pooled keep-alive connection does NOT call connect() on reuse — so
    arming must happen in request() (before the send), or a send-stall on a
    REUSED conn would be invisible to the watchdog. One server, one connection:
    request 1 succeeds (conn returns to the pool), request 2 reuses it and stalls.
    """
    srv, port, hold = _keepalive_then_stall_server()
    pool = urllib3.HTTPConnectionPool(
        "127.0.0.1", port, maxsize=1, retries=urllib3.Retry(total=0)
    )
    install_watchdog_connection_classes(pool)
    watchdog = _Watchdog()
    try:
        outcome1, status, _, _ = _worker_put(pool, "/ok", b"y" * 256, 5.0, watchdog)
        assert outcome1 == "ok" and status == 200
        # Reuse the pooled conn; the peer black-holes the body write.
        outcome2, exc2, elapsed2, arming2 = _worker_put(
            pool, "/stall", b"z" * (64 * 1024 * 1024), 1.0, watchdog
        )
    finally:
        hold["stop"] = True
        srv.close()
        watchdog.shutdown()
    assert outcome2 == "raised"
    assert isinstance(exc2, urllib3.exceptions.HTTPError)
    assert any(h.state == "cancelled" for h in arming2.all)
    assert elapsed2 < 5.0  # not hung


def _multi_stall_server() -> Tuple[socket.socket, int, Dict[str, object]]:
    """Accept MULTIPLE connections and black-hole each one's body write — so a
    urllib3-internal retry (which opens a fresh conn) stalls too.
    """
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(8)
    port = srv.getsockname()[1]
    hold: Dict[str, object] = {"conns": []}

    def serve() -> None:
        while not hold.get("stop"):
            try:
                srv.settimeout(0.2)
                conn, _ = srv.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            hold["conns"].append(conn)  # accept, never read → send stall

    threading.Thread(target=serve, daemon=True).start()
    return srv, port, hold


def test_internal_retry_attempt_is_also_watchdog_protected() -> None:
    """Codex #1b: after the watchdog cancels attempt 1, urllib3 classifies the
    resulting ProtocolError(RemoteDisconnected) as a pre-response reset and
    INTERNALLY retries on a fresh conn. That retry attempt must ALSO be armed
    (publish/arm happen per request()), so it can't run unbounded — both attempts
    get cancelled and the call returns promptly.
    """
    srv, port, hold = _multi_stall_server()
    # total=1 → one internal retry; ConnectionResetRetry-style would retry the
    # reset. Each attempt black-holes; each must be watchdog-armed+cancelled.
    pool = urllib3.HTTPConnectionPool(
        "127.0.0.1", port, maxsize=2,
        retries=urllib3.Retry(total=1, redirect=False, raise_on_status=False),
    )
    install_watchdog_connection_classes(pool)
    try:
        outcome, exc, elapsed, arming = _worker_put(
            pool, "/stall", b"z" * (64 * 1024 * 1024), 1.0
        )
    finally:
        hold["stop"] = True
        srv.close()
    assert outcome == "raised"
    # Both the initial attempt AND the internal retry were armed (≥2 handles),
    # and at least one was cancelled by the watchdog — none ran unbounded.
    assert len(arming.all) >= 2
    assert any(h.state == "cancelled" for h in arming.all)
    assert elapsed < 8.0  # bounded (≈ 2 × the 1s deadline), not hung


# --- Codex #9: watchdog-vs-finally interleaving ---------------------------


def test_handle_done_wins_when_worker_finishes_first() -> None:
    """If the worker has already finished (response fully read) when the watchdog
    fires, the watchdog must NOT shut down a socket that may have been reused.
    """
    handle = _PartHandle()
    handle.publish(object())  # a stand-in conn
    handle.finish()  # worker done first
    # Watchdog now tries to cancel — must be a no-op.
    conn = handle.cancel_if_active()
    assert conn is None
    assert handle.state == "done"


def test_handle_cancel_wins_when_still_in_flight() -> None:
    sentinel = object()
    handle = _PartHandle()
    handle.publish(sentinel)
    conn = handle.cancel_if_active()  # watchdog fires while still active
    assert conn is sentinel
    assert handle.state == "cancelled"
    # A late worker finish does not flip state back to done.
    handle.finish()
    assert handle.state == "cancelled"


def test_publish_after_cancel_is_ignored() -> None:
    handle = _PartHandle()
    handle.publish(object())
    handle.cancel_if_active()
    handle.publish(object())  # a urllib3-internal retry tries to publish a new conn
    # Already cancelled: no new conn is accepted.
    assert handle.state == "cancelled"


# --- per-part handle isolation across threads -----------------------------


def test_active_arming_is_thread_local() -> None:
    """Each concurrent part runs in its own pool thread and must see its OWN
    arming, never another part's (a global would cross the wires).
    """
    from hotdata._upload_watchdog import _Arming, _get_active_arming_for_test

    seen: Dict[int, object] = {}
    armings: Dict[int, _Arming] = {}
    barrier = threading.Barrier(3)
    wd = _Watchdog()

    def worker(i: int) -> None:
        a = _Arming(wd, deadline=100.0)
        armings[i] = a
        set_active_arming(a)
        barrier.wait()  # force all three to be set simultaneously
        seen[i] = _get_active_arming_for_test()
        set_active_arming(None)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    for i in range(3):
        assert seen[i] is armings[i]


# --- watchdog teardown (Codex #6) -----------------------------------------


def test_watchdog_thread_joins_on_shutdown() -> None:
    before = set(threading.enumerate())
    watchdog = _Watchdog()
    handle = _PartHandle()
    watchdog.arm(handle, deadline=100.0)  # never fires in the test
    watchdog.shutdown()  # must stop + join the thread
    after = set(threading.enumerate())
    leaked = [t for t in (after - before) if t.is_alive() and "watchdog" in t.name.lower()]
    assert not leaked


# --- ConnectionCls injection (Codex #2: HTTP and HTTPS) -------------------


def test_install_sets_both_http_and_https_connection_classes() -> None:
    from hotdata._upload_watchdog import (
        WatchdogHTTPConnection,
        WatchdogHTTPSConnection,
    )

    http_pool = urllib3.HTTPConnectionPool("127.0.0.1", 1)
    install_watchdog_connection_classes(http_pool)
    assert http_pool.ConnectionCls is WatchdogHTTPConnection

    https_pool = urllib3.HTTPSConnectionPool("127.0.0.1", 1)
    install_watchdog_connection_classes(https_pool)
    assert https_pool.ConnectionCls is WatchdogHTTPSConnection
