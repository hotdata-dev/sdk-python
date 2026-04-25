"""Shared fixtures for SDK integration tests.

Tests run against production. See www.hotdata.dev/api/README.md for the
contract — env vars, naming conventions, blast-radius rules.
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from typing import Iterator

import pytest

from hotdata import ApiClient, Configuration
from hotdata.api.connections_api import ConnectionsApi
from hotdata.api.datasets_api import DatasetsApi
from hotdata.api.indexes_api import IndexesApi
from hotdata.api.saved_queries_api import SavedQueriesApi
from hotdata.api.secrets_api import SecretsApi
from hotdata.api.workspaces_api import WorkspacesApi


REQUIRED_ENV = ("HOTDATA_SDK_TEST_API_KEY", "HOTDATA_SDK_TEST_WORKSPACE_ID")
DEFAULT_API_URL = "https://api.hotdata.dev"


@dataclass(frozen=True)
class TestEnv:
    api_url: str
    api_key: str
    workspace_id: str
    connection_id: str | None


def _load_env() -> TestEnv:
    missing = [name for name in REQUIRED_ENV if not os.environ.get(name)]
    if missing:
        pytest.skip(
            "SDK integration tests require env vars: " + ", ".join(missing)
        )
    # GitHub Actions sets `env:` keys even when the underlying secret/var is
    # unset, producing empty strings rather than absent keys. Use `or` to fall
    # back to the default for url and to None for the optional connection id.
    return TestEnv(
        api_url=os.environ.get("HOTDATA_SDK_TEST_API_URL") or DEFAULT_API_URL,
        api_key=os.environ["HOTDATA_SDK_TEST_API_KEY"],
        workspace_id=os.environ["HOTDATA_SDK_TEST_WORKSPACE_ID"],
        connection_id=os.environ.get("HOTDATA_SDK_TEST_CONNECTION_ID") or None,
    )


@pytest.fixture(scope="session")
def env() -> TestEnv:
    return _load_env()


@pytest.fixture(scope="session")
def api_client(env: TestEnv) -> Iterator[ApiClient]:
    config = Configuration(
        host=env.api_url,
        api_key=env.api_key,
        workspace_id=env.workspace_id,
    )
    with ApiClient(config) as client:
        yield client


@pytest.fixture(scope="session")
def workspace_id(env: TestEnv) -> str:
    return env.workspace_id


@pytest.fixture(scope="session")
def connection_id(env: TestEnv) -> str:
    if not env.connection_id:
        pytest.skip("HOTDATA_SDK_TEST_CONNECTION_ID required for this scenario")
    return env.connection_id


@pytest.fixture
def sdkci_name() -> "callable[[str], str]":
    """Returns `sdkci-<scenario>-<uuid8>` so orphans are identifiable.

    See api/README.md — every test-created resource must use this prefix.
    """

    def _make(scenario: str) -> str:
        return f"sdkci-{scenario}-{uuid.uuid4().hex[:8]}"

    return _make


# Per-API client fixtures keep tests one-liner short and avoid every test
# instantiating its own *Api(api_client).
@pytest.fixture
def datasets_api(api_client: ApiClient) -> DatasetsApi:
    return DatasetsApi(api_client)


@pytest.fixture
def workspaces_api(api_client: ApiClient) -> WorkspacesApi:
    return WorkspacesApi(api_client)


@pytest.fixture
def connections_api(api_client: ApiClient) -> ConnectionsApi:
    return ConnectionsApi(api_client)


@pytest.fixture
def indexes_api(api_client: ApiClient) -> IndexesApi:
    return IndexesApi(api_client)


@pytest.fixture
def saved_queries_api(api_client: ApiClient) -> SavedQueriesApi:
    return SavedQueriesApi(api_client)


@pytest.fixture
def secrets_api(api_client: ApiClient) -> SecretsApi:
    return SecretsApi(api_client)
