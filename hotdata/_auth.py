"""Transparent API-token -> JWT exchange for the Hotdata Python SDK.

Hotdata is moving API authentication to short-lived JWTs. Users still configure
the SDK with their long-lived ``hd_`` API token, but every request should carry
a fresh JWT instead. This module is the hand-written, regeneration-immune piece
that makes that happen behind the scenes: :class:`_TokenManager` exchanges the
API token for a JWT at ``POST {host}/v1/auth/jwt`` and keeps it fresh, mirroring
the CLI's ``jwt.rs`` logic so the CLI and SDK behave identically.

OpenAPI Generator only rewrites the files it generates, so a hand-added module
like this one (precedent: :mod:`hotdata.arrow`) survives regeneration. It is
additionally listed in ``.openapi-generator-ignore`` as belt-and-suspenders.

Key behaviors:

* **Pass-through** -- a credential that already looks like a JWT (``eyJ``
  prefix, matching the Gateway's own ``^Bearer eyJ.*`` detection) is returned
  unchanged and never exchanged. Every other (opaque) credential is treated as
  an API token and exchanged; set ``HOTDATA_DISABLE_JWT_EXCHANGE`` to force a
  raw, non-JWT credential through as-is (local/dev setups, rollback).
* **Opt-out** -- if ``HOTDATA_DISABLE_JWT_EXCHANGE`` is set to any truthy value,
  the credential is always returned as-is (hard escape hatch for rollout).
* **In-memory cache only** -- no disk writes. The server already de-duplicates
  mints (keyed by ``sha256(api_token)``), so per-process caching is sufficient.
* **Thread-safe** -- a :class:`threading.Lock` with single-flight mint covers
  the case where a shared ``ApiClient`` is hit from many threads at once.
* **Refresh, then re-mint** -- prefer the refresh token when available; on
  refresh failure, re-mint from the held API token (always possible since the
  SDK holds it). Matches the CLI.
* **TLS/proxy reuse** -- the exchange call reuses the SDK's configured TLS,
  client cert and proxy settings (see :func:`_pool_from_config`) so it behaves
  like every other SDK request, with a bounded timeout so a stalled token
  endpoint fails fast instead of hanging every call.
"""

import json
import os
import ssl
import threading
import time
from urllib.parse import urlencode

import urllib3

_LEEWAY = 30          # refresh when <30s of life remains
_TIMEOUT = 30.0       # seconds -- never let a stalled token endpoint hang every request
_CLIENT_ID = "hotdata-python-sdk"

# Env var that disables exchange entirely (any truthy value). Used as a hard
# escape hatch during the rollout window and for local/dev setups.
_DISABLE_ENV = "HOTDATA_DISABLE_JWT_EXCHANGE"

# The SOCKS schemes urllib3 routes through SOCKSProxyManager rather than the
# plain ProxyManager. Mirrors hotdata/rest.py's SUPPORTED_SOCKS_PROXIES.
_SUPPORTED_SOCKS_PROXIES = {"socks5", "socks5h", "socks4", "socks4a"}


class TokenExchangeError(Exception):
    """Raised when an API token cannot be exchanged for a JWT.

    Surfacing ``invalid_grant`` (expired/revoked API token) here keeps the
    failure clear instead of a confusing downstream 401.
    """


def _is_socks_proxy_url(url):
    # Mirror hotdata/rest.py.is_socks_proxy_url so the exchange pool routes
    # SOCKS proxies the same way the generated REST client does.
    if url is None:
        return False
    split_section = url.split("://")
    if len(split_section) < 2:
        return False
    return split_section[0].lower() in _SUPPORTED_SOCKS_PROXIES


def _pool_from_config(configuration):
    """Build a urllib3 pool manager from the SDK's TLS/proxy configuration.

    Deliberately parallels ``RESTClientObject.__init__`` in
    :mod:`hotdata.rest` so the token-exchange call honors the same
    ``ssl_ca_cert`` / ``ca_cert_data`` / ``cert_file`` / ``key_file`` /
    ``proxy`` / ``verify_ssl`` settings as every other SDK request. We build a
    fresh, lightweight pool here rather than reaching into the ``ApiClient``'s
    REST client (which the ``Configuration`` does not hold a reference to).
    """
    # cert_reqs -- honor verify_ssl exactly as the generated client does.
    if configuration.verify_ssl:
        cert_reqs = ssl.CERT_REQUIRED
    else:
        cert_reqs = ssl.CERT_NONE

    pool_args = {
        "cert_reqs": cert_reqs,
        "ca_certs": configuration.ssl_ca_cert,
        "cert_file": configuration.cert_file,
        "key_file": configuration.key_file,
        "ca_cert_data": configuration.ca_cert_data,
    }
    # Mirror rest.py's hostname/SNI handling so the exchange call does not
    # silently fail for users who customize them (corporate MITM proxies set
    # assert_hostname; some gateways require an explicit tls_server_name/SNI).
    if configuration.assert_hostname is not None:
        pool_args["assert_hostname"] = configuration.assert_hostname
    if configuration.tls_server_name:
        pool_args["server_hostname"] = configuration.tls_server_name
    # `retries`/`maxsize` are intentionally not mirrored: the exchange is a
    # single bounded-timeout request that fails fast rather than retrying.

    if configuration.proxy:
        if _is_socks_proxy_url(configuration.proxy):
            from urllib3.contrib.socks import SOCKSProxyManager
            pool_args["proxy_url"] = configuration.proxy
            pool_args["headers"] = configuration.proxy_headers
            return SOCKSProxyManager(**pool_args)
        pool_args["proxy_url"] = configuration.proxy
        pool_args["proxy_headers"] = configuration.proxy_headers
        return urllib3.ProxyManager(**pool_args)

    return urllib3.PoolManager(**pool_args)


class _TokenManager:
    """Exchanges an API token for short-lived JWTs and keeps them fresh.

    A credential that already looks like a JWT (``eyJ`` prefix) is passed
    through unchanged, as is any credential when
    ``HOTDATA_DISABLE_JWT_EXCHANGE`` is set; every other (opaque) API token is
    exchanged.
    """

    def __init__(self, credential, configuration, pool=None):
        self._credential = credential
        self._config = configuration      # read host + TLS lazily at mint time
        self._pool = pool                 # injected in tests; else built from config TLS
        self._lock = threading.Lock()
        self._jwt = None
        self._exp = 0.0
        self._refresh = None

    @property
    def _needs_exchange(self):
        # Opt-out wins outright: any truthy HOTDATA_DISABLE_JWT_EXCHANGE means
        # send the credential as-is, never touching the token endpoint.
        if os.environ.get(_DISABLE_ENV):
            return False
        # A compact JWT always starts with "eyJ" (base64 of '{"'), matching the
        # Gateway's own ``^Bearer eyJ.*`` detection -- those already are what we
        # want on the wire, so pass them through. Everything else is an opaque
        # API token to be exchanged. (Hotdata API tokens are bare hex; the
        # ``hd_`` prefix seen in docs/comments is cosmetic and not enforced by
        # the server, so we must not gate on it.) Use HOTDATA_DISABLE_JWT_EXCHANGE
        # to force a raw, non-JWT credential through unchanged (local/dev).
        return isinstance(self._credential, str) and not self._credential.startswith("eyJ")

    def bearer_value(self):
        """Return a live JWT (exchanging + caching), or the credential as-is.

        Returns the credential unchanged when it is already a JWT or when
        exchange is disabled; otherwise returns a cached JWT, refreshing or
        re-minting it when it is within ``_LEEWAY`` seconds of expiry.
        """
        if not self._needs_exchange:
            return self._credential            # already a JWT (or opt-out) -> unchanged
        with self._lock:
            # Fast path: a still-valid cached JWT, no network call.
            if self._jwt and time.time() < self._exp - _LEEWAY:
                return self._jwt
            # Prefer the refresh token; on failure, drop it and re-mint below.
            if self._refresh and not self._mint(
                {"grant_type": "refresh_token", "refresh_token": self._refresh}
            ):
                self._refresh = None           # refresh failed -> fall through to re-mint
            # Re-mint from the held API token if we still lack a fresh JWT.
            if not self._jwt or time.time() >= self._exp - _LEEWAY:
                self._mint({"grant_type": "api_token", "api_token": self._credential})
            return self._jwt

    def _mint(self, params):
        # Returns True on success. A non-200 from a refresh returns False so the
        # caller can re-mint from the API token; a non-200 from an api_token
        # mint raises TokenExchangeError.
        params["client_id"] = _CLIENT_ID
        pool = self._pool or _pool_from_config(self._config)   # reuses ssl_ca_cert/cert/proxy
        host = self._config.host.rstrip("/")                   # read host lazily -- may be set post-construct
        resp = pool.request(
            "POST",
            f"{host}/v1/auth/jwt",
            body=urlencode(params),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=_TIMEOUT,
        )
        if resp.status != 200:
            if params["grant_type"] == "refresh_token":
                return False               # let caller re-mint from the API token
            raise TokenExchangeError(
                f"token exchange failed: {resp.status} {resp.data[:200]!r}"
            )
        try:
            data = json.loads(resp.data)
        except (ValueError, TypeError) as exc:
            raise TokenExchangeError(
                f"token exchange returned a non-JSON body: {resp.data[:200]!r}"
            ) from exc
        self._jwt = data["access_token"]
        self._exp = time.time() + data.get("expires_in", 300)
        self._refresh = data.get("refresh_token") or self._refresh
        return True


__all__ = [
    "TokenExchangeError",
    "_TokenManager",
    "_CLIENT_ID",
    "_pool_from_config",
]
