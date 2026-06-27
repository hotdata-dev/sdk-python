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
* **Opt-out** -- if ``HOTDATA_DISABLE_JWT_EXCHANGE`` is set to an affirmative
  value (``1``/``true``/``yes``/``on``), the credential is always returned
  as-is (hard escape hatch for rollout); ``0``/``false``/empty do not opt out.
* **In-memory cache only** -- no disk writes. The server already de-duplicates
  mints (keyed by ``sha256(api_token)``), so per-process caching is sufficient.
* **Thread-safe** -- a :class:`threading.Lock` with single-flight mint covers
  the case where a shared ``ApiClient`` is hit from many threads at once.
* **Refresh, then re-mint** -- prefer the refresh token when available; on
  refresh failure, re-mint from the held API token (always possible since the
  SDK holds it). Matches the CLI.
* **Transient-failure retry** -- a momentary ``5xx`` or a transport error on the
  token endpoint is retried with bounded exponential backoff + jitter
  (``_MAX_ATTEMPTS`` total) before giving up, so a brief server-side blip does
  not fail the caller (#113). A ``4xx`` is never retried -- a bad/expired
  credential is not transient.
* **TLS/proxy reuse** -- the exchange call reuses the SDK's configured TLS,
  client cert and proxy settings (see :func:`_pool_from_config`) so it behaves
  like every other SDK request, with a bounded timeout so a stalled token
  endpoint fails fast instead of hanging every call.
"""

import json
import os
import random
import ssl
import threading
import time
from urllib.parse import urlencode

import urllib3

_LEEWAY = 30          # refresh when <30s of life remains
_TIMEOUT = 30.0       # seconds -- never let a stalled token endpoint hang every request
_CLIENT_ID = "hotdata-python-sdk"

# Bounded retry of *transient* token-exchange failures (#113). A momentary 5xx
# or a transport error (connection/read failure) on the token endpoint should
# not fail the caller outright -- an immediate re-attempt typically succeeds.
# We retry those, but never a 4xx (a bad/expired credential is not transient).
_MAX_ATTEMPTS = 3       # one initial attempt + up to two retries
_BACKOFF_BASE = 0.1     # seconds -- first retry waits ~this, doubling thereafter
_BACKOFF_MAX = 2.0      # cap on a single backoff so a flapping host can't stall us
_BACKOFF_JITTER = 0.5   # +/- fraction of jitter added to spread retries out

# Env var that disables exchange entirely. Used as a hard escape hatch during
# the rollout window and for local/dev setups. Only affirmative values opt out
# (see _DISABLE_VALUES) so that ``=0`` / ``=false`` do NOT silently disable it.
_DISABLE_ENV = "HOTDATA_DISABLE_JWT_EXCHANGE"
_DISABLE_VALUES = {"1", "true", "yes", "on"}

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
    if configuration.socket_options is not None:
        pool_args["socket_options"] = configuration.socket_options
    # `retries`/`maxsize` are intentionally not mirrored: urllib3's own Retry is
    # left at urllib3's default (it does not retry POST status codes anyway), so
    # we do not inherit the SDK's connection-reset retry here. Transient-failure
    # retry for the exchange is handled explicitly in `_TokenManager._exchange`
    # (5xx + transport errors, bounded backoff), where we can keep 4xx fatal.

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


def _is_transient_status(status):
    """True for HTTP statuses worth retrying (server-side, likely momentary).

    Only 5xx is transient: the request reached the server but it failed to
    handle it (e.g. a brief ``500``/``503``). A 4xx -- including ``400``/``401``
    from a bad or expired credential -- is a definitive rejection that a retry
    will not fix, so it is never retried.
    """
    return 500 <= status < 600


def _backoff_delay(attempt):
    """Seconds to sleep before retry number ``attempt`` (0 = first retry).

    Exponential growth from ``_BACKOFF_BASE`` (doubling per attempt) capped at
    ``_BACKOFF_MAX``, plus additive jitter in ``[0, _BACKOFF_JITTER * base]`` so
    concurrent clients retrying the same blip don't resynchronize into a thundering
    herd. Mirrors the Rust SDK's ``backoff_delay``.
    """
    base = min(_BACKOFF_BASE * (2 ** attempt), _BACKOFF_MAX)
    return base * (1 + _BACKOFF_JITTER * random.random())


class _TokenManager:
    """Exchanges an API token for short-lived JWTs and keeps them fresh.

    A credential that already looks like a JWT (``eyJ`` prefix) is passed
    through unchanged, as is any credential when
    ``HOTDATA_DISABLE_JWT_EXCHANGE`` is set; every other (opaque) API token is
    exchanged.
    """

    def __init__(self, credential, configuration, pool=None, sleep=None):
        self._credential = credential
        self._config = configuration      # read host + TLS lazily at mint time
        self._pool = pool                 # injected in tests; else built from config TLS
        self._sleep = sleep or time.sleep  # injected in tests so retry backoff is instant
        self._lock = threading.Lock()
        self._jwt = None
        self._exp = 0.0
        self._refresh = None

    @property
    def _needs_exchange(self):
        # Opt-out wins outright: an affirmative HOTDATA_DISABLE_JWT_EXCHANGE
        # (1/true/yes/on) means send the credential as-is, never touching the
        # token endpoint. Other values (incl. 0/false/empty) do not opt out.
        if os.environ.get(_DISABLE_ENV, "").strip().lower() in _DISABLE_VALUES:
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
        # Returns True on success. The refresh path is best-effort: ANY failure
        # -- a non-200, a transport error, or a malformed/missing-token body --
        # returns False so the caller re-mints from the held API token. An
        # api_token mint instead raises TokenExchangeError on any failure, since
        # there is no further fallback. Transient failures (5xx + transport
        # errors) are retried inside _exchange before either outcome.
        params["client_id"] = _CLIENT_ID
        is_refresh = params["grant_type"] == "refresh_token"
        try:
            data = self._exchange(params)
            token = data["access_token"]
            expires_in = float(data.get("expires_in", 300))
        except (
            TokenExchangeError,
            urllib3.exceptions.HTTPError,
            ValueError,
            TypeError,
            KeyError,
        ) as exc:
            if is_refresh:
                return False               # let caller re-mint from the API token
            if isinstance(exc, TokenExchangeError):
                raise
            raise TokenExchangeError(f"token exchange failed: {exc!r}") from exc
        self._jwt = token
        self._exp = time.time() + expires_in
        self._refresh = data.get("refresh_token") or self._refresh
        return True

    def _exchange(self, params):
        # POST the token-exchange request, retrying transient failures, and
        # return the parsed JSON body of the 200 response.
        #
        # Retries 5xx responses and transport errors (urllib3 HTTPError, e.g. a
        # connection/read failure) with bounded exponential backoff + jitter, up
        # to _MAX_ATTEMPTS total. A 4xx is returned immediately as a fatal
        # TokenExchangeError -- bad/expired credentials are not transient. Once
        # the budget is exhausted, the last failure is surfaced: a 5xx as a
        # TokenExchangeError preserving the status/body, a transport error as the
        # raised HTTPError (which _mint wraps). JSON/missing-token errors from
        # parsing a 200 body propagate unretried.
        pool = self._pool or _pool_from_config(self._config)   # reuses ssl_ca_cert/cert/proxy
        host = self._config.host.rstrip("/")                   # read host lazily -- may be set post-construct
        url = f"{host}/v1/auth/jwt"
        body = urlencode(params)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        for attempt in range(_MAX_ATTEMPTS):
            last = attempt == _MAX_ATTEMPTS - 1
            try:
                resp = pool.request(
                    "POST", url, body=body, headers=headers, timeout=_TIMEOUT
                )
            except urllib3.exceptions.HTTPError:
                # Transport-level failure (connection/read error): transient, but
                # don't retry past the budget -- re-raise for _mint to handle.
                if last:
                    raise
                self._sleep(_backoff_delay(attempt))
                continue
            if resp.status == 200:
                return json.loads(resp.data)
            if _is_transient_status(resp.status) and not last:
                self._sleep(_backoff_delay(attempt))
                continue
            # A 4xx, or a 5xx with the retry budget exhausted: fatal, surfacing
            # the last status/body.
            raise TokenExchangeError(
                f"token exchange failed: {resp.status} {resp.data[:200]!r}"
            )


__all__ = [
    "TokenExchangeError",
    "_TokenManager",
    "_CLIENT_ID",
    "_pool_from_config",
]
