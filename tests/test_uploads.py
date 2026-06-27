"""Unit tests for hotdata.uploads.

The ergonomic upload flow has two collaborators: the generated session
create/finalize ops (which go through the SDK ApiClient) and the direct-to-
storage ``PUT`` s (which go through a separate bare urllib3 pool). These tests
stub both seams so no server or object store is needed:

* the generated ``create_upload_session_handler`` / ``finalize_upload_handler``
  are patched to return canned models and capture the finalize body;
* ``hotdata.uploads._STORAGE_POOL`` is replaced with a fake pool that records
  every ``PUT`` (url, body, headers) and returns a canned status + ETag.

They verify the single and multipart paths end to end: correct bytes per part,
ascending part list with ETags, header isolation on storage PUTs, the finalize
body shape, progress reporting, and the error paths.
"""

from __future__ import annotations

import threading
from typing import Any, Dict, List, Optional, Tuple

import pytest

import hotdata.uploads as uploads_mod
from hotdata import UploadsApi as ExportedUploadsApi
from hotdata.uploads import (
    DEFAULT_PART_SIZE,
    MAX_PART_SIZE,
    MIB,
    MIN_PART_SIZE,
    TARGET_MAX_PARTS,
    UPLOAD_MEMORY_BUDGET,
    MalformedSessionError,
    MissingETagError,
    StorageError,
    UploadOptions,
    UploadsApi,
    auto_part_size_hint,
    effective_in_flight,
)
from hotdata.models.finalize_upload_response import FinalizeUploadResponse
from hotdata.models.upload_session_response import UploadSessionResponse


# --- Fakes ----------------------------------------------------------------


class _FakeHeaders:
    """Case-insensitive header map, like urllib3's HTTPHeaderDict."""

    def __init__(self, data: Dict[str, str]):
        self._data = {k.lower(): v for k, v in data.items()}

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key.lower(), default)


class _FakeResponse:
    def __init__(self, status: int, *, etag: Optional[str] = None, body: bytes = b""):
        self.status = status
        headers: Dict[str, str] = {}
        if etag is not None:
            headers["ETag"] = etag
        self.headers = _FakeHeaders(headers)
        self.data = body


class _FakeStoragePool:
    """Stand-in for the bare storage urllib3.PoolManager.

    Records each PUT and returns a per-URL canned response. ``body`` may be raw
    bytes (multipart) or a file-like progress reader (single PUT) — file-like
    bodies are drained so the single-PUT progress callback fires.
    """

    def __init__(self) -> None:
        self.calls: List[Dict[str, Any]] = []
        # url -> _FakeResponse, or a default for any url.
        self.responses: Dict[str, _FakeResponse] = {}
        self.default_response = _FakeResponse(200, etag='"default-etag"')
        self.lock = threading.Lock()

    def request(
        self,
        method: str,
        url: str,
        *,
        body: Any = None,
        headers: Optional[Dict[str, str]] = None,
        retries: Any = None,
        **kwargs: Any,
    ) -> _FakeResponse:
        # Drain a file-like body (single PUT) so its progress reader runs; keep
        # raw bytes verbatim (multipart parts).
        if hasattr(body, "read"):
            collected = b""
            while True:
                chunk = body.read(64 * 1024)
                if not chunk:
                    break
                collected += chunk
            recorded_body = collected
        else:
            recorded_body = body
        with self.lock:
            self.calls.append(
                {
                    "method": method,
                    "url": url,
                    "body": recorded_body,
                    "headers": dict(headers or {}),
                    "retries": retries,
                }
            )
        return self.responses.get(url, self.default_response)


@pytest.fixture
def fake_pool(monkeypatch: pytest.MonkeyPatch) -> _FakeStoragePool:
    pool = _FakeStoragePool()
    monkeypatch.setattr(uploads_mod, "_STORAGE_POOL", pool)
    return pool


def _patch_session(
    monkeypatch: pytest.MonkeyPatch,
    api: UploadsApi,
    session: UploadSessionResponse,
    finalize_capture: List[Tuple[Any, ...]],
) -> None:
    """Stub the generated create/finalize ops on the instance."""

    def fake_create(create_upload_request: Any, **kwargs: Any) -> UploadSessionResponse:
        finalize_capture.append(("create", create_upload_request))
        return session

    def fake_finalize(
        upload_id: str,
        x_upload_finalize_token: str,
        finalize_upload_request: Any = None,
        **kwargs: Any,
    ) -> FinalizeUploadResponse:
        finalize_capture.append(
            ("finalize", upload_id, x_upload_finalize_token, finalize_upload_request)
        )
        from datetime import datetime, timezone

        return FinalizeUploadResponse(
            content_type=None,
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            size_bytes=0,
            status="ready",
            upload_id=upload_id,
        )

    monkeypatch.setattr(api, "create_upload_session_handler", fake_create)
    monkeypatch.setattr(api, "finalize_upload_handler", fake_finalize)


def _make_api() -> UploadsApi:
    from hotdata import ApiClient, Configuration

    config = Configuration(
        host="https://api.hotdata.test",
        api_key="test-key",
        workspace_id="ws_test",
    )
    return UploadsApi(ApiClient(config))


# --- Pure helpers (ported from the Rust unit tests) -----------------------


def test_auto_part_size_keeps_8mib_for_normal_files() -> None:
    assert auto_part_size_hint(0) == DEFAULT_PART_SIZE
    assert auto_part_size_hint(1) == DEFAULT_PART_SIZE
    assert auto_part_size_hint(100 * MIB) == DEFAULT_PART_SIZE
    assert auto_part_size_hint(1024 * MIB) == DEFAULT_PART_SIZE
    assert auto_part_size_hint(DEFAULT_PART_SIZE * TARGET_MAX_PARTS) == DEFAULT_PART_SIZE


def test_auto_part_size_scales_up_for_very_large_files() -> None:
    big = 200 * 1024 * MIB  # 200 GiB
    hint = auto_part_size_hint(big)
    assert hint > DEFAULT_PART_SIZE
    assert hint % MIB == 0
    assert -(-big // hint) <= TARGET_MAX_PARTS
    assert MIN_PART_SIZE <= hint <= MAX_PART_SIZE


def test_auto_part_size_clamps_to_max_for_enormous_files() -> None:
    assert auto_part_size_hint(100 * 1024 * 1024 * MIB) == MAX_PART_SIZE


def test_effective_in_flight_capped_by_max_concurrency() -> None:
    assert effective_in_flight(12, 8 * MIB) == 12
    assert effective_in_flight(10, 8 * MIB) == 10
    assert effective_in_flight(12, MIB) == 12


def test_effective_in_flight_reduced_by_memory_budget() -> None:
    assert effective_in_flight(12, 64 * MIB) == 4
    assert effective_in_flight(12, 128 * MIB) == 2


def test_effective_in_flight_honors_explicit_low_concurrency() -> None:
    assert effective_in_flight(1, 8 * MIB) == 1
    assert effective_in_flight(0, 8 * MIB) == 1
    assert effective_in_flight(2, 8 * MIB) == 2


def test_effective_in_flight_floors_at_1_and_handles_zero() -> None:
    assert effective_in_flight(12, UPLOAD_MEMORY_BUDGET * 4) == 1
    assert effective_in_flight(12, 0) == 12


# --- Single-PUT path ------------------------------------------------------


def test_single_upload_puts_bytes_and_finalizes(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    content = b"hello, hotdata" * 100
    src = tmp_path / "data.parquet"
    src.write_bytes(content)

    session = UploadSessionResponse(
        finalize_token="tok-123",
        headers={},
        mode="single",
        upload_id="up_1",
        url="https://storage.test/put/up_1?sig=abc",
    )
    capture: List[Tuple[Any, ...]] = []
    api = _make_api()
    _patch_session(monkeypatch, api, session, capture)

    ticks: List[Tuple[int, int]] = []
    result = api.upload_file(
        str(src),
        content_type="application/parquet",
        progress=lambda done, total: ticks.append((done, total)),
    )

    # One PUT carrying the whole file, to the single URL.
    assert len(fake_pool.calls) == 1
    call = fake_pool.calls[0]
    assert call["method"] == "PUT"
    assert call["url"] == session.url
    assert call["body"] == content
    # Header isolation: only Content-Length, no SDK auth/workspace headers.
    assert call["headers"]["Content-Length"] == str(len(content))
    assert "Authorization" not in call["headers"]
    assert "X-Workspace-Id" not in call["headers"]
    # Single PUT is sent without retry (un-replayable streaming body).
    assert call["retries"] is False

    # create carried the declared size + content type; finalize sent an empty
    # parts body (single uploads have no parts) with the token.
    kind, create_req = capture[0]
    assert kind == "create"
    assert create_req.declared_size_bytes == len(content)
    assert create_req.content_type == "application/parquet"
    assert create_req.filename == "data.parquet"
    fin = capture[1]
    assert fin[0] == "finalize" and fin[1] == "up_1" and fin[2] == "tok-123"
    assert fin[3].parts is None
    # Finalize body serializes to `{}` (no parts), which the server requires.
    assert fin[3].to_dict() == {}

    assert isinstance(result, FinalizeUploadResponse)
    # Progress is monotonic and ends exactly at total.
    assert ticks[0] == (0, len(content))
    assert ticks[-1] == (len(content), len(content))
    assert all(b <= len(content) for b, _ in ticks)
    assert [b for b, _ in ticks] == sorted(b for b, _ in ticks)


def test_single_upload_missing_url_raises(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    src = tmp_path / "f.bin"
    src.write_bytes(b"x" * 10)
    session = UploadSessionResponse(
        finalize_token="t", headers={}, mode="single", upload_id="u", url=None
    )
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    with pytest.raises(MalformedSessionError, match="missing `url`"):
        api.upload_file(str(src))


def test_single_upload_storage_error(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    src = tmp_path / "f.bin"
    src.write_bytes(b"x" * 10)
    url = "https://storage.test/put"
    session = UploadSessionResponse(
        finalize_token="t", headers={}, mode="single", upload_id="u", url=url
    )
    fake_pool.responses[url] = _FakeResponse(403, body=b"<Error>SignatureDoesNotMatch</Error>")
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    with pytest.raises(StorageError) as ei:
        api.upload_file(str(src))
    assert ei.value.status == 403
    assert ei.value.part_number is None
    assert "SignatureDoesNotMatch" in ei.value.body


def test_zero_byte_single_upload(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    src = tmp_path / "empty.bin"
    src.write_bytes(b"")
    session = UploadSessionResponse(
        finalize_token="t",
        headers={},
        mode="single",
        upload_id="u",
        url="https://storage.test/put",
    )
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    ticks: List[Tuple[int, int]] = []
    api.upload_file(str(src), progress=lambda d, t: ticks.append((d, t)))
    assert fake_pool.calls[0]["body"] == b""
    assert fake_pool.calls[0]["headers"]["Content-Length"] == "0"
    # Terminal tick at (0, 0).
    assert ticks[-1] == (0, 0)


# --- Multipart path -------------------------------------------------------


def test_multipart_upload_slices_and_collects_etags(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    part_size = 5 * MIB
    # 2 full parts + a remainder => 3 parts.
    content = bytes((i % 256) for i in range(2 * part_size + 1234))
    src = tmp_path / "big.parquet"
    src.write_bytes(content)

    part_urls = [
        "https://storage.test/p1",
        "https://storage.test/p2",
        "https://storage.test/p3",
    ]
    for i, url in enumerate(part_urls, start=1):
        fake_pool.responses[url] = _FakeResponse(200, etag=f'"etag-{i}"')

    session = UploadSessionResponse(
        finalize_token="mtok",
        headers={},
        mode="multipart",
        part_size=part_size,
        part_urls=part_urls,
        upload_id="up_mp",
    )
    capture: List[Tuple[Any, ...]] = []
    api = _make_api()
    _patch_session(monkeypatch, api, session, capture)

    ticks: List[Tuple[int, int]] = []
    api.upload_file(
        str(src),
        max_concurrency=2,
        progress=lambda d, t: ticks.append((d, t)),
    )

    # Three PUTs, one per part. Order may vary (concurrent), so index by URL.
    assert len(fake_pool.calls) == 3
    by_url = {c["url"]: c for c in fake_pool.calls}
    assert by_url[part_urls[0]]["body"] == content[0:part_size]
    assert by_url[part_urls[1]]["body"] == content[part_size:(2 * part_size)]
    assert by_url[part_urls[2]]["body"] == content[(2 * part_size):]
    # Each part PUT declares its own Content-Length and carries no auth headers.
    assert by_url[part_urls[2]]["headers"]["Content-Length"] == str(len(content) - 2 * part_size)
    assert "Authorization" not in by_url[part_urls[0]]["headers"]
    # Part PUTs are retryable (idempotent), so a Retry object is passed.
    assert by_url[part_urls[0]]["retries"] is not False
    assert by_url[part_urls[0]]["retries"] is not None

    # Finalize body has the ascending part list with the storage ETags.
    fin = capture[-1]
    assert fin[0] == "finalize"
    parts = fin[3].parts
    assert [p.part_number for p in parts] == [1, 2, 3]
    assert [p.e_tag for p in parts] == ['"etag-1"', '"etag-2"', '"etag-3"']

    # Progress reaches total exactly and is non-decreasing.
    assert ticks[-1] == (len(content), len(content))
    assert [b for b, _ in ticks] == sorted(b for b, _ in ticks)


def test_multipart_part_url_count_mismatch_raises(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    part_size = 5 * MIB
    content = b"a" * (2 * part_size)  # splits into exactly 2 parts
    src = tmp_path / "f.bin"
    src.write_bytes(content)
    session = UploadSessionResponse(
        finalize_token="t",
        headers={},
        mode="multipart",
        part_size=part_size,
        part_urls=["https://storage.test/only-one"],  # too few
        upload_id="u",
    )
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    with pytest.raises(MalformedSessionError, match="part URLs"):
        api.upload_file(str(src))


def test_multipart_missing_etag_raises(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    part_size = 5 * MIB
    content = b"a" * part_size
    src = tmp_path / "f.bin"
    src.write_bytes(content)
    url = "https://storage.test/p1"
    fake_pool.responses[url] = _FakeResponse(200, etag=None)  # accepted, no ETag
    session = UploadSessionResponse(
        finalize_token="t",
        headers={},
        mode="multipart",
        part_size=part_size,
        part_urls=[url],
        upload_id="u",
    )
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    with pytest.raises(MissingETagError) as ei:
        api.upload_file(str(src))
    assert ei.value.part_number == 1


def test_multipart_storage_error_includes_part_number(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    part_size = 5 * MIB
    content = b"a" * part_size
    src = tmp_path / "f.bin"
    src.write_bytes(content)
    url = "https://storage.test/p1"
    fake_pool.responses[url] = _FakeResponse(500, body=b"boom")
    session = UploadSessionResponse(
        finalize_token="t",
        headers={},
        mode="multipart",
        part_size=part_size,
        part_urls=[url],
        upload_id="u",
    )
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    with pytest.raises(StorageError) as ei:
        api.upload_file(str(src))
    assert ei.value.status == 500
    assert ei.value.part_number == 1


# --- Options / session shape ----------------------------------------------


def test_unknown_mode_raises(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    src = tmp_path / "f.bin"
    src.write_bytes(b"x")
    session = UploadSessionResponse(
        finalize_token="t", headers={}, mode="teleport", upload_id="u"
    )
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    with pytest.raises(MalformedSessionError, match="unknown upload mode"):
        api.upload_file(str(src))


def test_options_bundle_and_kwarg_precedence(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    src = tmp_path / "f.bin"
    src.write_bytes(b"x" * 10)
    session = UploadSessionResponse(
        finalize_token="t",
        headers={},
        mode="single",
        upload_id="u",
        url="https://storage.test/put",
    )
    capture: List[Tuple[Any, ...]] = []
    api = _make_api()
    _patch_session(monkeypatch, api, session, capture)

    opts = UploadOptions(content_type="text/csv", filename="from-opts.csv")
    # Keyword filename overrides the options bundle; content_type comes from opts.
    api.upload_file(str(src), filename="from-kwarg.csv", options=opts)

    create_req = capture[0][1]
    assert create_req.content_type == "text/csv"
    assert create_req.filename == "from-kwarg.csv"


def test_explicit_part_size_hint_forwarded(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    src = tmp_path / "f.bin"
    src.write_bytes(b"x" * 10)
    session = UploadSessionResponse(
        finalize_token="t",
        headers={},
        mode="single",
        upload_id="u",
        url="https://storage.test/put",
    )
    capture: List[Tuple[Any, ...]] = []
    api = _make_api()
    _patch_session(monkeypatch, api, session, capture)
    api.upload_file(str(src), part_size=16 * MIB)
    assert capture[0][1].part_size == 16 * MIB


def test_session_headers_replayed_on_storage_put(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    src = tmp_path / "f.bin"
    src.write_bytes(b"x" * 10)
    session = UploadSessionResponse(
        finalize_token="t",
        headers={"x-amz-server-side-encryption": "AES256"},
        mode="single",
        upload_id="u",
        url="https://storage.test/put",
    )
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    api.upload_file(str(src))
    hdrs = fake_pool.calls[0]["headers"]
    assert hdrs["x-amz-server-side-encryption"] == "AES256"
    assert hdrs["Content-Length"] == "10"


def test_exported_uploads_api_is_enhanced() -> None:
    # `from hotdata import UploadsApi` resolves to the ergonomic subclass.
    assert ExportedUploadsApi is UploadsApi
    assert hasattr(ExportedUploadsApi, "upload_file")
