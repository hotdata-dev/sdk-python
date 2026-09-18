#!/usr/bin/env python3
"""Re-apply the SDK's transport request defaults after OpenAPI regeneration.

Two defaults the generator leaves on urllib3's (server-observable) behavior:

* ``Accept-Encoding``: urllib3 puts ``identity`` on every connection, which
  asks the server *not* to compress. We advertise
  ``urllib3.util.request.ACCEPT_ENCODING`` instead — exactly the codecs the
  installed urllib3 can transparently decode.
* ``User-Agent``: ``OpenAPI-Generator/1.0.0/python`` identifies neither the SDK
  nor its version, so server-side telemetry cannot attribute traffic.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def patch_accept_encoding() -> None:
    """Advertise compression on every request made through RESTClientObject."""
    path = ROOT / "hotdata" / "rest.py"
    src = path.read_text()

    if "ACCEPT_ENCODING" in src:
        return

    import_needle = "import urllib3\n"
    import_replacement = "import urllib3\nfrom urllib3.util.request import ACCEPT_ENCODING\n"
    if import_needle not in src:
        sys.exit(f"Failed to patch {path}: urllib3 import anchor not found")
    src = src.replace(import_needle, import_replacement, 1)

    needle = "        post_params = post_params or {}\n        headers = headers or {}\n"
    replacement = (
        "        post_params = post_params or {}\n"
        "        headers = headers or {}\n\n"
        "        # Ask for compressed responses. urllib3 defaults every connection to\n"
        "        # `Accept-Encoding: identity`, which is not \"no preference\" but an\n"
        "        # explicit request *not* to compress, and a spec-compliant server\n"
        "        # honors it. ACCEPT_ENCODING is built from the codecs the installed\n"
        "        # urllib3 can actually decode (gzip/deflate, plus br/zstd when their\n"
        "        # backends are present), so the server can never negotiate an encoding\n"
        "        # that reaches us as undecodable bytes. urllib3 decodes the body\n"
        "        # transparently, so callers are unaffected.\n"
        "        #\n"
        "        # setdefault, not assignment: an operation whose payload is already\n"
        "        # compressed end-to-end can pass `identity` and stay in control.\n"
        "        headers.setdefault('Accept-Encoding', ACCEPT_ENCODING)\n"
    )
    if needle not in src:
        sys.exit(f"Failed to patch {path}: request() header anchor not found")
    src = src.replace(needle, replacement, 1)

    path.write_text(src)


def patch_user_agent() -> None:
    """Point ApiClient at the hand-maintained User-Agent constant.

    The string itself lives in ``hotdata/_useragent.py`` (generator-ignored), so
    this patch is just an import plus the assignment — two anchors instead of
    carrying the logic inside generated output.
    """
    path = ROOT / "hotdata" / "api_client.py"
    src = path.read_text()

    if "_useragent" in src:
        return

    import_needle = "from hotdata.api_response import ApiResponse, T as ApiResponseT\n"
    import_replacement = (
        "from hotdata.api_response import ApiResponse, T as ApiResponseT\n"
        "from hotdata._useragent import USER_AGENT\n"
    )
    if import_needle not in src:
        sys.exit(f"Failed to patch {path}: api_response import anchor not found")
    src = src.replace(import_needle, import_replacement, 1)

    ua_needle = "        self.user_agent = 'OpenAPI-Generator/1.0.0/python'\n"
    ua_replacement = "        self.user_agent = USER_AGENT\n"
    if ua_needle not in src:
        sys.exit(f"Failed to patch {path}: default User-Agent anchor not found")
    src = src.replace(ua_needle, ua_replacement, 1)

    path.write_text(src)


def main() -> None:
    patch_accept_encoding()
    patch_user_agent()


if __name__ == "__main__":
    main()
