"""Scenario: auth_missing_token_401.

Calls without a bearer token return 401 with the documented ApiErrorResponse
shape. Uses an unauthenticated client built locally — does not touch the
session-scoped api_client.
"""

from __future__ import annotations

import pytest

from hotdata import ApiClient, Configuration
from hotdata.api.workspaces_api import WorkspacesApi
from hotdata.exceptions import ApiException


def test_auth_missing_token_401(env) -> None:
    config = Configuration(host=env.api_url)  # no api_key, no workspace_id
    with ApiClient(config) as client:
        api = WorkspacesApi(client)
        with pytest.raises(ApiException) as excinfo:
            api.list_workspaces()
    assert excinfo.value.status == 401, (
        f"expected 401 without bearer token, got {excinfo.value.status}"
    )
    body = excinfo.value.body or ""
    assert body, "expected non-empty error body on 401"
