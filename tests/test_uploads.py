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

import io
import json
import os
import threading
from typing import Any, Dict, List, Optional, Tuple

import pytest

import urllib3
from urllib3.util.retry import Retry

import hotdata.uploads as uploads_mod
from hotdata import UploadsApi as ExportedUploadsApi
from hotdata.exceptions import ApiException
from hotdata.uploads import (
    DEFAULT_PART_SIZE,
    MAX_PART_SIZE,
    MIB,
    MIN_PART_SIZE,
    TARGET_MAX_PARTS,
    UPLOAD_MEMORY_BUDGET,
    MalformedSessionError,
    MissingETagError,
    SizeLimitError,
    StorageError,
    StorageTransportError,
    UploadError,
    UploadOptions,
    UploadsApi,
    auto_part_size_hint,
    effective_in_flight,
)
from hotdata.models.finalize_upload_response import FinalizeUploadResponse
from hotdata.models.upload_response import UploadResponse
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


class _FakeUrllib3Response:
    """Minimal urllib3.HTTPResponse stand-in for the API transport (not storage):
    enough for rest.RESTResponse + ApiClient.response_deserialize.
    """

    def __init__(self, status: int, data: bytes, headers: Dict[str, str]):
        self.status = status
        self.reason = "OK" if 200 <= status < 300 else "Error"
        self.data = data
        # A plain dict (lowercased keys): ApiResponse validates headers as a dict,
        # and response_deserialize looks up 'content-type'.
        self.headers = {k.lower(): v for k, v in headers.items()}


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
        finalize_token: str,
        body: Any = None,
        _request_timeout: Any = None,
    ) -> FinalizeUploadResponse:
        finalize_capture.append(("finalize", upload_id, finalize_token, body))
        from datetime import datetime, timezone

        return FinalizeUploadResponse(
            content_type=None,
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            size_bytes=0,
            status="ready",
            upload_id=upload_id,
        )

    monkeypatch.setattr(api, "create_upload_session_handler", fake_create)
    # Stub the internal finalize seam (upload_file calls _finalize_handler, which
    # routes through a one-off no-retry client); see test_finalize_uses_no_retry_client
    # for the real seam's behavior.
    monkeypatch.setattr(api, "_finalize_handler", fake_finalize)


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


# --- Session/finalize API error paths -------------------------------------


def test_create_session_501_propagates_as_api_exception(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    # A 501 PRESIGN_UNSUPPORTED from POST /v1/uploads surfaces as ApiException
    # (the documented fallback signal), and no storage PUT is attempted.
    src = tmp_path / "f.bin"
    src.write_bytes(b"x" * 10)
    api = _make_api()

    def boom(create_upload_request: Any, **kwargs: Any) -> Any:
        raise ApiException(status=501, reason="PRESIGN_UNSUPPORTED")

    monkeypatch.setattr(api, "create_upload_session_handler", boom)
    with pytest.raises(ApiException) as ei:
        api.upload_file(str(src))
    assert ei.value.status == 501
    assert fake_pool.calls == []  # never reached storage


def test_finalize_is_called_exactly_once(
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
    api.upload_file(str(src))
    finalize_calls = [c for c in capture if c[0] == "finalize"]
    assert len(finalize_calls) == 1


# --- Transport / size / retry plumbing ------------------------------------


def test_storage_transport_error_is_wrapped(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    src = tmp_path / "f.bin"
    src.write_bytes(b"x" * 10)

    class _ExplodingPool:
        def request(self, *a: Any, **k: Any) -> Any:
            raise urllib3.exceptions.ProtocolError("connection aborted")

    monkeypatch.setattr(uploads_mod, "_STORAGE_POOL", _ExplodingPool())
    session = UploadSessionResponse(
        finalize_token="t",
        headers={},
        mode="single",
        upload_id="u",
        url="https://storage.test/put",
    )
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    with pytest.raises(StorageTransportError) as ei:
        api.upload_file(str(src))
    assert isinstance(ei.value.__cause__, urllib3.exceptions.HTTPError)
    assert ei.value.part_number is None


def test_size_limit_guard_on_part_size_hint(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    src = tmp_path / "f.bin"
    src.write_bytes(b"x" * 10)
    api = _make_api()
    # create should never be reached — the guard fires first.
    monkeypatch.setattr(
        api,
        "create_upload_session_handler",
        lambda *a, **k: pytest.fail("create should not be called"),
    )
    with pytest.raises(SizeLimitError) as ei:
        api.upload_file(str(src), part_size=2**63)
    assert ei.value.what == "part_size"


def test_size_limit_guard_on_declared_size(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    src = tmp_path / "f.bin"
    src.write_bytes(b"x" * 10)
    api = _make_api()

    real_stat = os.stat

    class _HugeStat:
        st_size = 2**63

    monkeypatch.setattr(
        uploads_mod.os,
        "stat",
        lambda p: _HugeStat() if str(p) == str(src) else real_stat(p),
    )
    with pytest.raises(SizeLimitError) as ei:
        api.upload_file(str(src))
    assert ei.value.what == "declared_size_bytes"


def test_custom_part_retry_is_forwarded(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    part_size = 5 * MIB
    content = b"a" * part_size
    src = tmp_path / "f.bin"
    src.write_bytes(content)
    url = "https://storage.test/p1"
    fake_pool.responses[url] = _FakeResponse(200, etag='"e1"')
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

    custom = Retry(total=7)
    api.upload_file(str(src), part_retry=custom)
    assert fake_pool.calls[0]["retries"] is custom


def test_default_part_retry_used_when_unset(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    part_size = 5 * MIB
    src = tmp_path / "f.bin"
    src.write_bytes(b"a" * part_size)
    url = "https://storage.test/p1"
    fake_pool.responses[url] = _FakeResponse(200, etag='"e1"')
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
    api.upload_file(str(src))
    retries = fake_pool.calls[0]["retries"]
    assert isinstance(retries, Retry)
    # The default policy retries idempotent PUTs on transient statuses.
    assert 429 in retries.status_forcelist


# --- Byte-granular progress (single PUT) ----------------------------------


def test_single_put_progress_is_byte_granular(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    # A body larger than the read block size produces multiple intermediate
    # progress ticks rather than jumping 0 -> total.
    content = b"z" * (300 * 1024)
    src = tmp_path / "big_single.bin"
    src.write_bytes(content)
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

    intermediate = [d for d, t in ticks if 0 < d < t]
    assert len(intermediate) >= 2, ticks
    assert ticks[-1] == (len(content), len(content))
    assert [d for d, _ in ticks] == sorted(d for d, _ in ticks)


# --- Concurrency is bounded and actually reached --------------------------


class _ConcurrencyProbePool:
    """Fake pool that measures peak simultaneous in-flight PUTs via a barrier.

    Sized so each wave has exactly ``parties`` threads; the barrier forces all
    ``parties`` to be in flight at once, and the executor's worker cap forbids
    more — so the recorded peak equals the effective concurrency.
    """

    def __init__(self, parties: int) -> None:
        self.barrier = threading.Barrier(parties, timeout=5)
        self.active = 0
        self.peak = 0
        self.lock = threading.Lock()

    def request(self, method: str, url: str, **kwargs: Any) -> _FakeResponse:
        with self.lock:
            self.active += 1
            self.peak = max(self.peak, self.active)
        try:
            self.barrier.wait()
        finally:
            with self.lock:
                self.active -= 1
        return _FakeResponse(200, etag='"etag"')


def _multipart_session(part_urls: List[str], part_size: int) -> UploadSessionResponse:
    return UploadSessionResponse(
        finalize_token="t",
        headers={},
        mode="multipart",
        part_size=part_size,
        part_urls=part_urls,
        upload_id="u",
    )


def test_multipart_concurrency_is_bounded_and_reached(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    part_size = 5 * MIB
    # 4 parts, max_concurrency=2 -> effective in-flight is 2; two waves of 2.
    content = b"a" * (4 * part_size)
    src = tmp_path / "mp.bin"
    src.write_bytes(content)
    part_urls = [f"https://storage.test/p{i}" for i in range(1, 5)]
    probe = _ConcurrencyProbePool(parties=2)
    monkeypatch.setattr(uploads_mod, "_STORAGE_POOL", probe)
    api = _make_api()
    _patch_session(monkeypatch, api, _multipart_session(part_urls, part_size), [])

    assert effective_in_flight(2, part_size) == 2
    api.upload_file(str(src), max_concurrency=2)
    assert probe.peak == 2


def test_multipart_serial_when_max_concurrency_one(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    part_size = 5 * MIB
    content = b"a" * (3 * part_size)
    src = tmp_path / "mp1.bin"
    src.write_bytes(content)
    part_urls = [f"https://storage.test/p{i}" for i in range(1, 4)]
    probe = _ConcurrencyProbePool(parties=1)  # barrier of 1 -> never blocks
    monkeypatch.setattr(uploads_mod, "_STORAGE_POOL", probe)
    api = _make_api()
    _patch_session(monkeypatch, api, _multipart_session(part_urls, part_size), [])
    api.upload_file(str(src), max_concurrency=1)
    assert probe.peak == 1


# --- More malformed-session cases -----------------------------------------


def test_multipart_empty_part_urls_raises(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    src = tmp_path / "f.bin"
    src.write_bytes(b"a" * (5 * MIB))
    session = UploadSessionResponse(
        finalize_token="t",
        headers={},
        mode="multipart",
        part_size=5 * MIB,
        part_urls=[],
        upload_id="u",
    )
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    with pytest.raises(MalformedSessionError, match="part_urls"):
        api.upload_file(str(src))


def test_multipart_nonpositive_part_size_raises(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    src = tmp_path / "f.bin"
    src.write_bytes(b"a" * 10)
    session = UploadSessionResponse(
        finalize_token="t",
        headers={},
        mode="multipart",
        part_size=0,
        part_urls=["https://storage.test/p1"],
        upload_id="u",
    )
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    with pytest.raises(MalformedSessionError, match="part_size"):
        api.upload_file(str(src))


# --- Header isolation under a poisoned main client ------------------------


def test_poisoned_main_client_headers_do_not_reach_storage(
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
    api = _make_api()
    # Install auth/scope/UA defaults on the SDK client — they must NOT leak onto
    # the storage PUT, which goes through the dedicated bare pool.
    api.api_client.set_default_header("Authorization", "Bearer SECRET")
    api.api_client.set_default_header("X-Workspace-Id", "ws_secret")
    api.api_client.set_default_header("User-Agent", "hotdata-sdk/test")
    _patch_session(monkeypatch, api, session, [])
    api.upload_file(str(src))
    hdrs = fake_pool.calls[0]["headers"]
    assert "Authorization" not in hdrs
    assert "X-Workspace-Id" not in hdrs
    assert "User-Agent" not in hdrs
    assert hdrs["Content-Length"] == "10"


# --- Wire-level create body -----------------------------------------------


def test_auto_part_size_hint_lands_on_wire(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    content = b"x" * (200 * 1024)
    src = tmp_path / "f.bin"
    src.write_bytes(content)
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
    api.upload_file(str(src))
    create_req = capture[0][1]
    assert create_req.part_size == auto_part_size_hint(len(content))
    assert create_req.part_size == DEFAULT_PART_SIZE


def test_content_encoding_forwarded(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool, tmp_path: Any
) -> None:
    src = tmp_path / "f.bin.gz"
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
    api.upload_file(str(src), content_encoding="gzip")
    assert capture[0][1].content_encoding == "gzip"


# --- upload_file from bytes / file objects --------------------------------


def test_upload_file_from_bytes_single(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool
) -> None:
    content = b"in-memory parquet bytes" * 50
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
    api.upload_file(content, content_type="application/parquet")
    assert fake_pool.calls[0]["body"] == content
    # No filename is inferred for a bytes source.
    assert capture[0][1].filename is None
    assert capture[0][1].declared_size_bytes == len(content)


def test_upload_file_from_bytes_multipart(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool
) -> None:
    part_size = 5 * MIB
    content = bytes((i % 251) for i in range(2 * part_size + 99))
    part_urls = ["https://storage.test/p1", "https://storage.test/p2", "https://storage.test/p3"]
    for i, url in enumerate(part_urls, start=1):
        fake_pool.responses[url] = _FakeResponse(200, etag=f'"e{i}"')
    session = _multipart_session(part_urls, part_size)
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    api.upload_file(content, max_concurrency=2)
    by_url = {c["url"]: c for c in fake_pool.calls}
    assert by_url[part_urls[0]]["body"] == content[0:part_size]
    assert by_url[part_urls[2]]["body"] == content[2 * part_size:]


def test_upload_file_from_file_object(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool
) -> None:
    content = b"seekable file object content" * 100
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
    # Size is inferred from the seekable stream; the user's file is not closed.
    fileobj = io.BytesIO(content)
    api.upload_file(fileobj, filename="data.parquet")
    assert fake_pool.calls[0]["body"] == content
    assert capture[0][1].declared_size_bytes == len(content)
    assert capture[0][1].filename == "data.parquet"
    assert not fileobj.closed


def test_upload_file_file_object_multipart_concurrent_reads(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool
) -> None:
    part_size = 5 * MIB
    content = bytes((i % 251) for i in range(3 * part_size))
    part_urls = [f"https://storage.test/p{i}" for i in range(1, 4)]
    for i, url in enumerate(part_urls, start=1):
        fake_pool.responses[url] = _FakeResponse(200, etag=f'"e{i}"')
    session = _multipart_session(part_urls, part_size)
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    api.upload_file(io.BytesIO(content), max_concurrency=3)
    by_url = {c["url"]: c for c in fake_pool.calls}
    # The lock-guarded positioned reads must still slice each part correctly.
    assert by_url[part_urls[0]]["body"] == content[0:part_size]
    assert by_url[part_urls[1]]["body"] == content[part_size:2 * part_size]
    assert by_url[part_urls[2]]["body"] == content[2 * part_size:]


def test_upload_file_non_seekable_stream_raises(fake_pool: _FakeStoragePool) -> None:
    class _NonSeekable:
        def read(self, n: int = -1) -> bytes:
            return b""

        def seekable(self) -> bool:
            return False

    api = _make_api()
    with pytest.raises(TypeError, match="upload_stream"):
        api.upload_file(_NonSeekable())  # type: ignore[arg-type]


def test_upload_file_bad_type_raises(fake_pool: _FakeStoragePool) -> None:
    api = _make_api()
    with pytest.raises(TypeError, match="path, bytes, or a seekable"):
        api.upload_file(12345)  # type: ignore[arg-type]


# --- upload_stream (legacy POST /v1/files) --------------------------------


def _upload_response_json() -> bytes:
    return json.dumps(
        {
            "content_type": "application/parquet",
            "created_at": "2026-01-01T00:00:00Z",
            "id": "file_123",
            "size_bytes": 5,
            "status": "ready",
        }
    ).encode()


def test_upload_stream_bytes_posts_to_v1_files(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HOTDATA_DISABLE_JWT_EXCHANGE", "1")
    from hotdata import rest

    captured: Dict[str, Any] = {}

    def fake_request(
        self: Any,
        method: str,
        url: str,
        headers: Any = None,
        body: Any = None,
        post_params: Any = None,
        _request_timeout: Any = None,
    ) -> Any:
        captured.update(method=method, url=url, body=body, headers=dict(headers or {}))
        resp = _FakeUrllib3Response(
            201, _upload_response_json(), {"content-type": "application/json"}
        )
        return rest.RESTResponse(resp)

    monkeypatch.setattr(rest.RESTClientObject, "request", fake_request)
    api = _make_api()
    out = api.upload_stream(b"hello", content_type="application/parquet")
    assert captured["method"] == "POST"
    assert captured["url"].endswith("/v1/files")
    assert captured["body"] == b"hello"
    assert captured["headers"]["Content-Type"] == "application/parquet"
    assert isinstance(out, UploadResponse)
    assert out.id == "file_123"


def test_upload_stream_file_object_streams_with_inferred_length(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HOTDATA_DISABLE_JWT_EXCHANGE", "1")
    api = _make_api()

    captured: Dict[str, Any] = {}

    class _FakePoolManager:
        def request(self, method: str, url: str, **kwargs: Any) -> Any:
            body = kwargs["body"]
            captured.update(
                method=method,
                url=url,
                headers=dict(kwargs.get("headers") or {}),
                streamed=body.read(),
                preload_content=kwargs.get("preload_content"),
            )
            return _FakeUrllib3Response(
                201, _upload_response_json(), {"content-type": "application/json"}
            )

    monkeypatch.setattr(api.api_client.rest_client, "pool_manager", _FakePoolManager())

    payload = b"streamed-from-a-file-object"
    out = api.upload_stream(io.BytesIO(payload))
    assert captured["method"] == "POST"
    assert captured["url"].endswith("/v1/files")
    # Length inferred from the seekable stream -> framed (not chunked).
    assert captured["headers"]["Content-Length"] == str(len(payload))
    assert captured["streamed"] == payload
    assert captured["preload_content"] is False
    # Default content type when unset.
    assert captured["headers"]["Content-Type"] == "application/octet-stream"
    # The SDK's User-Agent and scope auth ride the streamed request too.
    assert "User-Agent" in captured["headers"]
    assert captured["headers"]["X-Workspace-Id"] == "ws_test"
    assert isinstance(out, UploadResponse)


def test_upload_stream_bad_type_raises() -> None:
    api = _make_api()
    with pytest.raises(TypeError, match="bytes or a readable"):
        api.upload_stream(12345)  # type: ignore[arg-type]


def _make_api_with_session(session_id: str) -> UploadsApi:
    from hotdata import ApiClient, Configuration

    config = Configuration(
        host="https://api.hotdata.test",
        api_key="test-key",
        workspace_id="ws_test",
        session_id=session_id,
    )
    return UploadsApi(ApiClient(config))


def test_upload_stream_sends_session_and_workspace_scope(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HOTDATA_DISABLE_JWT_EXCHANGE", "1")
    from hotdata import rest

    captured: Dict[str, Any] = {}

    def fake_request(
        self: Any,
        method: str,
        url: str,
        headers: Any = None,
        body: Any = None,
        post_params: Any = None,
        _request_timeout: Any = None,
    ) -> Any:
        captured["headers"] = dict(headers or {})
        resp = _FakeUrllib3Response(
            201, _upload_response_json(), {"content-type": "application/json"}
        )
        return rest.RESTResponse(resp)

    monkeypatch.setattr(rest.RESTClientObject, "request", fake_request)
    api = _make_api_with_session("sb_xyz")
    api.upload_stream(b"hi")
    assert captured["headers"]["X-Session-Id"] == "sb_xyz"
    assert captured["headers"]["X-Workspace-Id"] == "ws_test"


# --- Finalize hardening ----------------------------------------------------


def test_finalize_uses_no_retry_client(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool
) -> None:
    # Don't stub _finalize_handler: let the real one run and route through its
    # one-off no-retry client. Capture the retries policy the generated finalize
    # sees.
    from datetime import datetime, timezone

    from hotdata.api.uploads_api import UploadsApi as Gen

    session = UploadSessionResponse(
        finalize_token="t",
        headers={},
        mode="single",
        upload_id="u",
        url="https://storage.test/put",
    )
    api = _make_api()
    monkeypatch.setattr(
        api, "create_upload_session_handler", lambda *a, **k: session
    )

    captured: Dict[str, Any] = {}

    def fake_gen_finalize(
        self: Any,
        upload_id: str,
        x_upload_finalize_token: str,
        finalize_upload_request: Any = None,
        **kwargs: Any,
    ) -> FinalizeUploadResponse:
        captured["retries"] = self.api_client.configuration.retries
        return FinalizeUploadResponse(
            content_type=None,
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            size_bytes=0,
            status="ready",
            upload_id=upload_id,
        )

    monkeypatch.setattr(Gen, "finalize_upload_handler", fake_gen_finalize)
    api.upload_file(b"hello world")
    # The exactly-once finalize must run with retries disabled regardless of the
    # SDK's configured policy.
    assert captured["retries"] is False


# --- File-object cursor + short-read correctness --------------------------


def test_upload_file_file_object_mid_cursor_single(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool
) -> None:
    # A file object positioned mid-stream uploads from the cursor to the end
    # (the tail), not from byte 0.
    content = b"H" * 100 + b"T" * 200
    fobj = io.BytesIO(content)
    fobj.seek(100)
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
    api.upload_file(fobj)
    assert fake_pool.calls[0]["body"] == b"T" * 200
    assert capture[0][1].declared_size_bytes == 200


def test_upload_file_file_object_mid_cursor_multipart(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool
) -> None:
    part_size = 5 * MIB
    head = b"H" * 10
    tail = bytes((i % 251) for i in range(2 * part_size + 77))
    fobj = io.BytesIO(head + tail)
    fobj.seek(len(head))
    part_urls = ["https://storage.test/p1", "https://storage.test/p2", "https://storage.test/p3"]
    for i, url in enumerate(part_urls, start=1):
        fake_pool.responses[url] = _FakeResponse(200, etag=f'"e{i}"')
    session = _multipart_session(part_urls, part_size)
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    api.upload_file(fobj, max_concurrency=3)
    by_url = {c["url"]: c for c in fake_pool.calls}
    assert by_url[part_urls[0]]["body"] == tail[0:part_size]
    assert by_url[part_urls[1]]["body"] == tail[part_size:2 * part_size]
    assert by_url[part_urls[2]]["body"] == tail[2 * part_size:]


def test_multipart_short_read_raises(
    monkeypatch: pytest.MonkeyPatch, fake_pool: _FakeStoragePool
) -> None:
    part_size = 5 * MIB
    # Only one part's worth of bytes, but we declare two parts' worth via `size`.
    fobj = io.BytesIO(b"a" * part_size)
    part_urls = ["https://storage.test/p1", "https://storage.test/p2"]
    for url in part_urls:
        fake_pool.responses[url] = _FakeResponse(200, etag='"e"')
    session = _multipart_session(part_urls, part_size)
    api = _make_api()
    _patch_session(monkeypatch, api, session, [])
    with pytest.raises(UploadError, match="returned 0 bytes"):
        api.upload_file(fobj, size=2 * part_size)
