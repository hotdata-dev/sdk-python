"""Per-part stall cancellation for multipart storage uploads (Item 3).

A storage part ``PUT`` can *black-hole*: the TCP connection is established and
bytes are accepted into the kernel send buffer, then the far end stops reading
(a send-side stall) or never sends a response (a response-read stall). No RST
arrives, so neither a connect timeout nor urllib3's inactivity ``read`` timeout
reliably catches it, and the worker thread hangs forever — which, without this
module, would hang the whole upload (the outer re-sweep never gets to retry).

CPython cannot interrupt a thread blocked in a socket syscall from the outside,
but it *can* be woken by acting on the socket itself. This module reaches the
in-flight socket via a connection **subclass** injected into the storage pool —
keeping ``pool.urlopen`` (so urllib3 still owns request-target construction, body
framing, response adaptation and redirects) — and a watchdog thread that calls
``sock.shutdown(SHUT_RDWR)`` on a stalled connection. ``shutdown`` (NOT
``close``) is the spike-verified safe primitive: it wakes a blocked
``send``/``recv`` with a clean error and leaves the fd valid, so closing it stays
the owning request's job and there is no fd-reuse race.

Wiring (corrected per Codex diff review):

* The per-part **worker** stashes an :class:`_Arming` (the watchdog + the
  per-attempt deadline in seconds) in a **thread-local** before its
  ``pool.urlopen`` call, and clears it (disarming all handles) in ``finally``.
* :class:`WatchdogHTTPConnection` / :class:`WatchdogHTTPSConnection`, on EVERY
  ``request()`` (i.e. every urllib3 attempt — initial and internal retries) and
  on ``connect()``, create a FRESH :class:`_PartHandle`, publish their live
  ``.sock`` to it, and arm it on the watchdog with a fresh ``part_put_timeout``
  deadline — **before** the blocking ``super().request()`` send, so a reused
  keep-alive connection (which does not call ``connect()``) and a urllib3
  internal retry are both protected. This is the architect's per-ATTEMPT transfer
  budget; the spike's one-handle-per-urlopen was the simplification that left
  reused conns + internal retries unprotected.
* A terminal (non-retryable) failure cancels all in-flight handles immediately
  (:meth:`_Watchdog.cancel_all`) so fail-fast doesn't wait out a sibling's full
  per-part timeout.
"""

from __future__ import annotations

import logging
import socket
import threading
import time
from typing import Any, Dict, List, Optional

import urllib3
from urllib3.connection import HTTPConnection, HTTPSConnection

_log = logging.getLogger("hotdata.uploads")

#: Per-thread arming context for the part ``PUT`` currently running on this
#: thread. Each part runs in its own pool worker thread; the connection subclass
#: reads this to arm a fresh handle per attempt. A thread-local (never a global)
#: so concurrent parts never cross wires.
_active = threading.local()


class _Arming:
    """What a part's worker publishes for the connection subclass to use: the
    watchdog to arm handles on, the per-attempt deadline, and the set of handles
    armed so far for this part (so the worker can disarm them all afterward).
    """

    __slots__ = ("watchdog", "deadline", "current", "all")

    def __init__(self, watchdog: "_Watchdog", deadline: float) -> None:
        self.watchdog = watchdog
        self.deadline = deadline
        #: the handle for the attempt currently in flight (at most one — a handle
        #: is armed ONLY while its attempt exclusively owns its socket).
        self.current: Optional["_PartHandle"] = None
        #: every handle ever armed for this part (so the worker's finally can
        #: defensively disarm any straggler).
        self.all: List["_PartHandle"] = []


def set_active_arming(arming: Optional[_Arming]) -> None:
    """Set (or clear, with ``None``) the active arming for the current thread."""
    _active.arming = arming


def _current_arming() -> Optional[_Arming]:
    return getattr(_active, "arming", None)


def _arm_fresh_handle_for(conn: Any) -> None:
    """Connection-subclass hook (called per attempt, BEFORE the blocking send):
    disarm the PREVIOUS attempt's handle, then arm a FRESH one for ``conn``.

    Disarming the previous handle here is what frees a superseded connection
    (e.g. attempt-1 errored and urllib3 is retrying on a fresh conn) so a stale
    handle can never shut down a socket the pool has reissued (Codex #1).
    """
    arming = _current_arming()
    if arming is None:
        return
    _disarm_current(arming)
    handle = _PartHandle()
    handle.publish(conn)
    arming.current = handle
    arming.all.append(handle)
    arming.watchdog.arm(handle, arming.deadline)


def _disarm_current(arming: Optional[_Arming]) -> None:
    """Mark the current attempt's handle done and remove it from the watchdog —
    its socket is no longer exclusively owned by this attempt, so it must not be
    shut down. Called when superseding (new attempt) and after the response is
    obtained (conn about to return to the pool).
    """
    if arming is None or arming.current is None:
        return
    handle = arming.current
    arming.current = None
    handle.finish()
    arming.watchdog.disarm(handle)


def _disarm_active_handle() -> None:
    """Connection-subclass hook: called right after a response is obtained for
    the current attempt — the conn is about to be released to the pool, so its
    handle must be disarmed immediately (cross-part reuse safety, Codex #1).
    """
    _disarm_current(_current_arming())


def _abort_precheck() -> None:
    """Connection-subclass hook (called at the TOP of ``connect()`` and
    ``request()``): if this part's watchdog has already been terminally aborted,
    raise BEFORE opening/using a socket, so a part that begins after a terminal
    error fails fast instead of blocking in DNS/TCP/TLS establishment (Codex #5
    pre-connection gap). Sticky-abort's socket-shutdown only helps once a socket
    exists; on a fresh connection there is none yet, so we must refuse to proceed.

    Raised as a urllib3 ``ProtocolError`` — the SAME class the watchdog's
    ``shutdown`` produces — so ``_put_to_storage`` wraps it as a retryable
    ``StorageTransportError`` and it flows to the outer re-sweep / terminal path.
    """
    arming = _current_arming()
    if arming is not None and arming.watchdog.is_aborted():
        raise urllib3.exceptions.ProtocolError(
            "upload aborted before connection",
            ConnectionAbortedError("upload watchdog aborted"),
        )


def _get_active_arming_for_test() -> Optional[_Arming]:
    """Test hook: read the current thread's active arming."""
    return _current_arming()


class _PartHandle:
    """Tracks one connection for one part-``PUT`` *attempt* and arbitrates the
    race between the worker finishing and the watchdog firing.

    Exactly one of three states (Codex #9):

    * ``active``    — the attempt is in flight; the published ``conn`` may be
      shut down by the watchdog.
    * ``done``      — the worker finished (``urlopen`` returned or raised) before
      the watchdog fired; the watchdog must NOT touch the socket (the pool may
      reuse it).
    * ``cancelled`` — the watchdog shut the socket down first; a later worker
      ``finish`` does not flip it back.

    All transitions take ``lock`` so the worker's ``finish`` and the watchdog's
    ``cancel_if_active`` are serialized.
    """

    __slots__ = ("lock", "state", "conn")

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.state = "active"
        self.conn: Any = None

    def publish(self, conn: Any) -> None:
        with self.lock:
            if self.state == "active":
                self.conn = conn

    def finish(self) -> None:
        """Mark the attempt done. No-op if already cancelled."""
        with self.lock:
            if self.state == "active":
                self.state = "done"
            self.conn = None

    def cancel_if_active(self) -> Any:
        """Watchdog entry point: if still active, mark cancelled and return the
        connection to shut down; otherwise return ``None`` (worker won the race).
        """
        with self.lock:
            if self.state != "active":
                return None
            self.state = "cancelled"
            return self.conn


class WatchdogHTTPConnection(HTTPConnection):
    """An ``HTTPConnection`` that arms a fresh per-attempt watchdog handle on its
    live socket so a stalled ``PUT`` can be cancelled. Publishes BEFORE the
    blocking send (and on ``connect()``), so a reused keep-alive connection and a
    urllib3-internal retry are both covered.
    """

    def connect(self) -> None:
        _abort_precheck()  # refuse to open a socket if already aborted
        super().connect()
        _arm_fresh_handle_for(self)

    def request(self, *args: Any, **kwargs: Any) -> Any:
        # Fail fast if aborted BEFORE connecting/sending (no socket yet to shut
        # down on a fresh conn). Then arm BEFORE the (possibly blocking) send. A
        # reused conn skips connect(), so arming here protects a pooled send-stall.
        _abort_precheck()
        _arm_fresh_handle_for(self)
        return super().request(*args, **kwargs)

    def getresponse(self, *args: Any, **kwargs: Any) -> Any:
        # getresponse() blocks waiting for the response (a response-read stall is
        # caught here while the handle is still armed). Once it RETURNS, the conn
        # is about to be released to the pool — disarm so a stale handle can't
        # shut down a socket another part reuses.
        resp = super().getresponse(*args, **kwargs)
        _disarm_active_handle()
        return resp


class WatchdogHTTPSConnection(HTTPSConnection):
    """HTTPS counterpart of :class:`WatchdogHTTPConnection` (production storage
    is HTTPS). ``.sock`` is the TLS socket; ``shutdown`` wakes it the same way.
    """

    def connect(self) -> None:
        _abort_precheck()
        super().connect()
        _arm_fresh_handle_for(self)

    def request(self, *args: Any, **kwargs: Any) -> Any:
        _abort_precheck()
        _arm_fresh_handle_for(self)
        return super().request(*args, **kwargs)

    def getresponse(self, *args: Any, **kwargs: Any) -> Any:
        resp = super().getresponse(*args, **kwargs)
        _disarm_active_handle()
        return resp


def install_watchdog_connection_classes(pool: Any) -> None:
    """Wire the watchdog connection subclass onto ``pool``.

    Accepts a single ``HTTP(S)ConnectionPool`` (sets ``ConnectionCls``) or a
    :class:`~urllib3.PoolManager`. For a ``PoolManager`` (Codex #2: production
    uses one over HTTPS), this overrides per-scheme pool creation AND re-stamps
    any host pools already cached — so a pool created by an earlier single-PUT to
    the same origin still gets the watchdog subclass for a later multipart PUT.
    """
    if isinstance(pool, urllib3.HTTPSConnectionPool):
        pool.ConnectionCls = WatchdogHTTPSConnection
    elif isinstance(pool, urllib3.HTTPConnectionPool):
        pool.ConnectionCls = WatchdogHTTPConnection
    elif isinstance(pool, urllib3.PoolManager):
        _install_on_pool_manager(pool)
    else:
        # Not a real urllib3 pool (e.g. a test fake): nothing to hook. The
        # watchdog simply never engages — a fake doesn't stall — so this is a
        # safe no-op rather than an error.
        _log.debug(
            "watchdog connection class not installed on %s (not a urllib3 pool)",
            type(pool).__name__,
        )


def _install_on_pool_manager(manager: urllib3.PoolManager) -> None:
    """Stamp the watchdog ``ConnectionCls`` on a ``PoolManager``: future pools via
    a ``_new_pool`` override, AND any already-cached host pools (Codex #2 — a pool
    created before install must not keep the stock connection class).
    """
    if not getattr(manager, "_hotdata_watchdog_installed", False):
        original_new_pool = manager._new_pool

        def _new_pool(scheme: str, host: str, port: int, request_context: Any = None) -> Any:
            new_pool = original_new_pool(
                scheme, host, port, request_context=request_context
            )
            _stamp_pool(new_pool, scheme)
            return new_pool

        manager._new_pool = _new_pool  # type: ignore[method-assign]
        manager._hotdata_watchdog_installed = True  # type: ignore[attr-defined]

    # Re-stamp pools already created+cached before this install ran. urllib3's
    # `RecentlyUsedContainer` refuses `.values()`/iteration ("not threadsafe"),
    # so enumerate by key and fetch each pool via __getitem__ under its own lock.
    existing = getattr(manager, "pools", None)
    if existing is not None:
        try:
            keys = list(existing.keys())
        except Exception:  # pragma: no cover - container shape guard
            keys = []
        for key in keys:
            try:
                cached_pool = existing[key]
            except KeyError:  # evicted between keys() and lookup
                continue
            if cached_pool is None:
                continue
            scheme = "https" if isinstance(cached_pool, urllib3.HTTPSConnectionPool) else "http"
            _stamp_pool(cached_pool, scheme)


def _stamp_pool(pool: Any, scheme: str) -> None:
    pool.ConnectionCls = (
        WatchdogHTTPSConnection if scheme == "https" else WatchdogHTTPConnection
    )


class _Watchdog:
    """A single background thread that shuts down stalled part connections.

    One instance per multipart ``upload_file`` operation. Each in-flight attempt
    :meth:`arm`\\ s a handle with a wall-clock deadline; the thread sleeps until
    the nearest deadline, then for any past-deadline handle still ``active`` it
    ``shutdown``\\ s the socket (the fd is closed by the owning request, never
    here). A completed attempt :meth:`disarm`\\ s its handle immediately so the
    registry doesn't grow and dead entries don't cause spurious wakeups.

    :meth:`cancel_all` cancels every in-flight handle now (terminal-error
    fast-fail). :meth:`shutdown` stops and joins the thread.
    """

    def __init__(self, monotonic: Any = None) -> None:
        # Injectable clock so tests don't wait real seconds for a deadline.
        self._now = monotonic or time.monotonic
        self._cond = threading.Condition()
        #: handle -> fire_at deadline (monotonic). dict for O(1) disarm.
        self._entries: Dict[_PartHandle, float] = {}
        self._stop = False
        #: STICKY terminal-abort flag (Codex #5). Once set, ANY handle armed
        #: afterwards is cancelled immediately — so a sibling still inside
        #: upload_one (minting/reading) that arms its FIRST handle AFTER
        #: cancel_all()'s snapshot is still killed promptly, not waited out.
        self._aborted = False
        self._thread: Optional[threading.Thread] = None

    def arm(self, handle: _PartHandle, deadline: float) -> None:
        """Register ``handle`` to be cancelled at ``now + deadline``. If the
        watchdog has already been aborted (terminal error), cancel ``handle``
        immediately instead of waiting for its deadline.
        """
        with self._cond:
            if self._aborted:
                aborted = True
            else:
                aborted = False
                self._entries[handle] = self._now() + deadline
                if self._thread is None:
                    self._thread = threading.Thread(
                        target=self._run, name="hotdata-upload-watchdog", daemon=True
                    )
                    self._thread.start()
                self._cond.notify()
        if aborted:
            # Fire outside the lock (shutdown can block briefly).
            self._fire(handle)

    def disarm(self, handle: _PartHandle) -> None:
        """Remove a (completed) handle so it can't fire and doesn't linger."""
        with self._cond:
            self._entries.pop(handle, None)
            self._cond.notify()

    def is_aborted(self) -> bool:
        """Whether a terminal abort has fired (sticky). New attempts check this
        to refuse to open a connection after a terminal error."""
        with self._cond:
            return self._aborted

    def cancel_all(self) -> None:
        """Shut down every in-flight handle NOW and STICK the abort (Q-B / Codex
        #5), so a handle armed AFTER this call is also cancelled at once.

        Without the sticky flag a sibling still inside ``upload_one`` (minting /
        reading the chunk) that arms its first handle a moment later would be
        missed by the snapshot and waited out for its full per-part timeout.
        """
        with self._cond:
            self._aborted = True
            handles = list(self._entries.keys())
        for handle in handles:
            self._fire(handle)
        with self._cond:
            self._cond.notify()

    def _run(self) -> None:
        with self._cond:
            while not self._stop:
                now = self._now()
                due = [h for h, t in self._entries.items() if t <= now]
                for handle in due:
                    self._entries.pop(handle, None)
                if due:
                    # Fire OUTSIDE the lock (shutdown can block briefly), then
                    # loop again to recompute against any newly-armed entries —
                    # never wait on a stale deadline (Codex #3).
                    self._cond.release()
                    try:
                        for handle in due:
                            self._fire(handle)
                    finally:
                        self._cond.acquire()
                    continue
                if self._entries:
                    next_at = min(self._entries.values())
                    self._cond.wait(timeout=max(next_at - now, 0.0))
                else:
                    self._cond.wait()  # sleep until armed or stopped

    @staticmethod
    def _fire(handle: _PartHandle) -> None:
        conn = handle.cancel_if_active()
        if conn is None:
            return
        sock = getattr(conn, "sock", None)
        if sock is None:
            return
        try:
            sock.shutdown(socket.SHUT_RDWR)
            _log.debug("watchdog shut down a stalled storage connection")
        except OSError:
            # Already closed / not connected — the owning request surfaces its
            # own error.
            pass

    def shutdown(self) -> None:
        """Stop and join the watchdog thread. Idempotent. Raises if the thread
        fails to terminate (it should not, now that the scheduler can't wait on a
        stale deadline — Codex #3).
        """
        with self._cond:
            self._stop = True
            self._cond.notify()
        thread = self._thread
        if thread is not None:
            thread.join(timeout=5.0)
            if thread.is_alive():  # pragma: no cover - would signal a scheduler bug
                raise RuntimeError("upload watchdog thread did not terminate")
            self._thread = None


__all__ = [
    "WatchdogHTTPConnection",
    "WatchdogHTTPSConnection",
    "install_watchdog_connection_classes",
    "set_active_arming",
    "_Arming",
    "_PartHandle",
    "_Watchdog",
]
