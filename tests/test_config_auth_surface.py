"""Guards that `Configuration`'s auth surface matches what goes on the wire.

`Configuration` is generated from `.openapi-generator-templates/configuration.mustache`,
which hand-adds typed kwargs/properties (`workspace_id`, ...) on top of the
generator's `api_keys` dict. `auth_settings()` and each operation's
`_auth_settings` list, by contrast, come straight from the spec. When a security
scheme leaves the spec but its convenience kwarg stays in the template, callers
keep setting a value that is silently never sent -- which is how `session_id`
(`X-Session-Id`) went dead: the server stopped enforcing it, the spec dropped the
`SessionId` scheme, and the kwarg would have lingered as a no-op that quietly
unscoped every request.

The tests below pin that invariant generally, so the next scheme removal fails
here instead of shipping a silent no-op:

* every typed apiKey kwarg on `Configuration` reaches `auth_settings()`;
* `session_id` / `X-Session-Id` are gone from the config surface, the template,
  and the operations that used to carry them.
"""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from hotdata import ApiClient, Configuration
from hotdata.api.query_api import QueryApi
from hotdata.api.results_api import ResultsApi

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIGURATION_TEMPLATE = REPO_ROOT / ".openapi-generator-templates" / "configuration.mustache"

# A JWT-shaped credential is returned as-is by _TokenManager, so no exchange
# request is ever made from these tests.
FAKE_JWT = "eyJfake.payload.signature"


def _config(**kwargs) -> Configuration:
    return Configuration(host="https://api.example.test", api_key=FAKE_JWT, **kwargs)


def _typed_api_key_kwargs() -> list[str]:
    """Kwargs the template adds for apiKey schemes (everything but the generic ones)."""
    generic = {
        "self",
        "host",
        "api_key",
        "api_keys",
        "api_key_prefix",
        "username",
        "password",
        "server_index",
        "server_variables",
        "server_operation_index",
        "server_operation_variables",
        "ignore_operation_servers",
        "ssl_ca_cert",
        "retries",
        "ca_cert_data",
        "cert_file",
        "key_file",
        "debug",
    }
    params = inspect.signature(Configuration.__init__).parameters
    return [
        name
        for name in params
        if name not in generic and isinstance(getattr(Configuration, name, None), property)
    ]


def test_typed_api_key_kwargs_are_discoverable() -> None:
    """Keeps the parametrized test below from silently degenerating to zero cases."""
    assert "workspace_id" in _typed_api_key_kwargs()


@pytest.mark.parametrize("kwarg", _typed_api_key_kwargs())
def test_typed_api_key_kwarg_reaches_auth_settings(kwarg: str) -> None:
    """A convenience kwarg that never shows up in auth_settings() is a no-op."""
    config = _config(**{kwarg: "value-for-" + kwarg})

    settings = config.auth_settings()
    wire_values = {setting["value"] for setting in settings.values()}
    assert "value-for-" + kwarg in wire_values, (
        f"Configuration(...{kwarg}=...) is accepted but auth_settings() never emits it, "
        "so the value is silently dropped instead of being sent."
    )


def test_configuration_no_longer_exposes_session_id() -> None:
    """The SessionId scheme left the spec; the convenience surface must go with it."""
    assert not hasattr(Configuration, "session_id")
    assert "session_id" not in inspect.signature(Configuration.__init__).parameters

    with pytest.raises(TypeError):
        _config(session_id="s_abcd1234")


def test_configuration_template_has_no_session_id() -> None:
    """Editing only the generated file would be undone by the next regen."""
    template = CONFIGURATION_TEMPLATE.read_text()
    assert "session_id" not in template
    assert "SessionId" not in template
    assert "X-Session-Id" not in template


@pytest.mark.parametrize(
    "api_cls, serialize, kwargs",
    [
        (
            QueryApi,
            "_query_serialize",
            {"query_request": {"sql": "select 1"}, "x_database_id": "db_abc"},
        ),
        (
            ResultsApi,
            "_list_results_serialize",
            {"x_database_id": "db_abc", "limit": None, "offset": None},
        ),
    ],
)
def test_session_header_is_not_sent(api_cls, serialize: str, kwargs: dict) -> None:
    """Even a raw api_keys['SessionId'] escape hatch must not reach the wire."""
    config = _config(workspace_id="ws_abc", api_keys={"SessionId": "s_abcd1234"})
    api = api_cls(ApiClient(config))

    _method, _url, headers, *_rest = getattr(api, serialize)(
        _request_auth=None,
        _content_type=None,
        _headers=None,
        _host_index=0,
        **kwargs,
    )

    assert "X-Session-Id" not in headers
    assert headers["X-Workspace-Id"] == "ws_abc"
