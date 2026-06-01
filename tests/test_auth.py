"""Unit tests for hotdata._auth._TokenManager.

These tests exercise the transparent JWT-exchange logic in complete isolation
from the network. Every test injects a *fake pool* via the documented
``_TokenManager(credential, configuration, pool=...)`` parameter, so no real
``urllib3.PoolManager`` is ever built and no socket is ever opened.

They verify the pinned public contract:

* first mint     -- an opaque (non-JWT) credential POSTs an ``api_token`` grant
                    to ``/v1/auth/jwt`` (form-encoded, correct Content-Type and
                    ``client_id``) and returns the minted ``access_token``;
* cache hit      -- a second ``bearer_value()`` within TTL does not re-hit the
                    pool;
* near-expiry    -- with < ``_LEEWAY`` seconds of life left and a refresh token
                    held, a ``refresh_token`` grant is POSTed;
* refresh fail   -- a non-200 refresh falls back to a fresh ``api_token`` mint;
* ``eyJ`` pass   -- a credential starting with ``eyJ`` is returned unchanged and
                    the pool is never called;
* exchange error -- a non-200 ``api_token`` mint raises ``TokenExchangeError``;
* opt-out        -- ``HOTDATA_DISABLE_JWT_EXCHANGE`` returns the credential as-is;
* concurrency    -- N racing threads cause exactly one mint (single-flight);
* deepcopy       -- a ``Configuration``/manager round-trips through deepcopy
                    despite the lock+pool, and the copy still mints.
"""

from __future__ import annotations

import copy
import json
import threading
import time
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs

import pytest

from hotdata import Configuration
from hotdata._auth import (
    _CLIENT_ID,
    _LEEWAY,
    TokenExchangeError,
    _TokenManager,
    _pool_from_config,
)


# --------------------------------------------------------------------------
# Test doubles
# --------------------------------------------------------------------------


class _FakeResponse:
    """Minimal stand-in for a urllib3.HTTPResponse.

    ``_TokenManager._mint`` only reads ``.status`` and ``.data`` (the latter
    being raw JSON bytes), so that is all we model.
    """

    def __init__(self, status: int, payload: Any):
        self.status = status
        if isinstance(payload, (bytes, bytearray)):
            self.data = bytes(payload)
        else:
            self.data = json.dumps(payload).encode()


class _FakePool:
    """Records every ``request(...)`` call and returns scripted responses.

    Each call pops the next response from ``responses``; if the list is
    exhausted the last response is reused (handy for "always succeeds" cases).
    A ``pre_request`` hook lets concurrency tests slow the first mint down to
    force a thread race.
    """

    def __init__(self, responses: List[_FakeResponse], pre_request=None):
        self._responses = list(responses)
        self.calls: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self._pre_request = pre_request

    def request(
        self,
        method: str,
        url: str,
        body: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> _FakeResponse:
        if self._pre_request is not None:
            self._pre_request()
        with self._lock:
            self.calls.append(
                {
                    "method": method,
                    "url": url,
                    "body": body,
                    "headers": dict(headers or {}),
                    "timeout": timeout,
                }
            )
            if len(self._responses) > 1:
                return self._responses.pop(0)
            return self._responses[0]


def _config(host: str = "https://api.hotdata.test") -> Configuration:
    """Build a Configuration exactly the way a user would."""
    return Configuration(host=host, api_key="hd_unused", workspace_id="ws_test")


def _mint_response(
    access_token: str = "eyJ.minted.jwt",
    *,
    refresh_token: Optional[str] = "rt_opaque",
    expires_in: int = 300,
) -> _FakeResponse:
    payload: Dict[str, Any] = {
        "access_token": access_token,
        "token_type": "Bearer",
        "scope": "permission:read_write",
    }
    if refresh_token is not None:
        payload["refresh_token"] = refresh_token
    if expires_in is not None:
        payload["expires_in"] = expires_in
    return _FakeResponse(200, payload)


def _form(body: Any) -> Dict[str, List[str]]:
    """Decode an x-www-form-urlencoded request body into a dict."""
    if isinstance(body, (bytes, bytearray)):
        body = body.decode()
    return parse_qs(body)


def _bearer_from(auth: Dict[str, Any]) -> str:
    """Pull the ``Authorization: Bearer ...`` value out of auth_settings()."""
    for setting in auth.values():
        value = str(setting.get("value", ""))
        if value.startswith("Bearer "):
            return value
    raise AssertionError(f"no Bearer auth setting found in {auth!r}")


# --------------------------------------------------------------------------
# First mint
# --------------------------------------------------------------------------


def test_first_mint_posts_api_token_grant() -> None:
    pool = _FakePool([_mint_response(access_token="eyJ.first.jwt")])
    cfg = _config()
    mgr = _TokenManager("hd_secret_token", cfg, pool=pool)

    token = mgr.bearer_value()

    assert token == "eyJ.first.jwt"
    assert len(pool.calls) == 1

    call = pool.calls[0]
    assert call["method"] == "POST"
    assert call["url"] == "https://api.hotdata.test/v1/auth/jwt"
    assert call["headers"]["Content-Type"] == "application/x-www-form-urlencoded"

    form = _form(call["body"])
    assert form["grant_type"] == ["api_token"]
    assert form["api_token"] == ["hd_secret_token"]
    assert form["client_id"] == [_CLIENT_ID]
    assert _CLIENT_ID == "hotdata-python-sdk"
    # The raw API token must never leak into the URL or headers.
    assert "hd_secret_token" not in call["url"]


def test_host_read_lazily_and_trailing_slash_stripped() -> None:
    """Host is read at mint time (so a late ``config.host = ...`` is honored)
    and a trailing slash is trimmed before composing the endpoint."""
    pool = _FakePool([_mint_response()])
    cfg = _config(host="https://placeholder.invalid")
    mgr = _TokenManager("hd_secret_token", cfg, pool=pool)

    # Reconfigure host after the manager was constructed.
    cfg.host = "https://late.hotdata.test/"
    mgr.bearer_value()

    assert pool.calls[0]["url"] == "https://late.hotdata.test/v1/auth/jwt"


# --------------------------------------------------------------------------
# Cache hit
# --------------------------------------------------------------------------


def test_second_call_within_ttl_is_cache_hit() -> None:
    pool = _FakePool([_mint_response(access_token="eyJ.cached.jwt", expires_in=300)])
    mgr = _TokenManager("hd_secret_token", _config(), pool=pool)

    first = mgr.bearer_value()
    second = mgr.bearer_value()

    assert first == second == "eyJ.cached.jwt"
    # The cached JWT is reused; the pool is hit exactly once.
    assert len(pool.calls) == 1


# --------------------------------------------------------------------------
# Near-expiry refresh
# --------------------------------------------------------------------------


def test_near_expiry_uses_refresh_token_grant() -> None:
    # First mint returns a token expiring inside the leeway window, plus a
    # refresh token. The next bearer_value() must refresh rather than re-mint.
    short_lived = _mint_response(
        access_token="eyJ.short.jwt",
        refresh_token="rt_first",
        expires_in=_LEEWAY - 5,  # already inside the refresh window
    )
    refreshed = _mint_response(
        access_token="eyJ.refreshed.jwt",
        refresh_token="rt_second",
        expires_in=300,
    )
    pool = _FakePool([short_lived, refreshed])
    mgr = _TokenManager("hd_secret_token", _config(), pool=pool)

    assert mgr.bearer_value() == "eyJ.short.jwt"
    assert mgr.bearer_value() == "eyJ.refreshed.jwt"

    assert len(pool.calls) == 2
    refresh_form = _form(pool.calls[1]["body"])
    assert refresh_form["grant_type"] == ["refresh_token"]
    assert refresh_form["refresh_token"] == ["rt_first"]
    assert refresh_form["client_id"] == [_CLIENT_ID]
    # A refresh grant must not carry the raw API token.
    assert "api_token" not in refresh_form


# --------------------------------------------------------------------------
# Refresh failure -> re-mint
# --------------------------------------------------------------------------


def test_refresh_failure_falls_back_to_api_token_mint() -> None:
    short_lived = _mint_response(
        access_token="eyJ.short.jwt",
        refresh_token="rt_doomed",
        expires_in=_LEEWAY - 5,
    )
    refresh_fail = _FakeResponse(400, {"error": "invalid_grant"})
    remint = _mint_response(access_token="eyJ.reminted.jwt", expires_in=300)
    pool = _FakePool([short_lived, refresh_fail, remint])
    mgr = _TokenManager("hd_secret_token", _config(), pool=pool)

    assert mgr.bearer_value() == "eyJ.short.jwt"
    # Second call: refresh 400 -> fall back to api_token mint.
    assert mgr.bearer_value() == "eyJ.reminted.jwt"

    assert len(pool.calls) == 3
    assert _form(pool.calls[1]["body"])["grant_type"] == ["refresh_token"]
    remint_form = _form(pool.calls[2]["body"])
    assert remint_form["grant_type"] == ["api_token"]
    assert remint_form["api_token"] == ["hd_secret_token"]


# --------------------------------------------------------------------------
# eyJ pass-through
# --------------------------------------------------------------------------


def test_jwt_credential_is_passed_through_unchanged() -> None:
    raw_jwt = "eyJhbGciOiJSUzI1NiJ9.payload.signature"
    pool = _FakePool([_mint_response()])
    mgr = _TokenManager(raw_jwt, _config(), pool=pool)

    assert mgr.bearer_value() == raw_jwt
    # A credential already shaped like a JWT must never be exchanged.
    assert pool.calls == []


# --------------------------------------------------------------------------
# Exchange error
# --------------------------------------------------------------------------


def test_non_200_api_token_mint_raises_token_exchange_error() -> None:
    pool = _FakePool([_FakeResponse(401, {"error": "invalid_grant"})])
    mgr = _TokenManager("hd_bad_token", _config(), pool=pool)

    with pytest.raises(TokenExchangeError):
        mgr.bearer_value()

    assert len(pool.calls) == 1
    assert _form(pool.calls[0]["body"])["grant_type"] == ["api_token"]


# --------------------------------------------------------------------------
# Opt-out
# --------------------------------------------------------------------------


def test_opt_out_env_var_returns_credential_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HOTDATA_DISABLE_JWT_EXCHANGE", "1")
    pool = _FakePool([_mint_response()])
    mgr = _TokenManager("hd_secret_token", _config(), pool=pool)

    assert mgr.bearer_value() == "hd_secret_token"
    assert pool.calls == []


# --------------------------------------------------------------------------
# Concurrency: single-flight mint
# --------------------------------------------------------------------------


def test_concurrent_callers_trigger_exactly_one_mint() -> None:
    n_threads = 16
    start = threading.Barrier(n_threads)

    # Slow the in-flight mint so all threads pile up on the lock and would each
    # mint if single-flight were broken.
    def slow() -> None:
        time.sleep(0.05)

    pool = _FakePool(
        [_mint_response(access_token="eyJ.single.jwt", expires_in=300)],
        pre_request=slow,
    )
    mgr = _TokenManager("hd_secret_token", _config(), pool=pool)

    results: List[str] = []
    results_lock = threading.Lock()

    def worker() -> None:
        start.wait()
        value = mgr.bearer_value()
        with results_lock:
            results.append(value)

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(results) == n_threads
    assert set(results) == {"eyJ.single.jwt"}
    # The decisive assertion: only one network mint happened despite the race.
    assert len(pool.calls) == 1


# --------------------------------------------------------------------------
# Deepcopy round-trip (the lock + pool gotcha)
# --------------------------------------------------------------------------


def test_configuration_deepcopy_round_trip() -> None:
    """``copy.deepcopy`` of a Configuration carrying a token manager must not
    choke on the manager's lock/pool, and the copy must be an independent
    object with its own freshly rebuilt manager.

    The copy's manager is rebuilt from the deepcopy-safe credential string (the
    lock + pool are never deep-copied), so we assert on that rather than reading
    ``api_key`` -- which would trigger a real network exchange."""
    original = Configuration(api_key="hd_x")

    duplicate = copy.deepcopy(original)

    assert duplicate is not original
    # Each Configuration carries its own manager; the copy's was rebuilt, not
    # the same object (which would share the original's lock/pool).
    assert duplicate._token_manager is not None
    assert duplicate._token_manager is not original._token_manager
    # The manager is bound to the copy (so it reads the copy's host at mint
    # time) and the credential survived the round-trip.
    assert duplicate._token_manager._config is duplicate
    assert duplicate._token_manager._credential == "hd_x"


def test_deepcopied_manager_credential_still_mints() -> None:
    """A token manager reconstructed from a deepcopy-safe credential still
    produces a working bearer value, and the two managers are distinct."""
    cfg = _config()
    pool_a = _FakePool([_mint_response(access_token="eyJ.a.jwt")])
    mgr_a = _TokenManager("hd_secret_token", cfg, pool=pool_a)

    # Mimic the __deepcopy__ contract: rebuild from the credential string
    # rather than deep-copying the lock/pool.
    pool_b = _FakePool([_mint_response(access_token="eyJ.b.jwt")])
    mgr_b = _TokenManager("hd_secret_token", copy.deepcopy(cfg), pool=pool_b)

    assert mgr_a is not mgr_b
    assert mgr_a.bearer_value() == "eyJ.a.jwt"
    assert mgr_b.bearer_value() == "eyJ.b.jwt"
    assert len(pool_a.calls) == 1
    assert len(pool_b.calls) == 1


# --------------------------------------------------------------------------
# Opaque (non-JWT) credentials are exchanged -- the prefix is not gated
# --------------------------------------------------------------------------


def test_bare_hex_token_is_exchanged() -> None:
    """Hotdata API tokens are bare hex with no ``hd_`` prefix (the prefix in
    the docs is cosmetic and not enforced by the server). Any opaque, non-JWT
    credential must therefore be exchanged, not passed through."""
    raw = "8a4bfd9cfa6926344f770d6b9a093c2b559dafc4de2a69137acb93e7e9821c7b"
    pool = _FakePool([_mint_response(access_token="eyJ.minted.jwt")])
    mgr = _TokenManager(raw, _config(), pool=pool)

    assert mgr.bearer_value() == "eyJ.minted.jwt"
    assert len(pool.calls) == 1
    assert _form(pool.calls[0]["body"])["api_token"] == [raw]


def test_configuration_exchanges_bare_token_then_opt_out_passes_through(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """End-to-end at the Configuration level: a bare token is exchanged so
    ``auth_settings()`` carries the minted JWT; with the opt-out env var set the
    raw token is sent unchanged (the arrow-test style dummy-key setup)."""
    raw = "8a4bfd9c0bare0token"

    # Exchange path: auth_settings() carries the minted JWT, not the raw token.
    pool = _FakePool([_mint_response(access_token="eyJ.live.jwt")])
    cfg = Configuration(host="https://api.hotdata.test", api_key=raw)
    cfg._token_manager._pool = pool
    assert _bearer_from(cfg.auth_settings()) == "Bearer eyJ.live.jwt"
    assert len(pool.calls) == 1

    # Opt-out path: same raw token, exchange disabled -> sent as-is, no mint.
    monkeypatch.setenv("HOTDATA_DISABLE_JWT_EXCHANGE", "1")
    pool2 = _FakePool([_mint_response()])
    cfg2 = Configuration(host="https://api.hotdata.test", api_key=raw)
    cfg2._token_manager._pool = pool2
    assert _bearer_from(cfg2.auth_settings()) == f"Bearer {raw}"
    assert pool2.calls == []


# --------------------------------------------------------------------------
# Configuration.api_key property + auth_settings() end-to-end
# --------------------------------------------------------------------------


def test_configuration_api_key_property_and_auth_settings_use_jwt() -> None:
    """The whole point of the design: ``Configuration.api_key`` returns a live
    JWT and ``auth_settings()`` assembles ``Authorization: Bearer <jwt>`` from
    it -- the regen-critical path that must keep working."""
    pool = _FakePool([_mint_response(access_token="eyJ.live.jwt", expires_in=300)])
    cfg = _config()
    cfg._token_manager = _TokenManager("hd_secret_token", cfg, pool=pool)

    assert cfg.api_key == "eyJ.live.jwt"
    assert _bearer_from(cfg.auth_settings()) == "Bearer eyJ.live.jwt"
    # Property getter + auth_settings together mint once and then cache.
    assert len(pool.calls) == 1


# --------------------------------------------------------------------------
# _pool_from_config mirrors rest.py's TLS/SNI handling
# --------------------------------------------------------------------------


def test_pool_from_config_honors_assert_hostname_and_sni() -> None:
    """A user who sets ``assert_hostname`` (corporate MITM) or
    ``tls_server_name`` (custom SNI) must have those applied to the exchange
    pool too, or the token call silently fails while normal calls work."""
    cfg = _config()
    cfg.assert_hostname = False
    cfg.tls_server_name = "sni.internal.test"

    pool = _pool_from_config(cfg)
    kw = pool.connection_pool_kw

    assert kw.get("assert_hostname") is False
    assert kw.get("server_hostname") == "sni.internal.test"


def test_pool_from_config_omits_hostname_args_when_unset() -> None:
    """When the user has not customized them, the args are absent (so urllib3
    uses its defaults) -- mirroring rest.py's conditional adds."""
    pool = _pool_from_config(_config())
    kw = pool.connection_pool_kw

    assert "assert_hostname" not in kw
    assert "server_hostname" not in kw


# --------------------------------------------------------------------------
# Malformed (non-JSON) success body
# --------------------------------------------------------------------------


def test_non_json_success_body_raises_token_exchange_error() -> None:
    """A 200 with a non-JSON body (e.g. a misrouted health page) surfaces as a
    clear TokenExchangeError rather than a bare JSONDecodeError."""
    pool = _FakePool([_FakeResponse(200, b"<html>not json</html>")])
    mgr = _TokenManager("hd_secret_token", _config(), pool=pool)

    with pytest.raises(TokenExchangeError):
        mgr.bearer_value()
