# Implementation brief: server-side support for SDK JWT exchange (monopoly)

> **For agents working in the `monopoly` repo.** This is the server half of a
> cross-repo change. The client half (the Python SDK transparently exchanging
> its `hd_` API token for a short-lived JWT) is being implemented separately in
> `sdk-python` and is **not** your concern. Your job is the two server-side
> enablers below. This document is self-contained — you do not need the SDK
> design doc.

## Context (what's being built and why)

Hotdata is moving API authentication to short-lived JWTs. The Python SDK is
gaining the ability to transparently exchange a long-lived `hd_…` API token for
a 5-minute JWT and use the JWT on subsequent requests — mirroring what the CLI
(`hotdata-cli`, `jwt.rs`) already does. To do that the SDK needs:

1. A **public, host-local exchange endpoint** on `api.hotdata.dev` it can POST
   to before it holds any JWT.
2. Its **own registered OAuth client** so SDK traffic is attributable
   separately from the CLI.

Both already have battle-tested machinery behind them — you are *exposing* and
*registering*, not building new auth logic.

### How the exchange already works

The API-token → JWT exchange is a custom OAuth 2.0 grant
(`authentication/grants.py`, `ApiTokenGrant`, a `ClientCredentialsGrant`
subclass) served by django-oauth-toolkit (DOT) at `POST /o/token/`:

```
POST /o/token/
Content-Type: application/x-www-form-urlencoded

grant_type=api_token&api_token=hd_…&client_id=<public-client>
```

Response (standard OAuth token shape, JSON):

```json
{
  "access_token": "<RS256 JWT>",
  "refresh_token": "<opaque>",
  "token_type": "Bearer",
  "expires_in": 300,
  "scope": "permission:read_write workspace:work_…"
}
```

- JWT access-token TTL: **5 minutes** (300s). Refresh-token TTL: **36 hours**
  for api_token-origin tokens.
- `client_id` is validated only as a *registered public client*
  (`grants.py` → `authenticate_client_id`); caller identity and scopes come
  entirely from the API token, not the client.
- The grant already de-duplicates mints server-side: it caches the JWT keyed by
  `sha256(api_token)` behind a `SET NX` lock, so a fleet of SDK processes
  sharing one API token will not stampede `/o/token/`. **Do not add new
  caching** — it exists.
- The JWT `issuer` is already `https://api.hotdata.dev`, so minting from the api
  host is consistent with the JWKS provider. The `api_token` grant does not use
  PKCE, so `PKCE_REQUIRED: True` does not block it (already proven by the CLI).

---

## Task 1 — Gateway `HTTPRoute`: expose `/v1/auth/jwt` → rewrite → `/o/token/`

Expose the exchange on the **api host** under the public `/v1` surface as
`/v1/auth/jwt`, implemented **purely at the Gateway** (Envoy Gateway / Gateway
API) — **no new Django view**.

- Match `Exact: /v1/auth/jwt` on `api.hotdata.dev`.
- `URLRewrite` (`ReplaceFullPath`) to `/o/token/`, forwarding to `webapp:8000`.
- **No `SecurityPolicy`** attached — the route must be reachable *before* the
  caller has a JWT (the `hd_` token in the request body is the credential,
  validated by Django's grant). SecurityPolicies are opt-in per route via
  `targetRef.name`, so an unattached route is genuinely public, not a gap. This
  mirrors the existing `api-auth-hotdata-route`, which also has no policy.

**Why `/v1/auth/jwt` (not `/v1/auth/token`):** `/v1/auth/token` is already taken
— it's the PKCE CLI-login view that mints an *opaque* token. The JWT-exchange
path is `/v1/auth/jwt`, parallel to the existing `/v1/auth/sandbox`.

### File to add

`infrastructure/kubernetes/base/gateway-api/httproute-api-jwt-exchange.yaml`
*(confirm this matches the repo's actual gateway-api directory layout and the
existing `httproute-api-*.yaml` naming — see "Before you start" below).*

```yaml
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

Wire it into whatever assembles the gateway routes (e.g. a kustomization
`resources:` list) the same way the sibling routes are wired.

### Trade-off you are accepting (form-encoding)

Envoy rewrites the path but **not the body**, and DOT's `/o/token/` expects
`application/x-www-form-urlencoded`. So the SDK sends a form-encoded body
(identical to the CLI); the response is already JSON. The form-encoding is
hidden from SDK users behind the `/v1/auth/jwt` path. A Django view would only
be warranted if we needed a JSON *request* body or custom error envelopes — see
the open decision below.

### ⚠️ Open decision — REQUIRES SIGN-OFF before/at PR

Because the rewrite targets `/o/token/`, `/v1/auth/jwt` accepts **every grant
DOT serves there**, not just `api_token`. Clarifications:

- **Not net-new attack surface:** `/o/token/` is already internet-facing on
  `app.hotdata.dev`; the rewrite exposes the *same* endpoint on a second host.
- **`refresh_token` is required, not a leak:** the SDK's refresh step posts
  `grant_type=refresh_token` to `/v1/auth/jwt`, so that grant flowing through is
  intentional.
- **Legitimate downside:** `authorization_code`/PKCE and any future grant are
  also reachable on the public `/v1` path, and errors return DOT's OAuth shape
  rather than the public-API error envelope.

**Recommendation: ship the rewrite first** (zero Django code, reuses the
battle-tested grant + server-side mint cache). A thin Django view at
`/v1/auth/jwt` that whitelists `{api_token, refresh_token}`, normalizes errors,
and adds SDK observability is the alternative — at the cost of code that
re-enters the same grant machinery. **Get explicit sign-off on rewrite-vs-view
before merging.** If the decision flips to a view, implement it at the same path
with the same external behavior.

---

## Task 2 — Register the `hotdata-python-sdk` OAuth client

The SDK registers its **own** public OAuth Application (rather than reusing
`hotdata-cli`) so the Sessions/management UI can attribute SDK traffic
separately and SDK-specific policy can be applied later without untangling it
from the CLI.

Use the repo's established convention — the idempotent seed command, **not a
data migration**. Monopoly seeds OAuth Applications via
`authentication/management/commands/seed_oauth_clients.py`
(`update_or_create` over an `APPLICATIONS` list), auto-run on every `migrate`
through a `post_migrate` signal. This is a one-entry diff:

```python
APPLICATIONS = [
    { "client_id": "hotdata-cli", ... },   # existing — leave as-is
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

**Match the exact field set and value conventions of the existing
`hotdata-cli` entry** in the actual file — the snippet above is from the design
and the real entry may have additional keys. Mirror the `hotdata-cli` entry and
change only what differs (`client_id`, `name`).

**Do not use a data migration.** The DOT `Application` model is swappable, so
`RunPython` would need
`apps.get_model(settings.OAUTH2_PROVIDER_APPLICATION_MODEL)` plus cross-app
migration dependencies, and it would bake seed data into schema history. The
seed command is the cleaner, already-standardized path.

---

## Before you start (verify against the real repo)

The file paths, names, and snippets here come from a design doc and must be
reconciled with the actual `monopoly` tree:

- [ ] Locate the real gateway-api directory and the existing
      `httproute-api-*.yaml` files; copy their structure, labels, annotations,
      and kustomization wiring. Confirm `parentRefs.name: hotdata-gateway`,
      `namespace`, and `backendRefs` (`webapp:8000`) match what siblings use.
- [ ] Confirm `api-auth-hotdata-route` (or equivalent) indeed has **no**
      `SecurityPolicy` attached — that's the precedent for a policy-free public
      route.
- [ ] Open `authentication/management/commands/seed_oauth_clients.py`, read the
      real `APPLICATIONS` list and the `hotdata-cli` entry, and mirror its exact
      shape.
- [ ] Confirm `/v1/auth/token` and `/v1/auth/sandbox` exist as described (so
      `/v1/auth/jwt` is the right, non-colliding name).

## Acceptance criteria

1. `POST https://api.hotdata.dev/v1/auth/jwt` with
   `Content-Type: application/x-www-form-urlencoded` and body
   `grant_type=api_token&api_token=<valid hd_ token>&client_id=hotdata-python-sdk`
   returns `200` with an `access_token` JWT (issuer `https://api.hotdata.dev`),
   `refresh_token`, and `expires_in: 300`.
2. The same endpoint accepts `grant_type=refresh_token&refresh_token=…&client_id=hotdata-python-sdk`
   and returns a fresh JWT.
3. An invalid/revoked `hd_` token returns DOT's `invalid_grant` error (the SDK
   surfaces this as a clear error).
4. The `hotdata-python-sdk` Application exists after `migrate` (idempotent —
   running the seed twice does not duplicate or error).
5. The new route has **no** `SecurityPolicy` targeting it.
6. Existing routes and the CLI's exchange flow are unaffected.

## Verification steps

- Render the kustomization locally (`kustomize build …` / `kubectl kustomize …`)
  and confirm the `HTTPRoute` appears with the rewrite filter and no policy ref.
- Run the seed command (or `migrate`) against a dev DB and confirm the
  Application row, then run it again to prove idempotency.
- In a dev/staging cluster, exercise acceptance criteria 1–3 with `curl`.

## Related rollout note (informational, no action here)

The Gateway already routes `Authorization: Bearer eyJ…` (JWTs) to a
JWT-validating `SecurityPolicy` and `Bearer hd_…` (API tokens) through the
existing extAuth/DB path (`httproute-api-jwt.yaml`). **Both are accepted
today**, so this change is non-breaking and can ship ahead of any JWT-only
enforcement. (Once API tokens are fully deprecated, the `api-hotdata-route` for
the legacy path can be removed — out of scope here.) One thing worth
confirming during rollout: that the data-plane `/v1/query` (per-workspace
runtimedb) routes accept JWTs equivalently to API tokens; workspaces /
sandboxes / sessions routes are already confirmed via `httproute-api-jwt.yaml`.
