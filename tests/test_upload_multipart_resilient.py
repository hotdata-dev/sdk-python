"""Integration tests for the resilient multipart path: the per-part unit driven
by the re-sweep loop, exercising eager (known-size) and streaming (mint-on-demand)
URL acquisition, the one-shot 403-only re-mint, 5xx → outer re-sweep, blank-ETag
recovery, and finalize completeness.

These stub the two seams (create/finalize/mint via monkeypatch, storage PUTs via
a sequencing fake pool) — no real server. The fake pool supports per-URL response
*sequences* so a 500-then-200 or 403-then-200 can be scripted per path.
"""

from __future__ import annotations

import threading
from typing import Any, Dict, List, Optional, Tuple

import pytest

import hotdata.uploads as uploads_mod
from hotdata.uploads import (
    MIB,
    MalformedSessionError,
    StorageError,
    UploadsApi,
)
from hotdata.models.finalize_upload_response import FinalizeUploadResponse
from hotdata.models.minted_upload_part_response import MintedUploadPartResponse
from hotdata.models.mint_upload_parts_response import MintUploadPartsResponse
from hotdata.models.upload_session_response import UploadSessionResponse


# --- sequencing fake storage pool -----------------------------------------


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
    """Fake storage pool. ``responses[url]`` is a list popped per call (last
    entry reused once exhausted), so a 500-then-200 sequence is scriptable.
    Records each PUT.
    """

    def __init__(self) -> None:
        self.responses: Dict[str, List[_Resp]] = {}
        self.default = _Resp(200, etag='"default"')
        self.calls: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def request(self, method: str, url: str, *, body=None, headers=None, retries=None, **kw):
        with self._lock:
            self.calls.append({"method": method, "url": url, "body": body})
            seq = self.responses.get(url)
            if not seq:
                return self.default
            return seq.pop(0) if len(seq) > 1 else seq[0]


@pytest.fixture
def seq_pool(monkeypatch):
    pool = _SeqPool()
    monkeypatch.setattr(uploads_mod, "_STORAGE_POOL", pool)
    # The resilient path installs the watchdog ConnectionCls on the pool; the
    # fake doesn't need it, but install is a no-op-safe call on a non-pool, so
    # stub it out for the fake.
    monkeypatch.setattr(uploads_mod, "install_watchdog_connection_classes", lambda p: None)
    return pool


def _make_api() -> UploadsApi:
    from hotdata import ApiClient, Configuration

    cfg = Configuration(host="https://api.hotdata.test", api_key="k", workspace_id="ws")
    return UploadsApi(ApiClient(cfg))


def _patch_finalize(monkeypatch, api, capture):
    def fake_finalize(upload_id, finalize_token, body=None, _request_timeout=None):
        from datetime import datetime, timezone

        capture.append(("finalize", upload_id, body))
        return FinalizeUploadResponse(
            content_type=None,
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            size_bytes=0,
            status="ready",
            upload_id=upload_id,
        )

    monkeypatch.setattr(api, "_finalize_handler", fake_finalize)


def _eager_session(part_urls, part_size):
    return UploadSessionResponse(
        finalize_token="tok",
        headers={},
        mode="multipart",
        part_size=part_size,
        part_urls=part_urls,
        upload_id="up_eager",
    )


def _streaming_session(part_size):
    return UploadSessionResponse(
        finalize_token="tok",
        headers={},
        mode="multipart",
        part_size=part_size,
        part_urls=None,  # streaming: mint on demand
        upload_id="up_stream",
    )


# --- 5xx → outer re-sweep (tier boundary, Item 5) -------------------------


def test_part_500_recovered_by_outer_resweep(seq_pool, monkeypatch):
    part_size = 5 * MIB
    content = b"a" * part_size
    api = _make_api()
    url = "https://storage.test/p1"
    seq_pool.responses[url] = [_Resp(500, body=b"boom"), _Resp(200, etag='"e1"')]
    monkeypatch.setattr(
        api, "create_upload_session_handler", lambda *a, **k: _eager_session([url], part_size)
    )
    capture: List[Any] = []
    _patch_finalize(monkeypatch, api, capture)

    api.upload_file(content, max_concurrency=2, round_base_delay=0.0)

    # 500 was NOT inner-retried (would have inner-swallowed it); the outer
    # re-sweep re-PUT and succeeded → part PUT twice.
    puts = [c for c in seq_pool.calls if c["url"] == url]
    assert len(puts) == 2
    fin = capture[-1]
    parts = fin[2].parts
    assert [p.part_number for p in parts] == [1]
    assert parts[0].e_tag == '"e1"'


# --- streaming: mint per part ---------------------------------------------


def test_streaming_session_mints_per_part(seq_pool, monkeypatch):
    part_size = 5 * MIB
    content = b"b" * (2 * part_size)
    api = _make_api()
    mint_calls: List[List[int]] = []

    def fake_mint(upload_id, x_upload_finalize_token, mint_upload_parts_request, **kw):
        nums = list(mint_upload_parts_request.part_numbers)
        mint_calls.append(nums)
        parts = [
            MintedUploadPartResponse(part_number=n, url=f"https://storage.test/spart/{n}")
            for n in nums
        ]
        return MintUploadPartsResponse(parts=parts)

    for n in (1, 2):
        seq_pool.responses[f"https://storage.test/spart/{n}"] = [_Resp(200, etag=f'"e{n}"')]
    monkeypatch.setattr(
        api, "create_upload_session_handler", lambda *a, **k: _streaming_session(part_size)
    )
    monkeypatch.setattr(api, "mint_upload_parts_handler", fake_mint)
    capture: List[Any] = []
    _patch_finalize(monkeypatch, api, capture)

    api.upload_file(content, max_concurrency=2, round_base_delay=0.0)

    # One mint per part, each PUT to its minted URL.
    assert sorted(n for nums in mint_calls for n in nums) == [1, 2]
    fin = capture[-1]
    assert [p.part_number for p in fin[2].parts] == [1, 2]
    assert [p.e_tag for p in fin[2].parts] == ['"e1"', '"e2"']


def test_streaming_mint_finite_timeout(seq_pool, monkeypatch):
    part_size = 5 * MIB
    api = _make_api()
    seen_timeout: List[Any] = []

    def fake_mint(upload_id, x_upload_finalize_token, mint_upload_parts_request, **kw):
        seen_timeout.append(kw.get("_request_timeout"))
        n = mint_upload_parts_request.part_numbers[0]
        return MintUploadPartsResponse(
            parts=[MintedUploadPartResponse(part_number=n, url=f"https://storage.test/s/{n}")]
        )

    seq_pool.responses["https://storage.test/s/1"] = [_Resp(200, etag='"e1"')]
    monkeypatch.setattr(
        api, "create_upload_session_handler", lambda *a, **k: _streaming_session(part_size)
    )
    monkeypatch.setattr(api, "mint_upload_parts_handler", fake_mint)
    _patch_finalize(monkeypatch, api, [])

    api.upload_file(b"c" * part_size, round_base_delay=0.0)
    # The mint must carry a finite (connect, read) timeout, not None.
    assert seen_timeout[0] == uploads_mod.MINT_TIMEOUT


# --- eager 403: one-shot inline re-mint (Codex #7) ------------------------


def test_eager_403_reminted_once_and_recovers(seq_pool, monkeypatch):
    part_size = 5 * MIB
    api = _make_api()
    eager_url = "https://storage.test/eager1"
    fresh_url = "https://storage.test/fresh1"
    seq_pool.responses[eager_url] = [_Resp(403, body=b"<Error>SignatureDoesNotMatch</Error>")]
    seq_pool.responses[fresh_url] = [_Resp(200, etag='"fresh-e1"')]

    mint_calls: List[List[int]] = []

    def fake_mint(upload_id, x_upload_finalize_token, mint_upload_parts_request, **kw):
        mint_calls.append(list(mint_upload_parts_request.part_numbers))
        return MintUploadPartsResponse(
            parts=[MintedUploadPartResponse(part_number=1, url=fresh_url)]
        )

    monkeypatch.setattr(
        api, "create_upload_session_handler", lambda *a, **k: _eager_session([eager_url], part_size)
    )
    monkeypatch.setattr(api, "mint_upload_parts_handler", fake_mint)
    capture: List[Any] = []
    _patch_finalize(monkeypatch, api, capture)

    api.upload_file(b"d" * part_size, round_base_delay=0.0)

    # Exactly one inline re-mint for part 1 after the 403.
    assert mint_calls == [[1]]
    assert any(c["url"] == fresh_url for c in seq_pool.calls)
    assert capture[-1][2].parts[0].e_tag == '"fresh-e1"'


def test_eager_5xx_does_not_remint(seq_pool, monkeypatch):
    part_size = 5 * MIB
    api = _make_api()
    eager_url = "https://storage.test/eager1"
    # 500 forever → never inline-remints; surfaces after the re-sweep budget.
    seq_pool.responses[eager_url] = [_Resp(500, body=b"boom")]

    mint_calls: List[Any] = []
    monkeypatch.setattr(
        api,
        "mint_upload_parts_handler",
        lambda *a, **k: mint_calls.append(1) or MintUploadPartsResponse(parts=[]),
    )
    monkeypatch.setattr(
        api, "create_upload_session_handler", lambda *a, **k: _eager_session([eager_url], part_size)
    )
    _patch_finalize(monkeypatch, api, [])

    with pytest.raises(StorageError) as ei:
        api.upload_file(b"e" * part_size, max_extra_rounds=1, round_base_delay=0.0)
    assert ei.value.status == 500
    # A 5xx is NOT an expiry signal: never inline-reminted.
    assert mint_calls == []


# --- blank ETag is retryable (Item 7) -------------------------------------


def test_blank_etag_retried_then_recovers(seq_pool, monkeypatch):
    part_size = 5 * MIB
    api = _make_api()
    url = "https://storage.test/p1"
    # First PUT returns 200 with a whitespace-only ETag → MissingETagError
    # (retryable); re-sweep gets a real one.
    seq_pool.responses[url] = [_Resp(200, etag="   "), _Resp(200, etag='"real"')]
    monkeypatch.setattr(
        api, "create_upload_session_handler", lambda *a, **k: _eager_session([url], part_size)
    )
    capture: List[Any] = []
    _patch_finalize(monkeypatch, api, capture)

    api.upload_file(b"f" * part_size, round_base_delay=0.0)
    assert capture[-1][2].parts[0].e_tag == '"real"'


# --- mint response validation (Item 6) ------------------------------------


def test_storage_3xx_surfaces_as_error(seq_pool, monkeypatch):
    # Codex #6: with redirects disabled, a storage 3xx must surface as a
    # StorageError (following it would invalidate the presigned signature), not
    # be silently treated as success.
    part_size = 5 * MIB
    api = _make_api()
    url = "https://storage.test/p1"
    seq_pool.responses[url] = [_Resp(302, body=b"redirect")]
    monkeypatch.setattr(
        api, "create_upload_session_handler", lambda *a, **k: _eager_session([url], part_size)
    )
    _patch_finalize(monkeypatch, api, [])
    with pytest.raises(StorageError) as ei:
        api.upload_file(b"h" * part_size, max_extra_rounds=0, round_base_delay=0.0)
    assert ei.value.status == 302


def test_bounded_retry_multiplication(seq_pool, monkeypatch):
    # The inner urllib3.Retry total and the outer re-sweep rounds MULTIPLY: a
    # part PUT that always fails transiently is attempted at most
    # (1 + max_extra_rounds) times by the OUTER loop. (The inner Retry total is a
    # urllib3 concern, exercised separately in test_upload_retry_policy.) Here we
    # bound the OUTER multiplication: a persistent 500 → exactly 1+rounds PUTs.
    part_size = 5 * MIB
    api = _make_api()
    url = "https://storage.test/p1"
    seq_pool.responses[url] = [_Resp(500, body=b"boom")]  # always 500
    monkeypatch.setattr(
        api, "create_upload_session_handler", lambda *a, **k: _eager_session([url], part_size)
    )
    _patch_finalize(monkeypatch, api, [])
    with pytest.raises(StorageError):
        api.upload_file(b"i" * part_size, max_extra_rounds=2, round_base_delay=0.0)
    puts = [c for c in seq_pool.calls if c["url"] == url]
    assert len(puts) == 3  # 1 initial round + 2 re-sweeps, bounded


def test_streaming_mint_missing_requested_part_is_rejected(seq_pool, monkeypatch):
    part_size = 5 * MIB
    api = _make_api()

    def bad_mint(upload_id, x_upload_finalize_token, mint_upload_parts_request, **kw):
        # Return a DIFFERENT part number than requested.
        return MintUploadPartsResponse(
            parts=[MintedUploadPartResponse(part_number=999, url="https://storage.test/x")]
        )

    monkeypatch.setattr(
        api, "create_upload_session_handler", lambda *a, **k: _streaming_session(part_size)
    )
    monkeypatch.setattr(api, "mint_upload_parts_handler", bad_mint)
    _patch_finalize(monkeypatch, api, [])

    with pytest.raises(MalformedSessionError):
        api.upload_file(b"g" * part_size, max_extra_rounds=0, round_base_delay=0.0)
