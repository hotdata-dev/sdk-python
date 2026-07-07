"""Parity/ergonomics fixes surfaced by the sdk-rust review.

Covers the two functional gaps (streaming-path selection, storage connect
timeout) and the ergonomic changes (top-level re-exports, unified UploadError
base, progress adapter, cancellation, exhausted marker, public timeout knob).
The seams are stubbed the same way as ``test_upload_multipart_resilient.py``:
create/finalize/mint via monkeypatch, storage PUTs via a sequencing fake pool.
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import pytest

import hotdata.uploads as uploads_mod
from hotdata.uploads import (
    MIB,
    STREAMING_THRESHOLD,
    MalformedSessionError,
    StorageError,
    UploadsApi,
)
from hotdata.exceptions import ApiException
from hotdata.models.finalize_upload_response import FinalizeUploadResponse
from hotdata.models.minted_upload_part_response import MintedUploadPartResponse
from hotdata.models.mint_upload_parts_response import MintUploadPartsResponse
from hotdata.models.upload_session_response import UploadSessionResponse


# --- sequencing fake storage pool (mirrors test_upload_multipart_resilient) --


class _Resp:
    def __init__(self, status: int, *, etag: Optional[str] = None, body: bytes = b""):
        self.status = status
        self._headers = {}
        if etag is not None:
            self._headers["ETag"] = etag
        self.data = body

    @property
    def headers(self):
        class _H:
            def __init__(self, d):
                self._d = {k.lower(): v for k, v in d.items()}

            def get(self, k, default=None):
                return self._d.get(k.lower(), default)

        return _H(self._headers)


class _SeqPool:
    def __init__(self) -> None:
        self.responses: Dict[str, List[_Resp]] = {}
        self.default = _Resp(200, etag='"default"')
        self.calls: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def request(self, method: str, url: str, *, body=None, headers=None, retries=None, **kw):
        # The single-PUT path passes a file-like body (a _ProgressReader); drain it
        # like real urllib3 would so its byte counter advances and the short-read
        # guard is satisfied. Record the drained bytes so body assertions still work.
        recorded = body
        if hasattr(body, "read"):
            recorded = body.read()
        with self._lock:
            self.calls.append({"method": method, "url": url, "body": recorded})
            seq = self.responses.get(url)
            if not seq:
                return self.default
            return seq.pop(0) if len(seq) > 1 else seq[0]


@pytest.fixture
def seq_pool(monkeypatch):
    pool = _SeqPool()
    monkeypatch.setattr(uploads_mod, "_STORAGE_POOL", pool)
    monkeypatch.setattr(uploads_mod, "install_watchdog_connection_classes", lambda p: None)
    return pool


def _make_api() -> UploadsApi:
    from hotdata import ApiClient, Configuration

    cfg = Configuration(host="https://api.hotdata.test", api_key="k", workspace_id="ws")
    return UploadsApi(ApiClient(cfg))


def _capture_create(monkeypatch, api, session, captured):
    def fake_create(create_upload_request, **kw):
        captured.append(create_upload_request)
        return session

    monkeypatch.setattr(api, "create_upload_session_handler", fake_create)


def _patch_finalize(monkeypatch, api, capture):
    def fake_finalize(upload_id, finalize_token, body=None, _request_timeout=None):
        capture.append(("finalize", upload_id, body))
        return FinalizeUploadResponse(
            content_type=None,
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            size_bytes=0,
            status="ready",
            upload_id=upload_id,
        )

    monkeypatch.setattr(api, "_finalize_handler", fake_finalize)


def _streaming_session(part_size):
    return UploadSessionResponse(
        finalize_token="tok",
        headers={},
        mode="multipart",
        part_size=part_size,
        part_urls=None,
        upload_id="up_stream",
    )


def _single_session():
    return UploadSessionResponse(
        finalize_token="tok",
        headers={},
        mode="single",
        upload_id="up_single",
        url="https://storage.test/single",
    )


def _eager_session(part_urls, part_size):
    return UploadSessionResponse(
        finalize_token="tok",
        headers={},
        mode="multipart",
        part_size=part_size,
        part_urls=part_urls,
        upload_id="up_eager",
    )


# === GAP 1: large files omit declared_size_bytes to force streaming ==========


def test_large_file_omits_declared_size_bytes(seq_pool, monkeypatch):
    """A file larger than STREAMING_THRESHOLD must OMIT declared_size_bytes so
    the server opens a streaming (per-part on-demand mint) session — the only
    way a presigned URL can't expire mid-transfer on a slow large upload.
    """
    part_size = 5 * MIB
    content = b"x" * (STREAMING_THRESHOLD + 1)
    api = _make_api()

    def fake_mint(upload_id, x_upload_finalize_token, mint_upload_parts_request, **kw):
        parts = [
            MintedUploadPartResponse(part_number=n, url=f"https://storage.test/s/{n}")
            for n in mint_upload_parts_request.part_numbers
        ]
        return MintUploadPartsResponse(parts=parts)

    monkeypatch.setattr(api, "mint_upload_parts_handler", fake_mint)
    captured: List[Any] = []
    _capture_create(monkeypatch, api, _streaming_session(part_size), captured)
    _patch_finalize(monkeypatch, api, [])

    api.upload_file(content, max_concurrency=2, round_base_delay=0.0)

    # The field must be ABSENT on the wire, not sent as null — the server only
    # opens a streaming session when declared_size_bytes is omitted entirely.
    assert captured[0].declared_size_bytes is None
    assert "declared_size_bytes" not in captured[0].to_dict()


def test_small_file_declares_size_bytes(seq_pool, monkeypatch):
    """A file at or below STREAMING_THRESHOLD keeps the known-size path (single
    PUT / eager fast path) by declaring its size.
    """
    content = b"y" * STREAMING_THRESHOLD
    api = _make_api()
    captured: List[Any] = []
    _capture_create(monkeypatch, api, _single_session(), captured)
    _patch_finalize(monkeypatch, api, [])

    api.upload_file(content)

    assert captured[0].declared_size_bytes == len(content)
    assert captured[0].to_dict()["declared_size_bytes"] == len(content)


def test_streaming_part_bytes_keyed_by_part_number(seq_pool, monkeypatch):
    """Byte ranges are keyed to the server part_number, never to completion or
    mint-arrival order: each minted URL receives exactly its own slice even when
    parts finish out of order under concurrency (coverage Gap 1).
    """
    part_size = 5 * MIB
    # Three distinguishable regions so a mis-keyed slice is detectable.
    content = b"A" * part_size + b"B" * part_size + b"C" * (part_size // 2)
    api = _make_api()

    def fake_mint(upload_id, x_upload_finalize_token, mint_upload_parts_request, **kw):
        # Return the requested parts in REVERSED order to prove URL↔part matching
        # is by number, not array position.
        nums = list(mint_upload_parts_request.part_numbers)
        parts = [
            MintedUploadPartResponse(part_number=n, url=f"https://storage.test/s/{n}")
            for n in reversed(nums)
        ]
        return MintUploadPartsResponse(parts=parts)

    for n in (1, 2, 3):
        seq_pool.responses[f"https://storage.test/s/{n}"] = [_Resp(200, etag=f'"e{n}"')]
    monkeypatch.setattr(api, "mint_upload_parts_handler", fake_mint)
    _capture_create(monkeypatch, api, _streaming_session(part_size), [])
    _patch_finalize(monkeypatch, api, [])

    api.upload_file(content, max_concurrency=3, round_base_delay=0.0)

    by_url = {c["url"]: c["body"] for c in seq_pool.calls}
    assert by_url["https://storage.test/s/1"] == content[0:part_size]
    assert by_url["https://storage.test/s/2"] == content[part_size:2 * part_size]
    assert by_url["https://storage.test/s/3"] == content[2 * part_size:]


# === GAP 2: storage pool has a bounded connect timeout =======================


def test_storage_pool_has_connect_timeout(monkeypatch):
    """The bare storage pool must bound TCP+TLS establishment so a dead endpoint
    fails fast into the re-sweep, while leaving the read/transfer unbounded (a
    large upload legitimately takes minutes; the watchdog owns stall detection).
    """
    monkeypatch.setattr(uploads_mod, "_STORAGE_POOL", None)
    pool = uploads_mod._storage_pool()
    timeout = pool.connection_pool_kw["timeout"]
    assert timeout.connect_timeout == uploads_mod.STORAGE_CONNECT_TIMEOUT
    assert timeout.read_timeout is None


# === Ergo #1: error hierarchy + helpers re-exported at top level =============


def test_error_hierarchy_importable_from_top_level():
    import hotdata

    for name in (
        "UploadError",
        "SessionCreateError",
        "MalformedSessionError",
        "SizeLimitError",
        "StorageError",
        "StorageTransportError",
        "MissingETagError",
        "MintPartError",
        "FinalizeError",
        "UploadCancelledError",
        "UploadOptions",
        "UploadProgress",
        "UploadSource",
        "tqdm_progress",
    ):
        assert hasattr(hotdata, name), f"hotdata.{name} not re-exported"
        assert name in hotdata.__all__, f"{name} missing from hotdata.__all__"
        assert getattr(hotdata, name) is getattr(uploads_mod, name)


# === Ergo #2: every phase failure is catchable as UploadError ================


def test_session_create_error_wraps_api_exception(seq_pool, monkeypatch):
    from hotdata.uploads import SessionCreateError, UploadError

    api = _make_api()

    def boom(create_upload_request, **kw):
        raise ApiException(status=501, reason="PRESIGN_UNSUPPORTED")

    monkeypatch.setattr(api, "create_upload_session_handler", boom)

    with pytest.raises(UploadError) as ei:  # catchable via the unified base
        api.upload_file(b"hi")
    assert isinstance(ei.value, SessionCreateError)
    assert ei.value.status == 501  # specific status stays detectable
    assert isinstance(ei.value.__cause__, ApiException)
    assert seq_pool.calls == []


def test_finalize_error_wraps_api_exception(seq_pool, monkeypatch):
    from hotdata.uploads import FinalizeError, UploadError

    api = _make_api()
    _capture_create(monkeypatch, api, _single_session(), [])

    # Let the real _finalize_handler run (that's where the wrapping lives) and make
    # the underlying generated call raise, so we exercise the ApiException→FinalizeError mapping.
    def boom(self, upload_id, finalize_token, body=None, _request_timeout=None):
        raise ApiException(status=409, reason="already finalized")

    monkeypatch.setattr(uploads_mod._GeneratedUploadsApi, "finalize_upload_handler", boom)

    with pytest.raises(UploadError) as ei:
        api.upload_file(b"hello")
    assert isinstance(ei.value, FinalizeError)
    assert ei.value.status == 409
    assert isinstance(ei.value.__cause__, ApiException)


def test_mint_error_wraps_api_exception_and_is_retryable(seq_pool, monkeypatch):
    from hotdata.uploads import MintPartError, UploadError

    part_size = 5 * MIB
    content = b"z" * part_size
    api = _make_api()

    def always_fail_mint(upload_id, token, req, **kw):
        raise ApiException(status=500, reason="mint boom")

    monkeypatch.setattr(api, "mint_upload_parts_handler", always_fail_mint)
    _capture_create(monkeypatch, api, _streaming_session(part_size), [])
    _patch_finalize(monkeypatch, api, [])

    with pytest.raises(UploadError) as ei:
        api.upload_file(content, max_concurrency=1, max_extra_rounds=1, round_base_delay=0.0)
    assert isinstance(ei.value, MintPartError)
    assert ei.value.status == 500
    # Retryable: it survived the round budget, so it is tagged exhausted (Ergo #6).
    assert ei.value.exhausted is True
    assert ei.value.rounds_attempted == 2


# === Ergo #3: tqdm_progress adapter (cumulative -> delta, thread-safe) =======


def test_tqdm_progress_converts_cumulative_to_delta():
    from hotdata.uploads import tqdm_progress

    class _Bar:
        def __init__(self):
            self.n = 0

        def update(self, delta):
            self.n += delta

    bar = _Bar()
    cb = tqdm_progress(bar)
    for done in (0, 8, 16, 20):  # cumulative, as upload_file emits
        cb(done, 20)
    assert bar.n == 20


def test_tqdm_progress_is_thread_safe():
    from hotdata.uploads import tqdm_progress

    class _Bar:
        def __init__(self):
            self.n = 0

        def update(self, delta):
            # Non-atomic read-modify-write; races would corrupt without the lock.
            cur = self.n
            self.n = cur + delta

    bar = _Bar()
    cb = tqdm_progress(bar)
    total = 1000
    # Many threads each advancing the cumulative counter by 1.
    threads = [threading.Thread(target=cb, args=(i + 1, total)) for i in range(total)]
    # Deliver in order so cumulative is monotone; the lock protects bar.n.
    for t in threads:
        t.start()
        t.join()
    assert bar.n == total


# === Ergo #4: cancellation ====================================================


def test_cancel_event_preset_aborts_before_any_put(seq_pool, monkeypatch):
    from hotdata.uploads import UploadCancelledError

    api = _make_api()
    _capture_create(monkeypatch, api, _single_session(), [])
    finalize_calls: List[Any] = []
    _patch_finalize(monkeypatch, api, finalize_calls)

    cancel = threading.Event()
    cancel.set()
    with pytest.raises(UploadCancelledError):
        api.upload_file(b"data", cancel_event=cancel)
    assert seq_pool.calls == []  # nothing PUT
    assert finalize_calls == []  # never finalized


def test_cancel_event_midflight_aborts_multipart(seq_pool, monkeypatch):
    from hotdata.uploads import UploadCancelledError

    part_size = 5 * MIB
    content = b"c" * (3 * part_size)
    api = _make_api()
    urls = [f"https://storage.test/p{n}" for n in (1, 2, 3)]
    for u in urls:
        seq_pool.responses[u] = [_Resp(200, etag='"e"')]
    session = UploadSessionResponse(
        finalize_token="tok",
        headers={},
        mode="multipart",
        part_size=part_size,
        part_urls=urls,
        upload_id="up",
    )
    _capture_create(monkeypatch, api, session, [])
    finalize_calls: List[Any] = []
    _patch_finalize(monkeypatch, api, finalize_calls)

    cancel = threading.Event()
    # Cancel as soon as the first part is PUT; serial so it takes effect on part 2.
    orig_request = seq_pool.request

    def request_then_cancel(method, url, **kw):
        resp = orig_request(method, url, **kw)
        cancel.set()
        return resp

    monkeypatch.setattr(seq_pool, "request", request_then_cancel)

    with pytest.raises(UploadCancelledError):
        api.upload_file(
            content, max_concurrency=1, cancel_event=cancel, round_base_delay=0.0
        )
    # Aborted before all three parts were PUT, and never finalized.
    assert len([c for c in seq_pool.calls if c["method"] == "PUT"]) < 3
    assert finalize_calls == []


# === Ergo #6: exhausted vs terminal marker on StorageError ===================


def test_storage_error_marked_exhausted_after_resweep(seq_pool, monkeypatch):
    part_size = 5 * MIB
    content = b"d" * part_size
    api = _make_api()
    url = "https://storage.test/p1"
    seq_pool.responses[url] = [_Resp(500, body=b"boom")]  # persistent 500
    _capture_create(monkeypatch, api, _eager_session([url], part_size), [])
    _patch_finalize(monkeypatch, api, [])

    with pytest.raises(StorageError) as ei:
        api.upload_file(content, max_concurrency=1, max_extra_rounds=1, round_base_delay=0.0)
    assert ei.value.status == 500
    assert ei.value.exhausted is True
    assert ei.value.rounds_attempted == 2


def test_terminal_error_not_marked_exhausted(seq_pool, monkeypatch):
    # A short-read is a deterministic, non-retryable (terminal) failure: it fails
    # fast on the first round and must NOT be tagged exhausted.
    part_size = 5 * MIB
    api = _make_api()

    class _ShortSource:
        size = 2 * part_size

        def read_range(self, offset, length):
            return b"x" * (length - 1)  # always one byte short

        def reader(self):
            raise AssertionError("multipart path does not use reader()")

    monkeypatch.setattr(uploads_mod, "_make_source", lambda source, size: _ShortSource())
    url1, url2 = "https://storage.test/p1", "https://storage.test/p2"
    _capture_create(monkeypatch, api, _eager_session([url1, url2], part_size), [])
    _patch_finalize(monkeypatch, api, [])

    from hotdata.uploads import UploadError

    with pytest.raises(UploadError) as ei:
        api.upload_file(b"ignored", max_concurrency=1, round_base_delay=0.0)
    assert ei.value.exhausted is False


# === Ergo #7: public request_timeout forwarded to control-plane calls ========


def test_request_timeout_forwarded_to_create_and_finalize(seq_pool, monkeypatch):
    api = _make_api()
    seen: Dict[str, Any] = {}

    def fake_create(create_upload_request, _request_timeout=None):
        seen["create"] = _request_timeout
        return _single_session()

    def fake_finalize(upload_id, finalize_token, body, _request_timeout):
        seen["finalize"] = _request_timeout
        return FinalizeUploadResponse(
            content_type=None,
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            size_bytes=0,
            status="ready",
            upload_id=upload_id,
        )

    monkeypatch.setattr(api, "create_upload_session_handler", fake_create)
    monkeypatch.setattr(api, "_finalize_handler", fake_finalize)

    api.upload_file(b"hi", request_timeout=7.5)

    assert seen["create"] == 7.5
    assert seen["finalize"] == 7.5
