# Mustache template override

Two Hotdata-specific DX tweaks applied to the Python `configuration.mustache`:

1. **`api_key` is the bearer token** — matching Hotdata's docs and CLI
   (`--api-key`, `HOTDATA_API_KEY`). Stock openapi-generator calls the
   bearer token `access_token`; we drop that name entirely and replace it
   with `api_key`. Internal `auth_settings()` is patched to read
   `self.api_key`. The token is sent verbatim: the API-token → JWT key
   exchange this template used to wire up (a `_TokenManager` minting from
   `/v1/auth/jwt`) is deprecated and gone, so `api_key` is a plain
   attribute again.

2. **`workspace_id` is a first-class kwarg and attribute.** Stock
   openapi-generator exposes apiKey security schemes only via an opaque
   `api_key: Dict[str, str]` dict keyed by scheme name. That's a footgun
   — callers have to know the generator's `apiKey`-security machinery to
   set a workspace scope. The template adds a typed `workspace_id` kwarg
   (and property) that stores into a renamed `self.api_keys` dict.

Net caller DX:

```python
cfg = hotdata.Configuration(
    api_key="sk_live_...",
    workspace_id="ws_abc",
)
```

Because these kwargs are hand-added, they don't disappear when a security
scheme leaves the spec — `auth_settings()` and the per-operation
`_auth_settings` lists do, leaving the kwarg behind as a silent no-op. When
a scheme is dropped upstream, drop its kwarg/property here in the same
change. `tests/test_config_auth_surface.py` fails if the two drift apart.

## Drift tripwire

The regenerate workflow runs `import hotdata` and relies on
`openapi-generator` 7.20.0 (pinned in `openapitools.json`). If a future
release renames the mustache vars our patch references (`authMethods`,
`isApiKey`, `isBasicBearer`, `isOAuth`, `name`, `keyParamName`), the
import will fail and the regen PR will be obviously broken rather than
shipping subtly wrong code.

Bumping the pinned generator version should include a diff of this
template against upstream's
`modules/openapi-generator/src/main/resources/python/configuration.mustache`.
