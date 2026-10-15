"""`Configuration` reads credentials and host from the environment.

The CLI already honours `HOTDATA_API_KEY`, `HOTDATA_WORKSPACE` and
`HOTDATA_API_URL`; the SDK now does the same when the matching constructor
argument is `None`. Explicit arguments always win, and an empty variable
counts as unset. `Configuration` is generated from the in-repo mustache
template, so the template is checked for the same wiring.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from hotdata import ApiClient, Configuration
from hotdata.api.workspaces_api import WorkspacesApi

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPO_ROOT / ".openapi-generator-templates" / "configuration.mustache"

ENV_VARS = ("HOTDATA_API_KEY", "HOTDATA_WORKSPACE", "HOTDATA_API_URL")


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def test_defaults_without_env() -> None:
    cfg = Configuration()
    assert cfg.api_key is None
    assert cfg.workspace_id is None
    assert cfg.host == "https://api.hotdata.dev"


def test_env_fills_in_missing_args(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOTDATA_API_KEY", "hd_env_key")
    monkeypatch.setenv("HOTDATA_WORKSPACE", "ws_env")
    monkeypatch.setenv("HOTDATA_API_URL", "https://api.example.test")
    cfg = Configuration()
    assert cfg.api_key == "hd_env_key"
    assert cfg.workspace_id == "ws_env"
    assert cfg.host == "https://api.example.test"
    # The env-provided values reach the wire exactly like explicit ones.
    auth = cfg.auth_settings()
    assert auth["BearerAuth"]["value"] == "Bearer hd_env_key"
    assert auth["WorkspaceId"]["value"] == "ws_env"


def test_explicit_args_win_over_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOTDATA_API_KEY", "hd_env_key")
    monkeypatch.setenv("HOTDATA_WORKSPACE", "ws_env")
    monkeypatch.setenv("HOTDATA_API_URL", "https://env.example.test")
    cfg = Configuration(
        api_key="hd_arg_key", workspace_id="ws_arg", host="https://arg.example.test"
    )
    assert cfg.api_key == "hd_arg_key"
    assert cfg.workspace_id == "ws_arg"
    assert cfg.host == "https://arg.example.test"


def test_empty_env_counts_as_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ENV_VARS:
        monkeypatch.setenv(name, "")
    cfg = Configuration()
    assert cfg.api_key is None
    assert cfg.workspace_id is None
    assert cfg.host == "https://api.hotdata.dev"


def test_env_host_is_used_for_requests(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOTDATA_API_URL", "https://env.example.test")
    monkeypatch.setenv("HOTDATA_API_KEY", "hd_env_key")
    client = ApiClient(Configuration())
    method, url, headers, _body, _post = WorkspacesApi(client)._list_workspaces_serialize(
        organization_public_id=None,
        _request_auth=None,
        _content_type=None,
        _headers=None,
        _host_index=0,
    )
    assert method == "GET"
    assert url.startswith("https://env.example.test/v1/workspaces")
    assert headers["Authorization"] == "Bearer hd_env_key"


def test_env_is_read_per_instance(monkeypatch: pytest.MonkeyPatch) -> None:
    # Resolved at construction, not at import: a later change to the
    # environment affects only configurations built after it.
    monkeypatch.setenv("HOTDATA_API_KEY", "first")
    first = Configuration()
    monkeypatch.setenv("HOTDATA_API_KEY", "second")
    second = Configuration()
    assert (first.api_key, second.api_key) == ("first", "second")


def test_template_carries_the_same_env_defaults() -> None:
    # configuration.py is regenerated from this template; the env wiring must
    # live there too or the next regen silently drops it.
    src = TEMPLATE.read_text()
    for name in ENV_VARS:
        assert f'os.environ.get("{name}")' in src
