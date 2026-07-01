"""Ergonomic, hand-written direct-to-storage (presigned) file uploads.

The auto-generated :class:`hotdata.api.uploads_api.UploadsApi` exposes the
presigned-upload flow only as raw building blocks. This module wraps it with a
thin subclass that orchestrates the whole flow transparently, so a caller
uploads a file with a single call:

1. ``POST /v1/uploads`` (:meth:`create_upload_session_handler`) opens a session
   and returns either a single ``url`` (``mode == "single"``) or a set of
   ``part_urls`` plus a ``part_size`` (``mode == "multipart"``), along with a
   one-time ``finalize_token``.
2. The client ``PUT`` s the bytes **directly to object storage** — never back
   through the API. Single uploads stream the whole file to ``url``; multipart
   uploads slice the file into ``part_size``-byte chunks and ``PUT`` each chunk
   to its ``part_urls[i - 1]``, collecting the storage ``ETag`` per part.
3. ``POST /v1/uploads/{upload_id}/finalize`` (:meth:`finalize_upload_handler`)
   confirms the upload with the finalize token in the ``X-Upload-Finalize-Token``
   header (empty object ``{}`` for single; the ascending ``{part_number, e_tag}``
   list for multipart) and returns a
   :class:`~hotdata.models.finalize_upload_response.FinalizeUploadResponse`.

Read ``upload_id`` from that response to load the upload into a managed table.

Storage PUT header isolation
----------------------------

A presigned storage URL already carries its authorization in the query string
(or in the server-provided ``headers`` map). Object stores (S3 and compatible)
reject a ``PUT`` carrying extra signed-ish headers with ``403
SignatureDoesNotMatch``, so storage ``PUT`` s go through a *dedicated, bare*
:class:`urllib3.PoolManager` that carries NONE of the SDK's bearer / workspace
headers — only an explicit ``Content-Length`` and whatever the server placed in
the session ``headers`` map (currently always empty). The SDK's own
``ApiClient`` (with its auth headers and proxy/TLS config) is deliberately not
reused for storage transfers.

This ``UploadsApi`` is a drop-in replacement for
:class:`hotdata.api.uploads_api.UploadsApi`; every generated method works
unchanged, and :meth:`UploadsApi.upload_file` adds the orchestrated flow.
"""

from __future__ import annotations

import copy
import io
import logging
import os
import threading
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, BinaryIO, Callable, Dict, Iterator, List, Optional, Tuple, Union

import urllib3
from urllib3.util.retry import Retry

from hotdata._retry import ConnectionResetRetry
from hotdata._upload_watchdog import (
    _Arming,
    _Watchdog,
    install_watchdog_connection_classes,
    set_active_arming,
)
from hotdata.api.uploads_api import UploadsApi as _GeneratedUploadsApi
from hotdata.api_client import ApiClient
from hotdata.exceptions import ApiException
from hotdata.models.create_upload_request import CreateUploadRequest
from hotdata.models.finalize_upload_part import FinalizeUploadPart
from hotdata.models.finalize_upload_request import FinalizeUploadRequest
from hotdata.models.finalize_upload_response import FinalizeUploadResponse
from hotdata.models.mint_upload_parts_request import MintUploadPartsRequest
from hotdata.models.upload_response import UploadResponse
from hotdata.models.upload_session_response import UploadSessionResponse
from hotdata.rest import RESTResponse

#: Response-type map for the legacy ``POST /v1/files`` op, mirroring the
#: generated ``upload_file`` handler.
_UPLOAD_FILE_RESPONSE_TYPES: Dict[str, Optional[str]] = {
    "201": "UploadResponse",
    "400": "ApiErrorResponse",
}

#: The accepted input types for :meth:`UploadsApi.upload_file`: a filesystem
#: path, raw bytes, or a seekable binary file object.
UploadSource = Union[str, "os.PathLike[str]", bytes, bytearray, BinaryIO]

_log = logging.getLogger("hotdata.uploads")

#: One mebibyte, the unit the storage part-size range is expressed in.
MIB = 1024 * 1024

#: Default cap on concurrent part ``PUT`` s when the caller doesn't set
#: ``max_concurrency``. Matches the boto3 / AWS CLI default of 10. The effective
#: in-flight count is the MIN of this and a memory budget (see
#: :func:`effective_in_flight`).
DEFAULT_MAX_CONCURRENCY = 10

#: Default part-size hint, in bytes (8 MiB), sent when the caller doesn't set
#: ``part_size``. The server clamps the hint to its own range and returns the
#: actual size. See :func:`auto_part_size_hint`.
DEFAULT_PART_SIZE = 8 * MIB

#: Target ceiling on part count when auto-scaling the part-size hint for very
#: large files, with headroom under S3's hard 10,000-part limit.
TARGET_MAX_PARTS = 9000

#: Minimum part size storage accepts (5 MiB). The hint is clamped to at least
#: this; the server enforces it too.
MIN_PART_SIZE = 5 * MIB

#: Maximum part size storage accepts (5 GiB). The hint is clamped to at most this.
MAX_PART_SIZE = 5 * 1024 * MIB

#: Target peak-memory budget for in-flight part buffers (256 MiB). Each in-flight
#: part buffers up to ``part_size`` bytes, so :func:`effective_in_flight` derives
#: the in-flight count as ``budget / part_size``. This is a TARGET, not a hard
#: ceiling: when the server returns a very large ``part_size`` a single in-flight
#: part may already exceed the budget, so it caps *concurrency*, not part size.
UPLOAD_MEMORY_BUDGET = 256 * MIB

#: The wire models sizes as a signed 64-bit integer. A declared size or part-size
#: hint beyond this is rejected up front rather than silently sent. Only reachable
#: for pathological sizes (~8 EiB), mirroring the Rust SDK's ``SizeOverflow``.
_MAX_WIRE_INT = 2**63 - 1

#: Progress callback: ``(bytes_done_total, total)``, where ``total`` is the full
#: declared file size. ``bytes_done_total`` is monotonically non-decreasing and
#: reaches exactly ``total`` when the transfer completes. For a multipart upload
#: it is invoked from worker threads, so a callback that touches shared state
#: must do its own locking.
UploadProgress = Callable[[int, int], None]


def auto_part_size_hint(declared_size: int) -> int:
    """Compute the part-size HINT to send in ``CreateUploadRequest.part_size``
    when the caller did not specify one.

    Starts from :data:`DEFAULT_PART_SIZE` (8 MiB) and grows only for files large
    enough that 8 MiB parts would exceed :data:`TARGET_MAX_PARTS` — so the common
    case is unchanged and only very large files (beyond ~72 GiB) get a larger
    hint to keep the part count bounded. The result is rounded UP to a whole MiB
    and clamped to ``[MIN_PART_SIZE, MAX_PART_SIZE]``. The server still has the
    final say and clamps to its own range. Pure and total:
    ``declared_size == 0`` yields :data:`DEFAULT_PART_SIZE`.
    """
    # Smallest part size that keeps the count at or under the target.
    by_count = -(-declared_size // TARGET_MAX_PARTS)  # ceil division
    raw = max(DEFAULT_PART_SIZE, by_count)
    # Round up to a whole MiB so the hint is a clean multiple.
    rounded = -(-raw // MIB) * MIB
    return max(MIN_PART_SIZE, min(rounded, MAX_PART_SIZE))


def effective_in_flight(max_concurrency: int, part_size: int) -> int:
    """Compute how many part ``PUT`` s to keep in flight, given the caller's
    ``max_concurrency`` and the SERVER's actual returned ``part_size``.

    Peak buffered memory is ``in_flight * part_size``, so in-flight is capped at
    ``UPLOAD_MEMORY_BUDGET / part_size``, then at ``max_concurrency``. Normal
    8 MiB parts give ``256/8 = 32``, capped to ``max_concurrency``; a 64 MiB part
    gives ``4``. ``max_concurrency`` is honored as an explicit floor: a caller
    asking for ``1`` (or ``0``) gets serial uploads (``1``). The result is always
    ``>= 1``. Pure and total: a zero ``part_size`` is treated as 1.
    """
    cap = max(max_concurrency, 1)
    by_budget = max(UPLOAD_MEMORY_BUDGET // max(part_size, 1), 1)
    return min(by_budget, cap)


@dataclass
class UploadOptions:
    """Options for :meth:`UploadsApi.upload_file`.

    All fields are optional. ``content_type`` / ``content_encoding`` /
    ``filename`` are recorded with the upload (advisory metadata; they do not
    change where the bytes are stored). ``part_size`` is a hint the server clamps
    to its allowed range and ignores for single-``PUT`` uploads. ``progress``,
    when set, is invoked as bytes flow.
    """

    #: Content type to record for the uploaded file (e.g. a Parquet/CSV/JSON MIME
    #: type). Advisory.
    content_type: Optional[str] = None
    #: Content encoding to record for the uploaded file (e.g. ``gzip``).
    content_encoding: Optional[str] = None
    #: Original file name, recorded for bookkeeping. Defaults to the source
    #: path's file name when not set.
    filename: Optional[str] = None
    #: Preferred part size, in bytes, for a large (multipart) upload. A hint the
    #: server clamps; ignored for single-``PUT`` uploads. When unset, the SDK
    #: auto-scales a hint via :func:`auto_part_size_hint`.
    part_size: Optional[int] = None
    #: Maximum number of part ``PUT`` s to keep in flight for a multipart upload.
    #: ``None`` uses :data:`DEFAULT_MAX_CONCURRENCY`. The effective in-flight
    #: count is the MIN of this and a peak-memory budget (see
    #: :func:`effective_in_flight`).
    max_concurrency: Optional[int] = None
    #: Optional progress callback invoked with ``(bytes_done_total, total)``.
    progress: Optional[UploadProgress] = None
    #: ``urllib3`` retry policy for part ``PUT`` s — the INNER retry tier (429 +
    #: pre-response reset; 5xx propagates to the whole-upload re-sweep). ``None``
    #: uses :func:`default_part_retry`. A custom policy that puts ``5xx`` back in
    #: its ``status_forcelist`` shifts the tier boundary. The single-``PUT``
    #: small-file path streams an un-replayable body and is always sent without
    #: retry regardless.
    part_retry: Optional[Retry] = None
    #: Extra whole-upload re-sweep rounds beyond the initial pass (Item 1).
    #: ``None`` uses :data:`DEFAULT_MAX_EXTRA_ROUNDS` (3). ``0`` disables the
    #: re-sweep (a single failure sinks the upload — the legacy behavior).
    max_extra_rounds: Optional[int] = None
    #: Base delay (seconds) for the capped-exponential backoff between re-sweep
    #: rounds. ``None`` uses :data:`DEFAULT_ROUND_BASE_DELAY` (2s). Set to ``0``
    #: in tests for instant rounds.
    round_base_delay: Optional[float] = None


# --- Errors ---------------------------------------------------------------


class UploadError(Exception):
    """Base class for errors raised by :meth:`UploadsApi.upload_file` while
    driving the direct-to-storage flow.

    Opening the session or finalizing fails with the generated client's
    :class:`~hotdata.exceptions.ApiException` instead (e.g. a ``501``
    ``PRESIGN_UNSUPPORTED`` when the storage backend cannot issue upload URLs);
    only the storage transfer and session-consistency failures raise
    ``UploadError`` subclasses.
    """


class MalformedSessionError(UploadError):
    """The create-session response was internally inconsistent for its declared
    ``mode`` (e.g. ``single`` without a ``url``, ``multipart`` without
    ``part_urls`` / ``part_size``, or a ``part_urls`` count that does not match
    how the file slices into parts).
    """


class SizeLimitError(UploadError):
    """A size (the file's declared size, or the part-size hint) does not fit the
    wire's signed 64-bit field. Only reachable for pathological sizes beyond
    ~8 EiB.
    """

    def __init__(self, *, what: str, value: int) -> None:
        self.what = what
        self.value = value
        super().__init__(f"{what} ({value} bytes) exceeds the maximum supported size")


class StorageTransportError(UploadError):
    """A storage ``PUT`` failed at the transport layer (connection refused,
    reset, TLS error, DNS failure, or retries exhausted) before any HTTP status
    was returned. The underlying ``urllib3`` error is the exception ``__cause__``.

    Distinct from :class:`StorageError`, which is a completed request that
    returned a non-2xx HTTP status.
    """

    def __init__(self, *, url: str, part_number: Optional[int]) -> None:
        self.url = url
        self.part_number = part_number
        if part_number is None:
            msg = "the upload transfer to storage failed before any response"
        else:
            msg = f"the transfer of part {part_number} to storage failed before any response"
        super().__init__(msg)


class StorageError(UploadError):
    """A storage ``PUT`` returned a non-2xx status.

    Carries the HTTP ``status`` and the response ``body`` (often XML for S3-style
    errors), plus the 1-based ``part_number`` for a multipart ``PUT`` (``None``
    for the single-``PUT`` path).
    """

    def __init__(self, *, status: int, part_number: Optional[int], body: str) -> None:
        self.status = status
        self.part_number = part_number
        self.body = body
        if part_number is None:
            msg = f"storage rejected the upload with status {status}: {body}"
        else:
            msg = f"storage rejected part {part_number} with status {status}: {body}"
        super().__init__(msg)


class MissingETagError(UploadError):
    """Storage accepted a part ``PUT`` but returned no usable ``ETag`` header
    (absent, or empty/whitespace-only), so the part cannot be finalized.

    Retryable (not terminal): a momentary backend hiccup that drops the header
    shouldn't be permanent, so the re-sweep re-``PUT`` s to pick up a real ETag.
    """

    def __init__(self, *, part_number: int) -> None:
        self.part_number = part_number
        super().__init__(
            f"storage returned no ETag for part {part_number}; cannot finalize"
        )


# --- Error classification (Item 2) ----------------------------------------


def _is_retryable(exc: BaseException) -> bool:
    """Whether the outer whole-upload re-sweep should retry a per-part failure.

    A deliberate **allowlist** of genuinely-transient transport / storage / mint
    conditions — each curable by a later round at lower concurrency (and, for a
    fresh minted URL, by re-minting). Everything NOT listed is non-retryable and
    fails the upload fast: a deterministic local short-read (a generic
    :class:`UploadError`), a contract/sizing violation
    (:class:`MalformedSessionError`, :class:`SizeLimitError`), a progress-callback
    exception (raised *after* a successful ``PUT`` — re-running would duplicate the
    write), or anything unexpected. Retrying those would burn the round budget for
    nothing or, worse, double-``PUT``.
    """
    if isinstance(exc, (StorageTransportError, MissingETagError)):
        return True
    if isinstance(exc, StorageError):
        return True  # incl. 5xx (outer tier owns it) and 403 (eager URL expiry)
    if isinstance(exc, ApiException):
        return True  # a per-part mint round-trip failure — a re-mint may cure it
    return False


def _parse_etag(headers: Any, part_number: int) -> str:
    """Extract a real, non-empty ``ETag`` from a part ``PUT`` response (Item 7).

    A missing header OR an empty / whitespace-only value is rejected as
    :class:`MissingETagError` (retryable). Otherwise the value is returned
    verbatim, quotes included — finalize must carry exactly what storage gave.
    """
    etag = headers.get("ETag")
    if etag is None or not str(etag).strip():
        raise MissingETagError(part_number=part_number)
    return etag


# --- Whole-upload re-sweep (Item 1) ---------------------------------------

#: Outer-tier (whole-upload re-sweep) defaults, mirroring the Rust SDK. Round 0
#: is the initial full pass; up to :data:`DEFAULT_MAX_EXTRA_ROUNDS` re-sweeps
#: follow, each re-running only the parts still failing, at halving concurrency.
DEFAULT_MAX_EXTRA_ROUNDS = 3
#: Capped-exponential backoff before re-sweep round N: ``base * 2**(N-1)``.
DEFAULT_ROUND_BASE_DELAY = 2.0
#: Clamp on the round-delay shift so it can't overflow.
_ROUND_DELAY_SHIFT_CAP = 16


@dataclass
class _PartPlan:
    """One part's work unit, keyed by its 1-based ``part_number``. Byte range is
    derived from the part number (``offset = index * part_size``), never from
    arrival/queue position, so a reordered mint response can't shift offsets
    (Item 6).
    """

    index: int          # 0-based position
    part_number: int    # 1-based
    offset: int
    length: int


def _round_in_flight(base: int, round_idx: int) -> int:
    """In-flight cap for re-sweep round ``round_idx``: halve each round, floor 1
    (``max(base >> round, 1)``). 8 → 8,4,2,1,1,…  A saturated jittery uplink
    resets fewer connections when fewer are in flight, so lowering concurrency
    each round directly targets that failure mode.
    """
    if round_idx >= base.bit_length():
        return 1
    return max(base >> round_idx, 1)


def _round_delay(round_idx: int, base_delay: float = DEFAULT_ROUND_BASE_DELAY) -> float:
    """Capped-exponential backoff before round ``round_idx`` (>=1):
    ``base_delay * 2**(round_idx - 1)``, shift clamped so it can't overflow.
    """
    shift = min(round_idx - 1, _ROUND_DELAY_SHIFT_CAP)
    return base_delay * (2 ** shift)


def _upload_parts_resilient(
    plans: List[_PartPlan],
    upload_one: Callable[[_PartPlan], FinalizeUploadPart],
    *,
    base_in_flight: int,
    max_extra_rounds: int = DEFAULT_MAX_EXTRA_ROUNDS,
    round_base_delay: float = DEFAULT_ROUND_BASE_DELAY,
    on_part_done: Optional[Callable[[_PartPlan], None]] = None,
    on_terminal: Optional[Callable[[], None]] = None,
    sleep: Callable[[float], None] = time.sleep,
) -> List[FinalizeUploadPart]:
    """Run every part's ``upload_one`` work unit with whole-upload re-sweep.

    Round 0 is the initial full pass at ``base_in_flight`` concurrency. Each
    subsequent round (up to ``max_extra_rounds``) waits a capped-exponential
    backoff, halves concurrency, and re-runs ONLY the parts that failed the
    previous round with a *retryable* error; completed parts keep their ETags.

    Invariants: every healthy part is attempted exactly once; a part failing K
    rounds is attempted ``K+1`` times (capped); a **terminal** (non-retryable,
    see :func:`_is_retryable`) error fails fast — the round stops dispatching new
    parts and the error is raised after in-flight workers drain. If parts still
    fail after the last round, the last underlying retryable error is raised
    (its cause preserved). A part slot that is never filled is a hard
    :class:`MalformedSessionError` — finalize never gets a silently-short list.

    ``on_part_done`` is invoked once per successfully-completed part (used for
    exactly-once progress): a re-swept part that failed earlier rounds did not
    fire it, so bytes are never double-counted.
    """
    results: Dict[int, FinalizeUploadPart] = {}
    counted: set = set()
    lock = threading.Lock()
    pending = list(plans)

    last_error: Optional[BaseException] = None

    for round_idx in range(0, 1 + max_extra_rounds):
        if not pending:
            break
        if round_idx > 0:
            sleep(_round_delay(round_idx, round_base_delay))
        in_flight = _round_in_flight(base_in_flight, round_idx)
        failures: Dict[int, BaseException] = {}
        terminal: List[BaseException] = []
        stop = threading.Event()

        def _fail_terminal(exc: BaseException) -> None:
            with lock:
                terminal.append(exc)
            stop.set()
            # Actively cancel in-flight siblings (terminal fast-fail, Q-B) so the
            # round-boundary join doesn't wait out a stalled sibling's full
            # per-part timeout. No-op if the caller wired no canceller.
            if on_terminal is not None:
                on_terminal()

        def run_one(plan: _PartPlan) -> None:
            if stop.is_set():
                # A terminal error elsewhere in the round: don't dispatch new work.
                failures[plan.part_number] = _NotDispatched()
                return
            try:
                part = upload_one(plan)
            except BaseException as exc:  # noqa: BLE001 - classified below
                if not _is_retryable(exc):
                    _fail_terminal(exc)
                    return
                with lock:
                    failures[plan.part_number] = exc
                return
            if part is None:
                with lock:
                    failures[plan.part_number] = MalformedSessionError(
                        f"part {plan.part_number} was never uploaded"
                    )
                return
            # Record success first, then fire the progress callback. A callback
            # exception is NOT a transport failure and the PUT already succeeded —
            # re-running would duplicate the write — so it is TERMINAL (abort the
            # upload, do not finalize), never retried (Codex #4).
            with lock:
                results[plan.part_number] = part
                fire = on_part_done is not None and plan.part_number not in counted
                if fire:
                    counted.add(plan.part_number)
            if fire:
                try:
                    on_part_done(plan)
                except BaseException as exc:  # noqa: BLE001 - callback bug → abort
                    _fail_terminal(exc)

        executor = ThreadPoolExecutor(max_workers=in_flight)
        try:
            # Bounded-wave dispatch: never submit more than `in_flight` at once,
            # so the per-round cap actually bounds concurrency AND a terminal
            # error stops not-yet-started parts from being dispatched.
            it = iter(pending)
            futures: set = set()
            for plan in _take(it, in_flight):
                futures.add(executor.submit(run_one, plan))
            while futures:
                done, futures = _wait_first(futures)
                # Surface any unexpected exception that escaped run_one (it should
                # classify everything itself; this is defense-in-depth so a future
                # exception can never be silently swallowed).
                for fut in done:
                    exc = fut.exception()
                    if exc is not None:
                        _fail_terminal(exc)
                for plan in _take(it, len(done)):
                    if stop.is_set():
                        break
                    futures.add(executor.submit(run_one, plan))
        finally:
            # Round-boundary join: by the time this returns, no worker from this
            # round is still touching the source / firing progress. The watchdog
            # (Item 3) makes a stalled worker terminable so this stays bounded.
            executor.shutdown(wait=True)

        if terminal:
            raise terminal[0]

        # Track the most recent real failure to surface on exhaustion.
        for exc in failures.values():
            if not isinstance(exc, _NotDispatched):
                last_error = exc
        pending = [p for p in pending if p.part_number in failures]

    if pending:
        # Exhausted the round budget with parts still failing: surface the last
        # underlying error so the caller's normal mapping applies.
        if last_error is not None:
            raise last_error
        raise StorageTransportError(url="", part_number=pending[0].part_number)

    # Completeness: every plan's slot must be filled.
    missing = [p.part_number for p in plans if p.part_number not in results]
    if missing:
        raise MalformedSessionError(f"part {missing[0]} was never uploaded")

    return [results[pn] for pn in sorted(results)]


class _NotDispatched(Exception):
    """Sentinel failure for a part skipped because the round was aborting on a
    terminal error; it is re-queued but never surfaced as the cause.
    """


def _take(it: Iterator[_PartPlan], n: int) -> List[_PartPlan]:
    out: List[_PartPlan] = []
    for _ in range(n):
        try:
            out.append(next(it))
        except StopIteration:
            break
    return out


def _wait_first(futures: set) -> Tuple[set, set]:
    """Block until at least one future completes; return ``(done, still_running)``."""
    done, not_done = wait(futures, return_when=FIRST_COMPLETED)
    return done, not_done


# --- Storage transport ----------------------------------------------------

# A dedicated, process-wide, *bare* pool for storage PUTs. Deliberately NOT the
# SDK's ApiClient pool: a host app may have installed auth / workspace headers
# there, which storage would reject. Built lazily and reused. No request
# timeout: a large upload legitimately takes minutes.
_STORAGE_POOL: Optional[urllib3.PoolManager] = None
_STORAGE_POOL_LOCK = threading.Lock()


def _storage_pool() -> urllib3.PoolManager:
    global _STORAGE_POOL
    if _STORAGE_POOL is None:
        with _STORAGE_POOL_LOCK:
            if _STORAGE_POOL is None:
                pool = urllib3.PoolManager()
                # Install the stall-cancellation connection subclass at creation
                # time — BEFORE any request can populate `manager.pools` with a
                # host pool carrying the stock connection class (Codex #2). The
                # single-PUT path uses this same pool, so an early single-PUT must
                # not leave an un-hooked cached pool for a later multipart PUT.
                install_watchdog_connection_classes(pool)
                _STORAGE_POOL = pool
    return _STORAGE_POOL


#: Per-part transfer-timeout shape (Item 3). A part ``PUT`` attempt is killed (into
#: the outer re-sweep) only if it cannot sustain even ``PART_TIMEOUT_MIN_BYTES_PER_SEC``
#: — a true stall, never a slow-but-progressing transfer. Size-scaled so a large
#: part legitimately gets longer, capped so a stalled giant part can't hang for hours.
PART_TIMEOUT_BASE = 60.0
PART_TIMEOUT_MIN_BYTES_PER_SEC = 64 * 1024
PART_TIMEOUT_MAX = 30 * 60.0

#: Per-sleep cap for the inner part retry's *exponential* backoff path.
PART_RETRY_BACKOFF_MAX = 120.0

#: Cap on a server-sent ``Retry-After`` for a part ``PUT`` (the per-part
#: retry-window deadline analog). ``backoff_max`` only bounds the exponential
#: backoff path; urllib3 honors ``Retry-After`` UNCAPPED. A multi-minute storage
#: ``Retry-After`` would stall the whole-upload re-sweep's round-boundary join, so
#: :class:`_RetryAfterCappedRetry` clamps it. Flat 120s, independent of part size
#: — NOT tied to :func:`_part_put_timeout` (the per-attempt transfer budget, up to
#: 30 min): tying the sleep cap to that would let a big part honor a 30-min
#: ``Retry-After`` and reintroduce the stall.
MAX_RETRY_AFTER_SECONDS = 120.0


class _RetryAfterCappedRetry(ConnectionResetRetry):
    """A part-pool retry that caps a server ``Retry-After`` at
    :data:`MAX_RETRY_AFTER_SECONDS`.

    Overriding ``get_retry_after`` (NOT ``sleep`` / ``sleep_for_retry``, whose
    shape changed across urllib3 1.26→2.x) is forward-compatible: it returns
    seconds in both versions, and ``Retry.sleep`` consults it. ``None`` (no
    ``Retry-After`` header) passes through untouched so the exponential backoff
    path is unaffected.
    """

    def get_retry_after(self, response: Any) -> Any:
        retry_after = super().get_retry_after(response)
        if retry_after is None:
            return None
        return min(retry_after, MAX_RETRY_AFTER_SECONDS)

#: Inactivity (connect, read) timeout for the per-part mint call (Item 4 / Codex #5).
#: NOTE: this is an INACTIVITY timeout, not a strict wall-clock bound — a slow-trickle
#: mint response could in principle evade it (same urllib3 limitation as a read
#: timeout). It bounds a mint *in practice* so a stalled mint can't hang the
#: round-boundary join; it is not a hard wall-clock guarantee. A mint trickle-stall
#: is far rarer than a storage one, so a mint watchdog is deliberately not built.
MINT_TIMEOUT = (10.0, 30.0)


def _part_put_timeout(content_length: int) -> float:
    """The size-scaled per-attempt transfer cap for one part ``PUT`` (Item 3).

    ``min(BASE + content_length / MIN_BYTES_PER_SEC, MAX)``: 8 MiB → 188s, 64 MiB
    → ~18 min, ≥ ~111 MiB → the 30-min cap, 0 bytes → the 60s base. This is the
    ONLY bound on a single in-flight PUT; the watchdog enforces it by shutting the
    socket down. Pure and total.
    """
    return min(
        PART_TIMEOUT_BASE + content_length / PART_TIMEOUT_MIN_BYTES_PER_SEC,
        PART_TIMEOUT_MAX,
    )


def default_part_retry() -> Retry:
    """The default INNER retry policy for multipart part ``PUT`` s (Item 5).

    A part ``PUT`` is idempotent — storage overwrites a part by number — so a
    retried part cannot corrupt the upload. This is the *inner* tier of the
    two-tier model: it retries genuinely-momentary conditions in place —

    * HTTP ``429`` admission-shedding, honoring ``Retry-After``;
    * pre-response connection resets on any method (via the
      :class:`~hotdata._retry.ConnectionResetRetry` base), which includes the
      watchdog's ``ProtocolError(RemoteDisconnected)`` when a stalled part is
      cancelled (Item 3) — so a watchdog-cancelled part is re-attempted.

    Storage ``5xx`` is deliberately **excluded** from ``status_forcelist`` so it
    is NOT inner-retried; it propagates to the whole-upload re-sweep (the outer
    tier), which owns its recovery with reduced concurrency. Redirects are not
    followed: a ``3xx`` on a presigned ``PUT`` would re-issue to a different URL
    and invalidate the signature, so it surfaces as an error instead.

    ``backoff_max`` caps a pathological ``Retry-After`` so the re-sweep's
    round-boundary join can't stall on an unbounded sleep.

    Override per upload via :attr:`UploadOptions.part_retry`; a custom policy that
    puts ``5xx`` back in its ``status_forcelist`` shifts the tier boundary (the
    caller's explicit choice).
    """
    kwargs: Dict[str, Any] = dict(
        total=3,
        backoff_factor=0.2,
        status_forcelist=(429,),
        allowed_methods=frozenset({"PUT"}),
        raise_on_status=False,
        respect_retry_after_header=True,
        redirect=False,
    )
    # urllib3 >= 2 takes backoff_max as a constructor arg; 1.26 only honors the
    # instance/class attribute `DEFAULT_BACKOFF_MAX` (which `get_backoff_time`
    # reads — NOT the deprecated `BACKOFF_MAX` alias). Set it the version-portable
    # way so the per-sleep cap is explicit regardless of urllib3 version.
    try:
        return _RetryAfterCappedRetry(backoff_max=PART_RETRY_BACKOFF_MAX, **kwargs)
    except TypeError:
        retry = _RetryAfterCappedRetry(**kwargs)
        retry.DEFAULT_BACKOFF_MAX = PART_RETRY_BACKOFF_MAX  # type: ignore[attr-defined]
        return retry


def _to_timeout(request_timeout: Any) -> Any:
    """Convert the SDK's ``_request_timeout`` (a number or ``(connect, read)``
    tuple) into a :class:`urllib3.Timeout`, or ``None`` for the pool default —
    matching the generated REST client's conversion.
    """
    if not request_timeout:
        return None
    if isinstance(request_timeout, (int, float)):
        return urllib3.Timeout(total=request_timeout)
    if isinstance(request_timeout, tuple) and len(request_timeout) == 2:
        return urllib3.Timeout(connect=request_timeout[0], read=request_timeout[1])
    return None


def _storage_headers(session_headers: Dict[str, str], content_length: int) -> Dict[str, str]:
    """Build the bare PUT headers: an explicit ``Content-Length`` plus the
    server-provided session headers replayed verbatim (currently always empty;
    the only place a ``Content-Type`` may legitimately be set).
    """
    headers = {"Content-Length": str(content_length)}
    headers.update(session_headers)
    return headers


def _put_to_storage(
    url: str,
    body: Any,
    headers: Dict[str, str],
    retries: Any,
    part_number: Optional[int],
) -> Any:
    """``PUT`` ``body`` to a presigned storage ``url`` on the bare, header-isolated
    pool, returning the response. Wraps a transport failure as
    :class:`StorageTransportError` and a non-2xx status as :class:`StorageError`.
    """
    _log.debug("storage PUT %s (content-length=%s)", url, headers.get("Content-Length"))
    try:
        response = _storage_pool().request(
            "PUT", url, body=body, headers=headers, retries=retries
        )
    except urllib3.exceptions.HTTPError as exc:
        raise StorageTransportError(url=url, part_number=part_number) from exc
    status = int(response.status)
    _log.debug("storage PUT %s -> %s", url, status)
    # Any non-2xx is an error, INCLUDING a 3xx (Codex #6): with redirects disabled
    # on the part pool, urllib3 returns the 3xx response rather than following it,
    # and following a redirect on a presigned PUT would re-issue to a different URL
    # and invalidate the signature. So a storage 3xx surfaces as StorageError, not
    # a silent success.
    if not 200 <= status < 300:
        data = getattr(response, "data", b"") or b""
        if isinstance(data, (bytes, bytearray)):
            error_body = bytes(data).decode("utf-8", errors="replace")
        else:
            error_body = str(data)
        raise StorageError(status=status, part_number=part_number, body=error_body)
    return response


class _ProgressReader(io.RawIOBase):
    """Wrap a binary file object so each read advances a byte counter and
    invokes the progress callback. Used for the single-``PUT`` path so progress
    is byte-granular rather than jumping 0% -> 100%. Monotonic non-decreasing;
    the running total never exceeds ``total``.

    A :class:`io.RawIOBase` so it satisfies the file-like body type that
    ``urllib3`` ``PUT`` s; ``http.client`` reads it in blocks via
    :meth:`readinto`, which is where progress is reported.
    """

    def __init__(
        self,
        fileobj: BinaryIO,
        total: int,
        progress: Optional[UploadProgress],
    ) -> None:
        super().__init__()
        self._file = fileobj
        self._total = total
        self._progress = progress
        self._done = 0

    @property
    def bytes_read(self) -> int:
        """Total bytes actually pulled from the source so far."""
        return self._done

    def readable(self) -> bool:
        return True

    def readinto(self, b: Any) -> int:
        # Never read past the declared size: a source longer than `total` (a
        # growing file, or a wrong explicit `size`) must not spill extra bytes
        # past `Content-Length` and corrupt the pooled connection.
        remaining = self._total - self._done
        if remaining <= 0:
            return 0
        chunk = self._file.read(min(len(b), remaining))
        if not chunk:
            return 0
        n = len(chunk)
        b[:n] = chunk
        self._done += n
        if self._progress is not None:
            self._progress(self._done, self._total)
        return n


class UploadsApi(_GeneratedUploadsApi):
    """Drop-in replacement for :class:`hotdata.api.uploads_api.UploadsApi` that
    adds :meth:`upload_file`, an orchestrated direct-to-storage upload. All
    base-class methods work unchanged.
    """

    def upload_file(  # type: ignore[override]
        self,
        source: UploadSource,
        *,
        size: Optional[int] = None,
        content_type: Optional[str] = None,
        content_encoding: Optional[str] = None,
        filename: Optional[str] = None,
        part_size: Optional[int] = None,
        max_concurrency: Optional[int] = None,
        progress: Optional[UploadProgress] = None,
        part_retry: Optional[Retry] = None,
        max_extra_rounds: Optional[int] = None,
        round_base_delay: Optional[float] = None,
        options: Optional[UploadOptions] = None,
        _request_timeout: Any = None,
    ) -> FinalizeUploadResponse:
        """Upload a file directly to object storage and finalize it.

        Opens an upload session, ``PUT`` s the bytes straight to storage (one
        ``PUT`` for a small file, concurrent part ``PUT`` s for a large one),
        then finalizes and returns the
        :class:`~hotdata.models.finalize_upload_response.FinalizeUploadResponse`.
        Read ``upload_id`` from it to load the upload into a managed table. The
        bytes never round-trip through the API.

        ``source`` may be a filesystem path, raw ``bytes`` / ``bytearray``, or a
        seekable binary file object. A non-seekable stream is not accepted here
        (multipart needs positioned reads) — use :meth:`upload_stream` for that.
        A file object is uploaded from its current position to the end (its
        cursor is consumed, not restored); pass ``size`` only if its length
        cannot be inferred by seeking.

        Per-call keyword arguments override the matching :class:`UploadOptions`
        field when both are given.

        :param source: A path, ``bytes``, or seekable binary file object.
        :param size: Byte size of ``source`` when it is a file object whose size
            cannot be determined (otherwise inferred from the path/bytes/seek).
        :param content_type: Content type to record (advisory).
        :param content_encoding: Content encoding to record (advisory).
        :param filename: Original file name to record; defaults to the path's
            base name (no default for bytes / file-object sources).
        :param part_size: Preferred multipart part-size hint, in bytes; the
            server clamps it and ignores it for single-``PUT`` uploads.
        :param max_concurrency: Max in-flight part ``PUT`` s for a multipart
            upload (default :data:`DEFAULT_MAX_CONCURRENCY`, further bounded by a
            peak-memory budget).
        :param progress: Callback invoked with ``(bytes_done_total, total)``.
        :param part_retry: ``urllib3`` retry policy for multipart part ``PUT`` s;
            defaults to :func:`default_part_retry`.
        :param options: An :class:`UploadOptions` bundle; individual keyword
            arguments take precedence over its fields.
        :raises SizeLimitError: the file is larger than the wire's 64-bit field.
        :raises MalformedSessionError: the session response was inconsistent.
        :raises StorageError: a storage ``PUT`` returned a non-2xx status.
        :raises StorageTransportError: a storage ``PUT`` failed before any
            response (connection/TLS/DNS error, or retries exhausted).
        :raises MissingETagError: a part ``PUT`` returned no ``ETag``.
        :raises OSError: the local file could not be opened or read.
        :raises hotdata.exceptions.ApiException: opening the session or
            finalizing failed (e.g. ``501`` ``PRESIGN_UNSUPPORTED`` — the storage
            backend cannot issue upload URLs; use ``POST /v1/files`` instead).
        """
        opts = options or UploadOptions()
        content_type = content_type if content_type is not None else opts.content_type
        content_encoding = (
            content_encoding if content_encoding is not None else opts.content_encoding
        )
        filename = filename if filename is not None else opts.filename
        part_size = part_size if part_size is not None else opts.part_size
        max_concurrency = (
            max_concurrency if max_concurrency is not None else opts.max_concurrency
        )
        progress = progress if progress is not None else opts.progress
        part_retry = part_retry if part_retry is not None else opts.part_retry
        max_extra_rounds = (
            max_extra_rounds if max_extra_rounds is not None else opts.max_extra_rounds
        )
        round_base_delay = (
            round_base_delay if round_base_delay is not None else opts.round_base_delay
        )

        src = _make_source(source, size)
        total = src.size
        if filename is None and isinstance(src, _PathSource):
            filename = src.default_filename

        # Part-size hint: honor an explicit value, else auto-scale from the
        # declared size. The server clamps it regardless.
        part_size_hint = part_size if part_size is not None else auto_part_size_hint(total)

        # The wire models sizes as a signed i64; reject a pathological size up
        # front rather than silently sending an out-of-range value.
        if total > _MAX_WIRE_INT:
            raise SizeLimitError(what="declared_size_bytes", value=total)
        if part_size_hint > _MAX_WIRE_INT:
            raise SizeLimitError(what="part_size", value=part_size_hint)

        session = self.create_upload_session_handler(
            CreateUploadRequest(
                content_type=content_type,
                content_encoding=content_encoding,
                filename=filename,
                declared_size_bytes=total,
                part_size=part_size_hint,
            ),
            _request_timeout=_request_timeout,
        )

        # Report initial progress so a 0-byte file (or an instant single PUT)
        # still emits a terminal tick.
        if progress is not None:
            progress(0, total)

        if session.mode == "single":
            self._upload_single(session, src, total, progress)
            parts: Optional[List[FinalizeUploadPart]] = None
        elif session.mode == "multipart":
            cap = max_concurrency if max_concurrency is not None else DEFAULT_MAX_CONCURRENCY
            retry = part_retry if part_retry is not None else default_part_retry()
            parts = self._upload_multipart(
                session,
                src,
                total,
                cap,
                retry,
                progress,
                max_extra_rounds=(
                    max_extra_rounds if max_extra_rounds is not None
                    else DEFAULT_MAX_EXTRA_ROUNDS
                ),
                round_base_delay=(
                    round_base_delay if round_base_delay is not None
                    else DEFAULT_ROUND_BASE_DELAY
                ),
            )
        else:
            raise MalformedSessionError(f"unknown upload mode {session.mode!r}")

        # Finalize: single sends an empty object `{}`; multipart sends the
        # ascending parts list. The token rides the X-Upload-Finalize-Token
        # header.
        #
        # The body MUST be a JSON object, never `{"parts": null}`: the server
        # rejects a null `parts`. Passing `parts=None` explicitly would put the
        # field in pydantic's `model_fields_set`, serializing to `{"parts":
        # null}`; constructing WITHOUT the field leaves it unset so it drops out
        # and the body is `{}`. So build the single-mode body field-free.
        if parts is None:
            finalize_body = FinalizeUploadRequest()
        else:
            finalize_body = FinalizeUploadRequest(parts=parts)
        return self._finalize_handler(
            session.upload_id,
            session.finalize_token,
            finalize_body,
            _request_timeout,
        )

    def upload_stream(
        self,
        body: Union[bytes, bytearray, BinaryIO],
        *,
        content_type: Optional[str] = None,
        content_length: Optional[int] = None,
        _request_timeout: Any = None,
    ) -> UploadResponse:
        """Stream an arbitrary byte source to the legacy ``POST /v1/files`` raw
        upload endpoint, returning the
        :class:`~hotdata.models.upload_response.UploadResponse`.

        Use this when the presigned :meth:`upload_file` path is unavailable
        (e.g. a ``501`` ``PRESIGN_UNSUPPORTED``) or when the bytes come from a
        non-seekable stream that :meth:`upload_file` cannot use. The body is sent
        through the SDK's authenticated client (workspace + bearer headers) — not
        the bare storage pool — because this request goes to the API, not object
        storage.

        ``body`` may be ``bytes`` / ``bytearray`` or a readable binary file
        object. A file object is streamed without being buffered into memory; set
        ``content_length`` (or pass a seekable file, whose length is inferred) so
        the server can reject an oversized upload before reading the body.

        :param body: The bytes or binary stream to upload.
        :param content_type: Content type for the body; defaults to
            ``application/octet-stream``.
        :param content_length: Explicit body length in bytes. Inferred from
            ``bytes`` length or a seekable file; required for a non-seekable
            stream to avoid chunked transfer.
        :raises hotdata.exceptions.ApiException: the upload was rejected.
        """
        if not isinstance(body, (bytes, bytearray)) and not hasattr(body, "read"):
            raise TypeError(
                f"upload_stream accepts bytes or a readable binary file object, "
                f"not {type(body).__name__}"
            )

        # The generated /v1/files op carries only WorkspaceId + BearerAuth; add
        # the X-Session-Id scope header here when a session is configured so
        # sandbox-scoped uploads keep their session context (matches the Rust SDK).
        scope_headers: Dict[str, str] = {}
        session_id = self.api_client.configuration.session_id
        if session_id:
            scope_headers["X-Session-Id"] = session_id

        if isinstance(body, (bytes, bytearray)):
            # bytes go through the generated serialize + transport unchanged;
            # urllib3 sets Content-Length from the buffer length automatically.
            data = bytes(body)
            params = self._upload_file_serialize(
                body=data,
                _request_auth=None,
                _content_type=content_type,
                _headers=scope_headers or None,
                _host_index=0,
            )
            response_data = self.api_client.call_api(*params, _request_timeout=_request_timeout)
            response_data.read()
            return self.api_client.response_deserialize(
                response_data=response_data,
                response_types_map=_UPLOAD_FILE_RESPONSE_TYPES,
            ).data

        # A file object: infer its length when seekable so the request is framed
        # (not chunked), then stream it through the SDK's authenticated pool.
        if content_length is None:
            seekable = getattr(body, "seekable", None)
            if callable(seekable) and body.seekable():
                current = body.tell()
                content_length = body.seek(0, io.SEEK_END) - current
                body.seek(current)
        headers: Dict[str, str] = dict(scope_headers)
        if content_length is not None:
            headers["Content-Length"] = str(content_length)
        method, url, header_params, _body, _post = self._upload_file_serialize(
            body=None,
            _request_auth=None,
            _content_type=content_type,
            _headers=headers or None,
            _host_index=0,
        )
        # Stream via the SDK's configured pool (auth + TLS/proxy), bypassing the
        # generated rest layer, which buffers and rejects file-like bodies.
        raw = self.api_client.rest_client.pool_manager.request(
            method,
            url,
            body=body,
            headers=header_params,
            preload_content=False,
            timeout=_to_timeout(_request_timeout),
        )
        rest_response = RESTResponse(raw)
        rest_response.read()
        return self.api_client.response_deserialize(
            response_data=rest_response,
            response_types_map=_UPLOAD_FILE_RESPONSE_TYPES,
        ).data

    # -- internals ---------------------------------------------------------

    def _finalize_handler(
        self,
        upload_id: str,
        finalize_token: str,
        body: FinalizeUploadRequest,
        _request_timeout: Any,
    ) -> FinalizeUploadResponse:
        """Finalize the upload with retries disabled.

        Finalize is exactly-once on the server: a retry of an ambiguous transient
        (a 429 the server actually processed, or a lost response) would turn a
        finalize that SUCCEEDED into a spurious "already finalized" error. So,
        regardless of the SDK's configured retry policy, this runs through a
        one-off client whose transport does no retries — mirroring the Rust SDK,
        which clones its config with ``max_retries = 0`` for finalize. Auth and
        scope settings are inherited via the shallow-copied configuration.
        """
        finalize_config = copy.copy(self.api_client.configuration)
        finalize_config.retries = False
        finalize_client = ApiClient(finalize_config)
        try:
            return _GeneratedUploadsApi(finalize_client).finalize_upload_handler(
                upload_id,
                finalize_token,
                body,
                _request_timeout=_request_timeout,
            )
        finally:
            finalize_client.close()

    def _upload_single(
        self,
        session: UploadSessionResponse,
        src: _Source,
        total: int,
        progress: Optional[UploadProgress],
    ) -> None:
        """Single-``PUT`` path: stream the whole source to ``session.url``,
        invoking the progress callback incrementally as chunks are sent.

        A streaming body cannot be replayed, so this ``PUT`` is sent once with no
        retry — an intentional trade for smooth progress on the large, common
        single-``PUT`` path.
        """
        url = session.url
        if not url:
            raise MalformedSessionError("single upload missing `url`")

        with src.reader() as fileobj:
            body = _ProgressReader(fileobj, total, progress)
            _put_to_storage(
                url,
                body,
                _storage_headers(session.headers, total),
                retries=False,
                part_number=None,
            )
            # The source ran out before its declared size: we PUT a body shorter
            # than `Content-Length`. Fail loudly before finalizing rather than
            # commit a truncated object (mirrors the multipart short-read guard).
            if body.bytes_read != total:
                raise UploadError(
                    f"source provided {body.bytes_read} bytes but the declared "
                    f"size is {total}; it may have changed size or the declared "
                    f"size is wrong"
                )

        # Guarantee a terminal tick at exactly `total`, even if the last chunk
        # boundary or an empty file left the counter short.
        if progress is not None:
            progress(total, total)

    def _upload_multipart(
        self,
        session: UploadSessionResponse,
        src: _Source,
        total: int,
        max_concurrency: int,
        part_retry: Retry,
        progress: Optional[UploadProgress],
        *,
        max_extra_rounds: int = DEFAULT_MAX_EXTRA_ROUNDS,
        round_base_delay: float = DEFAULT_ROUND_BASE_DELAY,
    ) -> List[FinalizeUploadPart]:
        """Resilient multipart path: ``PUT`` each ``part_size``-byte chunk to
        storage with the whole-upload re-sweep (Item 1) — a single part's
        transient failure never discards the upload.

        URL acquisition is per-path: a *known-size* (eager) session carries
        ``part_urls``; a *streaming* session (``part_urls`` absent) mints each
        part's URL on demand via ``POST /v1/uploads/{id}/parts``. Both run through
        the same re-sweep driver + per-part unit. A stalled ``PUT`` is cancelled
        by the per-upload watchdog (Item 3). Returns the parts ascending by part
        number, ready for finalize.
        """
        part_size = session.part_size
        if part_size is None or part_size <= 0:
            raise MalformedSessionError(
                f"multipart upload has invalid `part_size` {part_size!r}"
            )

        part_urls = session.part_urls
        # Streaming (mint-on-demand) is signalled by `part_urls` being ABSENT
        # (None) on the wire. A present-but-empty list is a malformed known-size
        # session (its URL count won't match), NOT streaming.
        streaming = part_urls is None
        expected_parts = max(-(-total // part_size), 1)  # ceil, at least 1
        if not streaming and len(part_urls) != expected_parts:
            # A known-size session's URL count must match how the file slices.
            raise MalformedSessionError(
                f"multipart upload returned {len(part_urls)} part URLs but the "
                f"file ({total} bytes) splits into {expected_parts} parts of "
                f"{part_size} bytes"
            )

        plans = [
            _PartPlan(
                index=i,
                part_number=i + 1,
                offset=i * part_size,
                length=min(part_size, total - i * part_size),
            )
            for i in range(expected_parts)
        ]

        in_flight = effective_in_flight(max_concurrency, part_size)
        progress_lock = threading.Lock()
        done = [0]  # boxed running byte total; guarded by `progress_lock`

        # Install the cancellation hook on the storage pool, and run one watchdog
        # for this whole upload. Both are torn down in `finally`.
        pool = _storage_pool()
        install_watchdog_connection_classes(pool)
        watchdog = _Watchdog()

        def upload_one(plan: _PartPlan) -> FinalizeUploadPart:
            chunk = src.read_range(plan.offset, plan.length)
            if len(chunk) != plan.length:
                # Deterministic local short-read (truncated source / wrong size):
                # a generic UploadError, which the driver classifies non-retryable.
                raise UploadError(
                    f"source returned {len(chunk)} bytes for part {plan.part_number} "
                    f"(expected {plan.length} at offset {plan.offset}); it may have "
                    f"changed size or the declared size is wrong"
                )

            url = self._part_url(session, plan, streaming)
            headers = _storage_headers(session.headers, plan.length)

            # Publish a per-attempt arming: the connection subclass arms a FRESH
            # watchdog handle on each urllib3 attempt (initial + internal retries,
            # reused keep-alive conns included), with this part's transfer budget.
            arming = _Arming(watchdog, _part_put_timeout(plan.length))
            set_active_arming(arming)
            try:
                try:
                    response = _put_to_storage(
                        url, chunk, headers, retries=part_retry, part_number=plan.part_number
                    )
                except StorageError as exc:
                    # Eager-path URL expiry: a 403 (ONLY) gets ONE inline re-mint
                    # + retry of the fresh URL. A 5xx is NOT an expiry signal — it
                    # propagates to the outer re-sweep (the tier boundary).
                    if not streaming and exc.status == 403:
                        fresh = self._mint_part(session, plan.part_number)
                        response = _put_to_storage(
                            fresh, chunk, headers, retries=part_retry,
                            part_number=plan.part_number,
                        )
                    else:
                        raise
            finally:
                # Defensively disarm every handle this part armed (the subclass
                # already disarms each attempt's handle on supersede and after its
                # response; this catches the error path where getresponse() never
                # returned). A completed/failed part can't be shut down later.
                for handle in arming.all:
                    handle.finish()
                    watchdog.disarm(handle)
                set_active_arming(None)

            etag = _parse_etag(response.headers, plan.part_number)
            return FinalizeUploadPart(e_tag=etag, part_number=plan.part_number)

        def on_part_done(plan: _PartPlan) -> None:
            if progress is None:
                return
            with progress_lock:
                done[0] = min(done[0] + plan.length, total)
                progress(done[0], total)

        try:
            return _upload_parts_resilient(
                plans,
                upload_one,
                base_in_flight=in_flight,
                max_extra_rounds=max_extra_rounds,
                round_base_delay=round_base_delay,
                on_part_done=on_part_done,
                on_terminal=watchdog.cancel_all,
            )
        finally:
            watchdog.shutdown()

    def _part_url(
        self, session: UploadSessionResponse, plan: _PartPlan, streaming: bool
    ) -> str:
        """Resolve the storage URL for ``plan``: the eager ``part_urls`` entry
        for a known-size session, or a freshly minted URL for a streaming one.
        """
        if not streaming:
            return session.part_urls[plan.index]
        return self._mint_part(session, plan.part_number)

    def _mint_part(self, session: UploadSessionResponse, part_number: int) -> str:
        """Mint a fresh presigned URL for one part (streaming path, and the
        eager-path 403 re-mint). Validates the response is for the requested part
        number (Item 6); carries a finite (inactivity) timeout (Item 4 / Codex #5).
        """
        resp = self.mint_upload_parts_handler(
            session.upload_id,
            session.finalize_token,
            MintUploadPartsRequest(part_numbers=[part_number]),
            _request_timeout=MINT_TIMEOUT,
        )
        # Strict validation (Item 6): we requested exactly one part number, so the
        # response must contain exactly that one. Reject a DUPLICATE (two entries
        # for the part — ambiguous, and a plain dict would silently collapse it),
        # an EXTRA/UNREQUESTED part number (contract violation), or a MISSING one.
        parts = resp.parts or []
        numbers = [p.part_number for p in parts]
        if numbers.count(part_number) > 1:
            raise MalformedSessionError(
                f"mint returned duplicate URLs for part {part_number}"
            )
        extra = [n for n in numbers if n != part_number]
        if extra:
            raise MalformedSessionError(
                f"mint returned URLs for parts that were not requested: {sorted(set(extra))}"
            )
        url = next((p.url for p in parts if p.part_number == part_number), None)
        if not url:
            raise MalformedSessionError(
                f"mint did not return a URL for part {part_number}"
            )
        return url


class _Source:
    """Random-access view over the bytes to upload, plus the total ``size``.

    Abstracts the three accepted inputs (a path, raw bytes, or a seekable file
    object) behind :meth:`read_range` (positioned read of one part, used
    concurrently for multipart) and :meth:`reader` (a fresh stream over the whole
    content, used for the single-``PUT`` path).
    """

    size: int

    def read_range(self, offset: int, length: int) -> bytes:
        raise NotImplementedError

    @contextmanager
    def reader(self) -> Iterator[BinaryIO]:
        raise NotImplementedError
        yield  # pragma: no cover - makes this a generator for the type checker


class _PathSource(_Source):
    """A filesystem path. Each read opens its own handle so concurrent part
    reads never share a cursor and a retry re-reads its range cleanly.
    """

    def __init__(self, path: "os.PathLike[str] | str") -> None:
        self._path = os.fspath(path)
        self.size = os.stat(self._path).st_size

    @property
    def default_filename(self) -> str:
        return os.path.basename(self._path)

    def read_range(self, offset: int, length: int) -> bytes:
        with open(self._path, "rb") as fileobj:
            fileobj.seek(offset)
            return fileobj.read(length)

    @contextmanager
    def reader(self) -> Iterator[BinaryIO]:
        fileobj = open(self._path, "rb")
        try:
            yield fileobj
        finally:
            fileobj.close()


class _BytesSource(_Source):
    """Raw in-memory bytes. Slicing is cheap and thread-safe."""

    def __init__(self, data: bytes) -> None:
        self._data = data
        self.size = len(data)

    def read_range(self, offset: int, length: int) -> bytes:
        return self._data[offset:offset + length]

    @contextmanager
    def reader(self) -> Iterator[BinaryIO]:
        yield io.BytesIO(self._data)


class _FileObjSource(_Source):
    """A user-owned, seekable binary file object. The content uploaded is from
    the object's position *at call time* to its end (the Python convention for
    file-object uploads, like ``requests`` / ``boto3``); ``base`` records that
    position so every read is relative to it.

    A lock serializes the seek+read of each part (cheap, in-memory) so concurrent
    part tasks never corrupt the shared cursor; the slow ``PUT`` s still run
    concurrently. The file object is never closed (the caller owns it), and its
    cursor is not restored afterwards.
    """

    def __init__(self, fileobj: BinaryIO, size: Optional[int]) -> None:
        self._file = fileobj
        self._base = fileobj.tell()
        if size is None:
            size = fileobj.seek(0, io.SEEK_END) - self._base
            fileobj.seek(self._base)
        self.size = size
        self._lock = threading.Lock()

    def read_range(self, offset: int, length: int) -> bytes:
        with self._lock:
            self._file.seek(self._base + offset)
            return self._file.read(length)

    @contextmanager
    def reader(self) -> Iterator[BinaryIO]:
        self._file.seek(self._base)
        yield self._file


def _make_source(source: UploadSource, size: Optional[int]) -> _Source:
    """Normalize an upload input into a :class:`_Source`.

    Accepts a path, ``bytes`` / ``bytearray``, or a seekable binary file object.
    A non-seekable stream (or any other type) raises ``TypeError`` pointing at
    :meth:`UploadsApi.upload_stream`, which streams to the legacy endpoint.
    """
    if isinstance(source, (bytes, bytearray)):
        return _BytesSource(bytes(source))
    if isinstance(source, (str, os.PathLike)):
        return _PathSource(source)
    if hasattr(source, "read"):
        seekable = getattr(source, "seekable", None)
        if not (callable(seekable) and source.seekable()):
            raise TypeError(
                "upload_file needs a seekable file object (it does positioned "
                "reads for multipart). For a non-seekable stream use "
                "upload_stream, which sends to POST /v1/files in one request."
            )
        return _FileObjSource(source, size)
    raise TypeError(
        f"upload_file accepts a path, bytes, or a seekable binary file object, "
        f"not {type(source).__name__}. (Did you mean the generated "
        f"hotdata.api.uploads_api.UploadsApi.upload_file(body=...) raw op, or "
        f"upload_stream?)"
    )


__all__ = [
    "DEFAULT_MAX_CONCURRENCY",
    "DEFAULT_MAX_EXTRA_ROUNDS",
    "DEFAULT_PART_SIZE",
    "DEFAULT_ROUND_BASE_DELAY",
    "MAX_PART_SIZE",
    "MIB",
    "MIN_PART_SIZE",
    "TARGET_MAX_PARTS",
    "UPLOAD_MEMORY_BUDGET",
    "MalformedSessionError",
    "MissingETagError",
    "SizeLimitError",
    "StorageError",
    "StorageTransportError",
    "UploadError",
    "UploadOptions",
    "UploadProgress",
    "UploadSource",
    "UploadsApi",
    "auto_part_size_hint",
    "default_part_retry",
    "effective_in_flight",
]
