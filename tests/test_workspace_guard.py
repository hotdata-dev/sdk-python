"""Client-side guard for workspace-scoped calls with no workspace id.

Without it the request goes out missing `X-Workspace-Id` and the server replies
with a bare 404 that does not say what was wrong. The guard (hotdata/_workspace.py,
wired into ApiClient.update_params_for_auth by scripts/patch_workspace_guard.py)
raises `MissingWorkspaceError` before anything is sent, naming the constructor
argument and the environment variable. Operations that are not workspace-scoped
(the Workspaces endpoints, whose security is BearerAuth only) must keep working.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import patch

import pytest

from hotdata import ApiClient, Configuration, MissingWorkspaceError
from hotdata._workspace import ensure_workspace
from hotdata.api.databases_api import DatabasesApi as _GeneratedDatabasesApi
from hotdata.api.workspaces_api import WorkspacesApi
from hotdata.exceptions import ApiValueError
from hotdata.loads import DatabasesApi
from hotdata.rest import RESTResponse

REPO_ROOT = Path(__file__).resolve().parents[1]


class _FakeHTTPResponse:
    def __init__(self, status: int, body: bytes) -> None:
        self.status = status
        self.reason = "OK"
        self.data = body
        self.headers = {"Content-Type": "application/json"}

    def getheaders(self) -> Dict[str, str]:
        return self.headers

    def getheader(self, name: str, default: Any = None) -> Any:
        return self.headers.get(name, default)


def _recording_rest(body: Any) -> tuple[Any, List[Dict[str, Any]]]:
    """A stand-in for RESTClientObject.request that records what was sent."""
    seen: List[Dict[str, Any]] = []
    payload = json.dumps(body).encode()

    def request(method, url, headers=None, body=None, post_params=None, _request_timeout=None):
        seen.append({"method": method, "url": url, "headers": dict(headers or {})})
        return RESTResponse(_FakeHTTPResponse(200, payload))

    return request, seen


@pytest.fixture(autouse=True)
def _no_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HOTDATA_WORKSPACE", raising=False)
    monkeypatch.delenv("HOTDATA_API_KEY", raising=False)


def _client(**kwargs: Any) -> ApiClient:
    return ApiClient(Configuration(host="https://api.example.test", api_key="hd_key", **kwargs))


def test_workspace_scoped_call_without_workspace_fails_before_sending() -> None:
    request, seen = _recording_rest({"databases": []})
    client = _client()
    with patch.object(client.rest_client, "request", side_effect=request):
        with pytest.raises(MissingWorkspaceError) as ei:
            _GeneratedDatabasesApi(client).list_databases()
    assert seen == []  # nothing went on the wire
    msg = str(ei.value)
    assert "workspace_id" in msg
    assert "HOTDATA_WORKSPACE" in msg
    assert "X-Workspace-Id" in msg
    assert "/v1/databases" in msg
    assert ei.value.method == "GET"
    # It is a client-side value error, so existing `except ApiValueError` /
    # `except ValueError` handlers see it too.
    assert isinstance(ei.value, ApiValueError)
    assert isinstance(ei.value, ValueError)


def test_enhanced_client_is_guarded_too() -> None:
    client = _client()
    with patch.object(client.rest_client, "request") as req:
        with pytest.raises(MissingWorkspaceError):
            DatabasesApi(client).list_databases()
    req.assert_not_called()


def test_workspace_from_constructor_is_sent() -> None:
    request, seen = _recording_rest({"databases": []})
    client = _client(workspace_id="ws_arg")
    with patch.object(client.rest_client, "request", side_effect=request):
        _GeneratedDatabasesApi(client).list_databases()
    assert seen[0]["headers"]["X-Workspace-Id"] == "ws_arg"


def test_workspace_from_env_is_sent(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOTDATA_WORKSPACE", "ws_env")
    request, seen = _recording_rest({"databases": []})
    client = _client()
    with patch.object(client.rest_client, "request", side_effect=request):
        _GeneratedDatabasesApi(client).list_databases()
    assert seen[0]["headers"]["X-Workspace-Id"] == "ws_env"


def test_explicit_header_satisfies_the_guard() -> None:
    request, seen = _recording_rest({"databases": []})
    client = _client()
    with patch.object(client.rest_client, "request", side_effect=request):
        _GeneratedDatabasesApi(client).list_databases(_headers={"x-workspace-id": "ws_hdr"})
    assert seen[0]["headers"]["x-workspace-id"] == "ws_hdr"


def test_request_auth_override_bypasses_the_guard() -> None:
    request, seen = _recording_rest({"databases": []})
    client = _client()
    override = {"in": "header", "key": "Authorization", "type": "bearer", "value": "Bearer other"}
    with patch.object(client.rest_client, "request", side_effect=request):
        _GeneratedDatabasesApi(client).list_databases(_request_auth=override)
    assert seen[0]["headers"]["Authorization"] == "Bearer other"


def test_unscoped_workspace_endpoints_still_work() -> None:
    # The Workspaces endpoints carry BearerAuth only (security: [BearerAuth]),
    # so there is no workspace to require.
    request, seen = _recording_rest({"ok": True, "workspaces": []})
    client = _client()
    with patch.object(client.rest_client, "request", side_effect=request):
        WorkspacesApi(client).list_workspaces()
    assert seen[0]["url"].endswith("/v1/workspaces")
    assert "X-Workspace-Id" not in seen[0]["headers"]


def test_ensure_workspace_ignores_operations_without_the_scheme() -> None:
    cfg = Configuration(api_key="hd_key")
    ensure_workspace(cfg, ["BearerAuth"], {}, "/v1/workspaces", "GET")
    ensure_workspace(cfg, None, {}, "/v1/workspaces", "GET")
    ensure_workspace(cfg, [], None, "/v1/workspaces", "GET")
    with pytest.raises(MissingWorkspaceError):
        ensure_workspace(cfg, ["BearerAuth", "WorkspaceId"], {}, "/v1/databases", "GET")


def test_empty_workspace_id_counts_as_missing() -> None:
    cfg = Configuration(api_key="hd_key", workspace_id="")
    with pytest.raises(MissingWorkspaceError):
        ensure_workspace(cfg, ["WorkspaceId"], {}, "/v1/databases", "GET")


def test_patch_is_applied_and_wired_for_regeneration() -> None:
    api_client_src = (REPO_ROOT / "hotdata" / "api_client.py").read_text()
    assert "ensure_workspace(" in api_client_src
    workflow = (REPO_ROOT / ".github" / "workflows" / "regenerate.yml").read_text()
    assert "scripts/patch_workspace_guard.py" in workflow
    ignore = (REPO_ROOT / ".openapi-generator-ignore").read_text().splitlines()
    assert "hotdata/_workspace.py" in ignore
