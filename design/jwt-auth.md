# Design: Transparent JWT exchange in the Python SDK

## Summary

Hotdata is moving API authentication to short-lived JWTs. Today the Python SDK
sends the user's long-lived API token (`hd_…`) directly as
`Authorization: Bearer <token>` on every request. This design makes the SDK
**transparently exchange that API token for a JWT** and use the JWT for
subsequent requests — with **zero changes to user code** and **without breaking
OpenAPI regeneration**.

Users continue to write exactly what they write today:

```python
configuration = hotdata.Configuration(api_key="hd_…", workspace_id="…")
with hotdata.ApiClient(configuration) as client:
    hotdata.WorkspacesApi(client).list_workspaces()   # JWT used under the hood
```

## Background: how auth works across the system

### Webapp (monopoly)

The API-token → JWT exchange is a custom OAuth 2.0 grant
(`authentication/grants.py`, `ApiTokenGrant`, a `ClientCredentialsGrant`
subclass) served by django-oauth-toolkit at `POST /o/token/`:

```
POST /o/token/
Content-Type: application/x-www-form-urlencoded

grant_type=api_token&api_token=hd_…&client_id=<public-client>
```

Response (standard OAuth token shape, already JSON):

```json
{
  "access_token": "<RS256 JWT>",
  "refresh_token": "<opaque>",
  "token_type": "Bearer",
  "expires_in": 300,
  "scope": "permission:read_write workspace:work_…"
}
```

- JWT access token TTL: **5 minutes** (300s).
- Refresh token TTL: **36 hours** for api_token-origin tokens.
- `client_id` is validated only as a *registered public client*
  (`grants.py` → `authenticate_client_id`); caller identity and scopes come
  entirely from the API token, not the client.
- The server already de-duplicates mints: the grant caches the JWT keyed by
  `sha256(api_token)` behind a `SET NX` lock, so a fleet of processes sharing
  one API token will not stampede `/o/token/`.

`/o/token/` is **not** a spec-mandated path — RFC 6749 leaves the token
endpoint URL to the deployment (discoverable via authorization-server
metadata). `/o/` is simply django-oauth-toolkit's default mount point.

### CLI (hotdata-cli, `jwt.rs`)

The CLI holds the `hd_` token, exchanges it once, caches the session in
`~/.hotdata/session.json`, and before every request runs
`ensure_access_token()`: return the cached JWT if it has >30s of life left,
otherwise refresh, otherwise re-mint from the API token. The API token never
goes on the wire after the first exchange. This SDK design intentionally
mirrors that logic so CLI and SDK behave identically.

### Backward compatibility (confirmed)

The Gateway routes `Authorization: Bearer eyJ…` (JWTs) to a JWT-validating
`SecurityPolicy` and `Bearer hd_…` (API tokens) through the existing
extAuth/DB path (`httproute-api-jwt.yaml`). **Both are accepted today**, so this
upgrade is non-breaking and can ship ahead of any JWT-only enforcement.
*("Once API tokens are fully deprecated, delete api-hotdata-route.")*

## Goals & constraints

1. **No user code change.** The public `Configuration(api_key=…)` surface is
   unchanged.
2. **Survive OpenAPI regeneration.** `configuration.py`, `api_client.py`, and
   `rest.py` are all regenerated; the design must not depend on hand-edits to
   generated output.
3. **Single host.** The SDK should only ever talk to its configured `host`
   (`api.hotdata.dev`), not a second OAuth host.
4. **Match the CLI's refresh semantics** for consistent behavior.

## Decisions

### Exchange endpoint: `POST {host}/v1/auth/jwt` — Gateway rewrite, no Django view

The exchange is exposed on the **api host** under the public `/v1` surface as
`/v1/auth/jwt`. (`/v1/auth/token` is already taken — it's the PKCE CLI-login
view that mints an *opaque* token — so the JWT-exchange path is `/v1/auth/jwt`,
parallel to the existing `/v1/auth/sandbox`.)

This is implemented **purely at the Gateway**, not as a new Django view:

- A new `HTTPRoute` on `api.hotdata.dev` matches `Exact: /v1/auth/jwt` and uses
  a `URLRewrite` (`ReplaceFullPath`) filter to rewrite the path to `/o/token/`,
  forwarding to `webapp:8000`.
- The route carries **no `SecurityPolicy`** — it must be reachable before the
  caller has a JWT (the `hd_` token in the request body is the credential,
  validated by Django's grant). This mirrors `api-auth-hotdata-route`, which
  already has no policy attached. SecurityPolicies are opt-in per route via
  `targetRef.name`, so an unattached route is genuinely public — not a gap.

```yaml
# infrastructure/kubernetes/base/gateway-api/httproute-api-jwt-exchange.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-jwt-exchange-hotdata-route
  namespace: hotdata
spec:
  parentRefs:
    - name: hotdata-gateway
  hostnames:
    - api.hotdata.dev
  rules:
    - matches:
        - path: { type: Exact, value: /v1/auth/jwt }
      filters:
        - type: URLRewrite
          urlRewrite:
            path: { type: ReplaceFullPath, replaceFullPath: /o/token/ }
      backendRefs:
        - { name: webapp, port: 8000 }
```

**Trade-off accepted:** Envoy rewrites the path but not the body, and DOT's
`/o/token/` expects `application/x-www-form-urlencoded`. So the SDK sends a
form-encoded request body (identical to the CLI); the response is already JSON.
The form-encoding is entirely hidden from SDK users behind the `/v1/auth/jwt`
path. A Django view would only be warranted if we needed a JSON *request* body
or custom error envelopes — not worth the extra code/maintenance here.

This works because the JWT `issuer` is already `https://api.hotdata.dev` (so
minting from the api host is consistent with the JWKS provider), and the
`api_token` grant doesn't do PKCE, so `PKCE_REQUIRED: True` doesn't block it
(already proven by the CLI).

**Open decision — rewrite vs. a thin Django view.** Because the rewrite targets
`/o/token/`, `/v1/auth/jwt` accepts *every* grant DOT serves there, not just
`api_token`. Two clarifications on why this is acceptable:

- It is **not net-new attack surface**: `/o/token/` is already internet-facing
  on `app.hotdata.dev`. The rewrite exposes the same endpoint on a second host.
- We **rely** on `grant_type=refresh_token` flowing through this path — the
  SDK's refresh step posts it to `/v1/auth/jwt`. So "it also accepts
  refresh_token" is required, not a leak.

The legitimate downside is that `authorization_code`/PKCE and any future grant
are also reachable on the public `/v1` path, and errors come back in DOT's
OAuth shape rather than the public-API error envelope. A thin Django view at
`/v1/auth/jwt` could whitelist `{api_token, refresh_token}`, normalize errors,
and add SDK-specific observability — at the cost of a small amount of code that
re-enters the same grant machinery. **Recommendation: ship the rewrite first**
(zero Django code, reuses the battle-tested grant + server-side mint cache), and
revisit a view only if grant-whitelisting or error-shape consistency becomes a
requirement. Flagging for explicit sign-off.

### Dedicated client_id: `hotdata-python-sdk`, seeded via the seed command

The SDK registers its **own** public OAuth Application from the start rather
than reusing `hotdata-cli`, so the Sessions/management UI can attribute SDK
traffic separately and SDK-specific policy can be applied later without
untangling it from the CLI.

Registration follows the repo's established convention — **not** a data
migration. Monopoly seeds OAuth Applications via the idempotent
`authentication/management/commands/seed_oauth_clients.py` command
(`update_or_create` over an `APPLICATIONS` list), auto-run on every `migrate`
through a `post_migrate` signal. So this is a one-entry diff:

```python
APPLICATIONS = [
    { "client_id": "hotdata-cli", ... },
    {
        "client_id": "hotdata-python-sdk",
        "name": "Hotdata Python SDK",
        "client_type": "public",
        "authorization_grant_type": "authorization-code",  # api_token grant rides on this, same as the CLI
        "algorithm": "RS256",
        "redirect_uris": "",          # no browser/PKCE leg — api_token grant only
        "skip_authorization": False,
        "hash_client_secret": True,
    },
]
```

A data migration is *not* idiomatic here: the DOT `Application` model is
swappable, so `RunPython` would need `apps.get_model(settings.OAUTH2_PROVIDER_APPLICATION_MODEL)`
plus cross-app migration dependencies, and it would bake seed data into schema
history. The seed command is the cleaner, already-standardized path.

## SDK implementation

### 1. New hand-written module `hotdata/_auth.py` (regen-immune)

OpenAPI Generator only writes the files it generates; hand-added modules in the
package survive regeneration untouched (precedent: `hotdata/arrow.py`, PR #60,
which is absent from `.openapi-generator/FILES` and so is never overwritten).
This module will additionally be added to `.openapi-generator-ignore` as
belt-and-suspenders (it is **not** there today — see work breakdown).

It is a direct port of the CLI's `jwt.rs` logic. It takes a reference to the
owning `Configuration` so it reads `host` at mint time (host may be set after
construction) and **reuses the SDK's configured TLS/proxy/timeout** rather than
a bare pool:

```python
# hotdata/_auth.py  (hand-written)
import json
import threading
import time
from urllib.parse import urlencode

_LEEWAY = 30          # refresh when <30s of life remains
_TIMEOUT = 30.0       # seconds — never let a stalled token endpoint hang every request
_CLIENT_ID = "hotdata-python-sdk"


class TokenExchangeError(Exception):
    """Raised when an hd_ API token cannot be exchanged for a JWT."""


class _TokenManager:
    """Exchanges an API token for short-lived JWTs and keeps them fresh.

    Pass-through for anything that already looks like a JWT (``eyJ`` prefix),
    matching the Gateway's own ``^Bearer eyJ.*`` detection.
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
        # A compact JWT always starts with "eyJ" (base64 of '{"'). Anything
        # else (hd_… or other opaque API tokens) must be exchanged.
        # (Alternative: treat a 3-segment dotted string as a JWT — the webapp
        # uses dot-count detection. eyJ-prefix matches the Gateway and is fine.)
        return isinstance(self._credential, str) and not self._credential.startswith("eyJ")

    def bearer_value(self):
        if not self._needs_exchange:
            return self._credential            # already a JWT → unchanged
        with self._lock:
            if self._jwt and time.time() < self._exp - _LEEWAY:
                return self._jwt
            if self._refresh and not self._mint(
                {"grant_type": "refresh_token", "refresh_token": self._refresh}
            ):
                self._refresh = None           # refresh failed → fall through to re-mint
            if not self._jwt or time.time() >= self._exp - _LEEWAY:
                self._mint({"grant_type": "api_token", "api_token": self._credential})
            return self._jwt

    def _mint(self, params):
        params["client_id"] = _CLIENT_ID
        pool = self._pool or _pool_from_config(self._config)   # reuses ssl_ca_cert/cert/proxy
        host = self._config.host.rstrip("/")
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
        data = json.loads(resp.data)
        self._jwt = data["access_token"]
        self._exp = time.time() + data.get("expires_in", 300)
        self._refresh = data.get("refresh_token") or self._refresh
        return True
```

Notes:
- **In-memory cache only** — no disk cache. The server-side mint de-duplication
  (keyed by `sha256(api_token)`) already prevents cross-process stampedes, so
  per-process caching is sufficient and avoids surprise disk writes.
- **Thread-safe** — `ApiClient` may be shared across threads; the lock with a
  single-flight mint covers concurrent exchanges. The *manager itself* must be
  created eagerly (see below) so concurrent first requests don't each build one.
- **Bounded I/O on the hot path** — every exchange uses an explicit `timeout`
  and the SDK's own TLS/proxy config, so a slow or stalled token endpoint fails
  fast instead of hanging all SDK calls.
- **Refresh, then re-mint** — use the refresh token when available; on refresh
  failure, re-mint from the held API token (always possible since the SDK holds
  it). Matches the CLI.

### 2. `api_key` becomes a property (one change in the custom template)

`Configuration.auth_settings()` reads `self.api_key` on **every** request and
builds `Authorization: Bearer <api_key>`. So making `api_key` a property whose
getter returns a live JWT means every existing call site transparently sends a
fresh JWT — no change to `api_client.py`, `rest.py`, or user code.

This is the regen-safe place to make the change: `configuration.py` is
generated from the team-owned custom template
`.openapi-generator-templates/configuration.mustache` (which already adds
`workspace_id`, `session_id`, `refresh_api_key_hook`). Editing the template *is*
the canonical, regeneration-surviving way to change `Configuration`.

The manager is created **eagerly** (in `__init__` and in the setter), never
lazily in the getter — lazy creation has a race where concurrent first requests
each build a manager before any lock helps.

```python
# in __init__ — replaces `self.api_key = api_key`
from hotdata._auth import _TokenManager
self._token_manager = _TokenManager(api_key, self) if api_key is not None else None

@property
def api_key(self):
    if self._token_manager is None:
        return None
    return self._token_manager.bearer_value()   # fresh JWT, exchanged + cached

@api_key.setter
def api_key(self, value):
    from hotdata._auth import _TokenManager
    self._token_manager = _TokenManager(value, self) if value is not None else None
```

> Note: the existing `refresh_api_key_hook` is *not* usable here —
> `auth_settings()` builds the bearer value directly from `self.api_key` and
> never routes through `get_api_key_with_prefix()`, so the hook only fires for
> the `X-Workspace-Id`/`X-Session-Id` schemes, not the bearer token.

### 3. `__deepcopy__` handling (required)

`Configuration.copy()` deep-copies the instance, and `_TokenManager` holds a
`threading.Lock` **and** a `urllib3.PoolManager` — neither is deepcopy-able. The
template's `__deepcopy__` must skip `_token_manager` and re-create it on the
copy from the (deepcopy-able) credential string, e.g.:

```python
def __deepcopy__(self, memo):
    cls = self.__class__
    result = cls.__new__(cls)
    memo[id(self)] = result
    for k, v in self.__dict__.items():
        if k == "_token_manager":
            continue                     # rebuilt below; never deepcopy lock/pool
        setattr(result, k, copy.deepcopy(v, memo))
    tm = self._token_manager
    result._token_manager = _TokenManager(tm._credential, result) if tm else None
    return result
```

This is the single most likely thing to break if missed.

## Edge cases

- **Pass-through** — credentials starting with `eyJ` (raw JWTs) or non-`hd_`
  test credentials are sent unchanged, so local/dev setups and the rollout
  window don't break.
- **Opt-out** — honor `HOTDATA_DISABLE_JWT_EXCHANGE` for a hard escape hatch.
- **Hot-path network call** — exchange happens inside `auth_settings()`, but
  only on first use and within 30s of expiry; otherwise it's a pure in-memory
  return.
- **SSL reuse** — ideally hand `_TokenManager` the same `ssl_ca_cert`/cert
  config the SDK already builds, rather than a bare `PoolManager`.
- **Clear errors** — surface `invalid_grant` (expired/revoked API token) as a
  `TokenExchangeError` rather than a confusing downstream 401.

## Testing plan

- Unit-test `_TokenManager` against a mocked `/v1/auth/jwt`: first-mint, cache
  hit, near-expiry refresh, refresh-failure → re-mint, `eyJ` pass-through,
  exchange error.
- Concurrency: N threads hit `bearer_value()` → exactly one mint.
- `copy.deepcopy(configuration)` round-trip (the lock gotcha).
- Regen-safety CI check: run the generator + `patch_api_client_close.py`, assert
  `_auth.py` survives and the `api_key` property is present (guards template
  drift).

## Work breakdown

**monopoly**
1. Gateway `HTTPRoute` `/v1/auth/jwt` → rewrite → `/o/token/`, no SecurityPolicy.
2. Add the `hotdata-python-sdk` entry to `seed_oauth_clients.py`.

**sdk-python**
3. Add hand-written `hotdata/_auth.py` (`_TokenManager`, `TokenExchangeError`);
   list it in `.openapi-generator-ignore`.
4. Template: `api_key` property + setter, `__deepcopy__` handling.
5. Tests per the plan above.

## Open questions

- **Rewrite vs. view** — sign-off needed on shipping the Gateway rewrite (which
  exposes all DOT grants on `/v1/auth/jwt`) vs. writing a thin grant-whitelisting
  view. See "Open decision" above. *(Recommendation: rewrite first.)*
- Confirm the data-plane `/v1/query` (per-workspace runtimedb) routes accept
  JWTs equivalently to API tokens during the rollout window (workspaces /
  sandboxes / sessions routes are confirmed via `httproute-api-jwt.yaml`).

*(Resolved by review: `_TokenManager` reuses the SDK's TLS/proxy config and a
bounded timeout for the exchange call — folded into the design above.)*
