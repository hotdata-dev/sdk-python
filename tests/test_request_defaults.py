"""Transport-level request defaults the SDK puts on every call.

Two things the generated client left on urllib3's defaults, both observable by
the server and neither of them what an SDK wants:

* **Compression.** urllib3 sets ``Accept-Encoding: identity`` on every
  connection it opens. That is not "no preference" — it is an explicit request
  *not* to compress, and a spec-compliant server honors it. Every JSON response
  (query results, table listings, job payloads) therefore came back
  uncompressed. The fix advertises ``urllib3.util.request.ACCEPT_ENCODING``,
  which is exactly the set the *installed* urllib3 can transparently decode, so
  the SDK can never be handed a body it cannot read.

* **User-Agent.** ``OpenAPI-Generator/1.0.0/python`` identifies neither the SDK
  nor its version, so server-side telemetry cannot tell one client release from
  another — or a hotdata client from any other generated client.

These tests drive the real ``ApiClient`` against a real socket and assert on
what the *server* saw, because the header is only interesting on the wire: a
unit assertion against ``default_headers`` would have passed both before and
after the fix.
"""

from __future__ import annotations

import gzip
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

import pytest
from urllib3.util.request import ACCEPT_ENCODING

from hotdata.api_client import ApiClient
from hotdata.configuration import Configuration


class _RecordingHandler(BaseHTTPRequestHandler):
    """Records the request headers, then replies with a gzipped JSON body.

    The reply is compressed unconditionally — the point is to prove the client
    both *asks* for compression and transparently *decodes* the result, so the
    body is gzipped regardless of what the client advertised.
    """

    protocol_version = "HTTP/1.1"
    payload = {"rows": ["value"] * 64}

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        self.server.seen_headers = {  # type: ignore[attr-defined]
            key.lower(): value for key, value in self.headers.items()
        }
        # get_all, not get: a case-sensitive default check produces two
        # Accept-Encoding header *lines*, which a dict of headers would hide.
        self.server.seen_encodings = (  # type: ignore[attr-defined]
            self.headers.get_all("Accept-Encoding") or []
        )
        body = gzip.compress(json.dumps(self.payload).encode())
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args: Any) -> None:
        """Silence the stderr request log."""


class _QuietServer(HTTPServer):
    """An HTTPServer that does not log the teardown reset.

    The client holds a keep-alive connection open and drops it when the
    ``ApiClient`` context manager exits, which the handler thread sees as a
    reset. That is the expected end of the test, not a failure, so it should
    not print a traceback.
    """

    def handle_error(self, request: Any, client_address: Any) -> None:
        """Swallow the expected connection reset at teardown."""


@pytest.fixture
def server():
    """A local HTTP server that records what the client sent."""
    httpd = _QuietServer(("127.0.0.1", 0), _RecordingHandler)
    httpd.seen_headers = {}  # type: ignore[attr-defined]
    httpd.seen_encodings = []  # type: ignore[attr-defined]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield httpd
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


@pytest.fixture
def client(server):
    """A real ApiClient pointed at the recording server."""
    host = f"http://127.0.0.1:{server.server_address[1]}"
    with ApiClient(Configuration(host=host)) as api_client:
        yield api_client


def _get(client: ApiClient, server: HTTPServer, headers: dict[str, str] | None = None) -> Any:
    """Issue a GET through the full client stack and return the response."""
    host = f"http://127.0.0.1:{server.server_address[1]}"
    header_params = dict(client.default_headers)
    header_params.update(headers or {})
    return client.call_api("GET", f"{host}/v1/results", header_params=header_params)


def test_requests_compressed_responses(client, server):
    """The SDK asks for compression instead of urllib3's `identity` opt-out."""
    _get(client, server)

    accept_encoding = server.seen_headers["accept-encoding"]
    assert accept_encoding != "identity"
    assert "gzip" in accept_encoding


def test_advertises_only_encodings_urllib3_can_decode(client, server):
    """Never advertise an encoding the installed urllib3 cannot decode.

    ``ACCEPT_ENCODING`` is built from the codecs actually available at import
    time (brotli and zstd are optional), so pinning to it — rather than to a
    hardcoded string — is what guarantees a server can never pick an encoding
    that would come back as undecodable bytes.
    """
    _get(client, server)

    assert server.seen_headers["accept-encoding"] == ACCEPT_ENCODING


def test_compressed_response_is_transparently_decoded(client, server):
    """Asking for compression must not change what callers receive."""
    response = _get(client, server)

    assert json.loads(response.read()) == _RecordingHandler.payload


def test_caller_can_override_accept_encoding(client, server):
    """An explicit per-request encoding wins over the default.

    A response that is already compressed end-to-end (an Arrow IPC stream with
    LZ4/ZSTD record batches, say) gains nothing from a second pass, so the
    default must be a floor, not a ceiling.
    """
    _get(client, server, headers={"Accept-Encoding": "identity"})

    assert server.seen_headers["accept-encoding"] == "identity"


def test_user_agent_identifies_the_sdk_and_version(client, server):
    """Server-side telemetry must be able to attribute traffic to a release."""
    from hotdata.api_client import USER_AGENT

    _get(client, server)

    user_agent = server.seen_headers["user-agent"]
    assert user_agent == USER_AGENT
    assert "OpenAPI-Generator" not in user_agent
    assert user_agent.startswith("hotdata-python/")


def test_user_agent_remains_caller_settable(client, server):
    """The generator's `user_agent` setter stays the supported override."""
    client.user_agent = "my-app/2.0"

    _get(client, server)

    assert server.seen_headers["user-agent"] == "my-app/2.0"


def test_lowercase_override_is_not_duplicated(client, server):
    """A differently-cased opt-out must suppress the default, not duplicate it.

    HTTP header names are case-insensitive and nothing stops a caller from
    passing ``accept-encoding``. A case-*sensitive* default check leaves both
    keys in the dict, urllib3 emits one header line per key, and the server
    receives ``identity`` *and* the compressed set — so the documented
    per-request opt-out is silently lost. urllib3 itself lowercases header
    names before deciding whether to add its own ``Accept-Encoding``; this
    matches that.
    """
    _get(client, server, headers={"accept-encoding": "identity"})

    assert server.seen_encodings == ["identity"]
