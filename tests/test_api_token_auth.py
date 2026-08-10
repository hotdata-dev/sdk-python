"""The API token is the only credential: it goes on the wire verbatim.

Hotdata deprecated the API-token -> JWT key exchange. The SDK used to hold a
hand-written `_TokenManager` (`hotdata/_auth.py`) that POSTed the configured
token to `/v1/auth/jwt`, cached the returned JWT, and refreshed it with a
`refresh_token` grant; `Configuration.api_key` was a property that minted on
every read. All of that is gone -- the configured token is sent as
`Authorization: Bearer <token>` unchanged.

These tests pin that end to end: the token reaches the wire as-is, no token
endpoint is ever contacted, and the exchange machinery cannot creep back in via
the generated `configuration.py` or its mustache template.
"""

from __future__ import annotations

import copy
import importlib
from pathlib import Path

import pytest
import urllib3

from hotdata import ApiClient, Configuration
from hotdata.api.workspaces_api import WorkspacesApi

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIGURATION_TEMPLATE = REPO_ROOT / ".openapi-generator-templates" / "configuration.mustache"
CONFIGURATION_MODULE = REPO_ROOT / "hotdata" / "configuration.py"

# An opaque (non-JWT-shaped) token: exactly the credential the old exchange
# would have swapped for a JWT before sending.
API_TOKEN = "hd_opaque_api_token"


def _config(**kwargs) -> Configuration:
    return Configuration(host="https://api.example.test", api_key=API_TOKEN, **kwargs)


def _no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make any outbound urllib3 request an immediate failure.

    The exchange built its own pool manager, so a surviving mint would show up
    here rather than as a silently different header.
    """

    def explode(*args, **kwargs):  # pragma: no cover - only runs on regression
        raise AssertionError(f"unexpected outbound request: {args!r} {kwargs!r}")

    monkeypatch.setattr(urllib3.PoolManager, "request", explode)
    monkeypatch.setattr(urllib3.PoolManager, "urlopen", explode)


def test_api_token_is_sent_verbatim_as_bearer(monkeypatch: pytest.MonkeyPatch) -> None:
    """The configured token itself is the bearer credential."""
    _no_network(monkeypatch)
    config = _config()

    assert config.auth_settings()["BearerAuth"]["value"] == f"Bearer {API_TOKEN}"


def test_authorization_header_carries_the_api_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Serializing a real operation puts the raw token in the header."""
    _no_network(monkeypatch)
    api = WorkspacesApi(ApiClient(_config(workspace_id="ws_abc")))

    _method, _url, headers, *_rest = api._list_workspaces_serialize(
        organization_public_id=None,
        _request_auth=None,
        _content_type=None,
        _headers=None,
        _host_index=0,
    )

    assert headers["Authorization"] == f"Bearer {API_TOKEN}"


def test_api_token_is_read_repeatedly_without_exchange(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every request re-reads the credential; none of those reads mint anything."""
    _no_network(monkeypatch)
    config = _config()

    values = {config.auth_settings()["BearerAuth"]["value"] for _ in range(5)}

    assert values == {f"Bearer {API_TOKEN}"}


def test_api_token_can_be_replaced_and_cleared(monkeypatch: pytest.MonkeyPatch) -> None:
    """`api_key` stays writable, and clearing it drops the bearer header."""
    _no_network(monkeypatch)
    config = _config()

    config.api_key = "hd_rotated"
    assert config.auth_settings()["BearerAuth"]["value"] == "Bearer hd_rotated"

    config.api_key = None
    assert "BearerAuth" not in config.auth_settings()


def test_deepcopy_preserves_the_api_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """`ApiClient` deepcopies the configuration; the credential must survive it.

    The exchange needed a `__deepcopy__` special case because the token manager
    held a lock and a pool manager. A plain string needs none, but the copy must
    still authenticate.
    """
    _no_network(monkeypatch)
    config = _config(workspace_id="ws_abc")

    clone = copy.deepcopy(config)

    assert clone.api_key == API_TOKEN
    assert clone.auth_settings()["BearerAuth"]["value"] == f"Bearer {API_TOKEN}"


def test_jwt_opt_out_env_var_is_inert(monkeypatch: pytest.MonkeyPatch) -> None:
    """`HOTDATA_DISABLE_JWT_EXCHANGE` was the exchange escape hatch.

    With no exchange left there is nothing to disable, so the variable must not
    change behavior -- callers who still export it get the same raw token.
    """
    _no_network(monkeypatch)
    monkeypatch.setenv("HOTDATA_DISABLE_JWT_EXCHANGE", "0")

    assert _config().auth_settings()["BearerAuth"]["value"] == f"Bearer {API_TOKEN}"


def test_auth_exchange_module_is_gone() -> None:
    """`hotdata._auth` existed only to run the key exchange."""
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("hotdata._auth")


def test_api_key_is_a_plain_attribute() -> None:
    """A property getter is what made every read a potential mint."""
    assert not isinstance(getattr(Configuration, "api_key", None), property)


@pytest.mark.parametrize(
    "path",
    [CONFIGURATION_MODULE, CONFIGURATION_TEMPLATE],
    ids=["generated", "template"],
)
def test_no_exchange_machinery_in_configuration(path: Path) -> None:
    """Editing only the generated file would be undone by the next regen."""
    source = path.read_text()

    for needle in (
        "_TokenManager",
        "_token_manager",
        "_auth import",
        "/v1/auth/jwt",
        "refresh_token",
        "HOTDATA_DISABLE_JWT_EXCHANGE",
    ):
        assert needle not in source, f"{path.name} still references {needle}"
