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

import io
import logging
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, BinaryIO, Callable, Dict, Iterator, List, Optional, Union

import urllib3
from urllib3.util.retry import Retry

from hotdata.api.uploads_api import UploadsApi as _GeneratedUploadsApi
from hotdata.models.create_upload_request import CreateUploadRequest
from hotdata.models.finalize_upload_part import FinalizeUploadPart
from hotdata.models.finalize_upload_request import FinalizeUploadRequest
from hotdata.models.finalize_upload_response import FinalizeUploadResponse
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
    #: ``urllib3`` retry policy for multipart part ``PUT`` s (idempotent, so safe
    #: to retry). ``None`` uses :func:`default_part_retry`. The single-``PUT``
    #: path streams an un-replayable body and is always sent without retry.
    part_retry: Optional[Retry] = None


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
    """Storage accepted a part ``PUT`` but returned no ``ETag`` header, so the
    part cannot be finalized.
    """

    def __init__(self, *, part_number: int) -> None:
        self.part_number = part_number
        super().__init__(
            f"storage returned no ETag for part {part_number}; cannot finalize"
        )


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
                _STORAGE_POOL = urllib3.PoolManager()
    return _STORAGE_POOL


def default_part_retry() -> Retry:
    """The default retry policy for multipart part ``PUT`` s.

    A part ``PUT`` is idempotent — storage overwrites a part by number — so a
    retried part cannot corrupt the upload. Retry connection errors and the
    transient 429/5xx statuses storage may return under load. The single-``PUT``
    path streams an un-replayable body and so is always sent without retry.
    Override per upload via :attr:`UploadOptions.part_retry`.
    """
    return Retry(
        total=3,
        backoff_factor=0.2,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"PUT"}),
        raise_on_status=False,
    )


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
    if status >= 400:
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

    def readable(self) -> bool:
        return True

    def readinto(self, b: Any) -> int:
        chunk = self._file.read(len(b))
        if not chunk:
            return 0
        n = len(chunk)
        b[:n] = chunk
        self._done = min(self._done + n, self._total)
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
            parts = self._upload_multipart(session, src, total, cap, retry, progress)
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
        #
        # Finalize is exactly-once on the server. It is safe under the SDK's
        # DEFAULT retry policy: that policy does no status retries (status=0), and
        # urllib3 gates read-error retries (which include any ProtocolError, e.g.
        # a post-response reset) by allowed_methods, which excludes POST — so a
        # finalize the server already processed is never replayed. Only a
        # pre-response reset (server did no work) is retried, which is safe. NOTE:
        # a caller who overrides Configuration.retries with a policy that retries
        # POST on a status/read error could double-finalize and see a spurious
        # "already finalized" error; the default is the safe path.
        if parts is None:
            finalize_body = FinalizeUploadRequest()
        else:
            finalize_body = FinalizeUploadRequest(parts=parts)
        return self.finalize_upload_handler(
            session.upload_id,
            session.finalize_token,
            finalize_body,
            _request_timeout=_request_timeout,
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
        if isinstance(body, (bytes, bytearray)):
            # bytes go through the generated serialize + transport unchanged;
            # urllib3 sets Content-Length from the buffer length automatically.
            data = bytes(body)
            params = self._upload_file_serialize(
                body=data,
                _request_auth=None,
                _content_type=content_type,
                _headers=None,
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
        headers: Optional[Dict[str, str]] = (
            {"Content-Length": str(content_length)} if content_length is not None else None
        )
        method, url, header_params, _body, _post = self._upload_file_serialize(
            body=None,
            _request_auth=None,
            _content_type=content_type,
            _headers=headers,
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
    ) -> List[FinalizeUploadPart]:
        """Multipart path: slice the file into ``part_size``-byte chunks (the
        last is the remainder), ``PUT`` each chunk to its ``part_urls[i - 1]``
        with bounded concurrency, and collect ``(part_number, e_tag)`` per part.

        Returns the parts sorted ascending by part number, ready for finalize.
        """
        part_urls = session.part_urls
        part_size = session.part_size
        if not part_urls:
            raise MalformedSessionError("multipart upload missing `part_urls`")
        if part_size is None or part_size <= 0:
            raise MalformedSessionError(
                f"multipart upload has invalid `part_size` {part_size!r}"
            )

        # The URL count must match the number of `part_size`-byte chunks the file
        # splits into (last is the remainder). A mismatch means a session
        # inconsistent with our declared size, so fail loudly.
        expected_parts = max(-(-total // part_size), 1)  # ceil, at least 1
        if len(part_urls) != expected_parts:
            raise MalformedSessionError(
                f"multipart upload returned {len(part_urls)} part URLs but the "
                f"file ({total} bytes) splits into {expected_parts} parts of "
                f"{part_size} bytes"
            )

        in_flight = effective_in_flight(max_concurrency, part_size)
        done = [0]  # boxed running byte total; guarded by `lock`
        lock = threading.Lock()

        def upload_part(index: int) -> FinalizeUploadPart:
            part_number = index + 1
            offset = index * part_size
            length = min(part_size, total - offset)
            chunk = src.read_range(offset, length)
            response = _put_to_storage(
                part_urls[index],
                chunk,
                _storage_headers(session.headers, length),
                retries=part_retry,
                part_number=part_number,
            )
            etag = response.headers.get("ETag")
            if not etag:
                raise MissingETagError(part_number=part_number)
            if progress is not None:
                with lock:
                    done[0] = min(done[0] + length, total)
                    current = done[0]
                progress(current, total)
            return FinalizeUploadPart(e_tag=etag, part_number=part_number)

        results: List[Optional[FinalizeUploadPart]] = [None] * len(part_urls)
        executor = ThreadPoolExecutor(max_workers=in_flight)
        try:
            futures = {
                executor.submit(upload_part, i): i for i in range(len(part_urls))
            }
            # Surface the first failure as soon as it lands rather than waiting
            # for in-flight stragglers to drain. A part PUT is idempotent, so any
            # straggler still running when we bail does no harm.
            for future in as_completed(futures):
                exc = future.exception()
                if exc is not None:
                    raise exc
                results[futures[future]] = future.result()
        finally:
            # cancel_futures drops parts that have not started; already-running
            # ones can't be cancelled (threads) but we no longer wait on them.
            executor.shutdown(wait=False, cancel_futures=True)

        # results is indexed by 0-based part position, so it is already ascending
        # by part_number with no duplicates.
        return [part for part in results if part is not None]


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
    """A user-owned, seekable binary file object. A lock serializes the
    seek+read of each part (cheap, in-memory) so concurrent part tasks never
    corrupt the shared cursor; the slow ``PUT`` s still run concurrently. The
    file object is never closed (the caller owns it).
    """

    def __init__(self, fileobj: BinaryIO, size: int) -> None:
        self._file = fileobj
        self.size = size
        self._lock = threading.Lock()

    def read_range(self, offset: int, length: int) -> bytes:
        with self._lock:
            self._file.seek(offset)
            return self._file.read(length)

    @contextmanager
    def reader(self) -> Iterator[BinaryIO]:
        self._file.seek(0)
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
        if size is None:
            current = source.tell()
            size = source.seek(0, io.SEEK_END) - current
            source.seek(current)
        return _FileObjSource(source, size)
    raise TypeError(
        f"upload_file accepts a path, bytes, or a seekable binary file object, "
        f"not {type(source).__name__}. (Did you mean the generated "
        f"hotdata.api.uploads_api.UploadsApi.upload_file(body=...) raw op, or "
        f"upload_stream?)"
    )


__all__ = [
    "DEFAULT_MAX_CONCURRENCY",
    "DEFAULT_PART_SIZE",
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
