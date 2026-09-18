"""The SDK's default ``User-Agent``.

The generator's default is ``OpenAPI-Generator/1.0.0/python``, which identifies
neither the SDK nor its version — server-side telemetry cannot tell a hotdata
client from any other generated client, let alone one release from another.

openapi-generator *does* expose an ``httpUserAgent`` property for this, but it
bakes a literal string in at **generation** time. Regeneration is driven by
OpenAPI spec changes, not by releases, so a baked version string reports
whatever the version happened to be at the last regen — it would go stale
silently and misattribute traffic, which is worse than the generic default. The
version is therefore resolved at import time from installed package metadata,
the same source :mod:`hotdata.__init__` uses for ``__version__``.

This lives outside the generated modules (see ``.openapi-generator-ignore``) so
a regeneration cannot overwrite it; ``scripts/patch_request_defaults.py`` only
has to re-point ``ApiClient`` at the constant.
"""

from __future__ import annotations

import importlib.metadata
import platform

import urllib3


def _default_user_agent() -> str:
    """``hotdata-python/<version> (Python/<py>; urllib3/<urllib3>)``.

    The runtime versions ride along because the transport stack is where
    client-side failures usually originate: knowing which urllib3 a bug report
    came from is the difference between reproducing a problem and guessing.
    """
    try:
        sdk_version = importlib.metadata.version("hotdata")
    except importlib.metadata.PackageNotFoundError:
        # Running from a source checkout without an install.
        sdk_version = "0.0.0+unknown"
    return (
        f"hotdata-python/{sdk_version} "
        f"(Python/{platform.python_version()}; urllib3/{urllib3.__version__})"
    )


#: Sent as ``User-Agent`` on every request. ``ApiClient.user_agent`` still
#: overrides it per client, which is the supported way for an application to
#: identify itself.
USER_AGENT = _default_user_agent()


__all__ = ["USER_AGENT", "_default_user_agent"]
