"""Scenario: auth_unknown_workspace.

A valid bearer token combined with a fabricated workspace id (random UUID) must
return a 4xx error and never leak data from another workspace. Server may
respond 403 (forbidden) or 404 (not found) — both are acceptable.
"""

from __future__ import annotations

import uuid

import pytest

from hotdata import ApiClient, Configuration
from hotdata.api.datasets_api import DatasetsApi
from hotdata.exceptions import ApiException


def test_auth_unknown_workspace(env) -> None:
    fake_workspace = f"ws_{uuid.uuid4().hex}"
    config = Configuration(
        host=env.api_url,
        api_key=env.api_key,
        workspace_id=fake_workspace,
    )
    with ApiClient(config) as client:
        api = DatasetsApi(client)
        with pytest.raises(ApiException) as excinfo:
            api.list_datasets()
    assert excinfo.value.status in (403, 404), (
        f"expected 403/404 for fabricated workspace, got {excinfo.value.status}"
    )
