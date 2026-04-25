# Mustache template override

Two Hotdata-specific DX tweaks applied to the Python `configuration.mustache`:

1. **`api_key` is the bearer token** — matching Hotdata's docs and CLI
   (`--api-key`, `HOTDATA_API_KEY`). Stock openapi-generator calls the
   bearer token `access_token`; we drop that name entirely and replace it
   with `api_key`. Internal `auth_settings()` is patched to read
   `self.api_key`.

2. **`workspace_id` and `session_id` are first-class kwargs and
   attributes.** Stock openapi-generator exposes apiKey security schemes
   only via an opaque `api_key: Dict[str, str]` dict keyed by scheme name.
   That's a footgun — callers have to know the generator's
   `apiKey`-security machinery to set a workspace scope. The template
   adds typed `workspace_id` / `session_id` kwargs (and properties) that
   store into a renamed `self.api_keys` dict.

Net caller DX:

```python
cfg = hotdata.Configuration(
    api_key="sk_live_...",
    workspace_id="ws_abc",
    session_id="sb_xyz",
)
```

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
