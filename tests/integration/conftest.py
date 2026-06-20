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
from hotdata.api.connection_types_api import ConnectionTypesApi
from hotdata.api.connections_api import ConnectionsApi
from hotdata.api.database_context_api import DatabaseContextApi
from hotdata.api.databases_api import DatabasesApi
from hotdata.api.embedding_providers_api import EmbeddingProvidersApi
from hotdata.api.indexes_api import IndexesApi
from hotdata.api.information_schema_api import InformationSchemaApi
from hotdata.api.jobs_api import JobsApi
from hotdata.api.refresh_api import RefreshApi
from hotdata.api.saved_queries_api import SavedQueriesApi
from hotdata.api.secrets_api import SecretsApi
from hotdata.api.uploads_api import UploadsApi
from hotdata.api.workspaces_api import WorkspacesApi
from hotdata.exceptions import ApiException
from hotdata.models.create_database_request import CreateDatabaseRequest


REQUIRED_ENV = ("HOTDATA_SDK_TEST_API_KEY", "HOTDATA_SDK_TEST_WORKSPACE_ID")
DEFAULT_API_URL = "https://api.hotdata.dev"

# Queries are scoped to a database via the X-Database-Id header. Databases no
# longer auto-expire, so rather than create one per run (which would leak),
# tests find-or-create a single stable database by name and reuse it — same
# pattern as the e2e suite. Name is not unique server-side; we key off it.
SHARED_DATABASE_NAME = "sdkci-shared"


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


@pytest.fixture(scope="session")
def database_id(api_client: ApiClient) -> str:
    """Id of the shared `sdkci-shared` database, creating it if absent.

    Queries require an `X-Database-Id` scope; databases persist (no auto-expiry)
    so we reuse one across runs instead of creating-and-deleting per session.
    """
    databases_api = DatabasesApi(api_client)
    for db in databases_api.list_databases().databases:
        if db.name == SHARED_DATABASE_NAME:
            return db.id
    created = databases_api.create_database(
        CreateDatabaseRequest(name=SHARED_DATABASE_NAME)
    )
    return created.id


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
def workspaces_api(api_client: ApiClient) -> WorkspacesApi:
    return WorkspacesApi(api_client)


@pytest.fixture
def connections_api(api_client: ApiClient) -> ConnectionsApi:
    return ConnectionsApi(api_client)


@pytest.fixture
def databases_api(api_client: ApiClient) -> DatabasesApi:
    return DatabasesApi(api_client)


@pytest.fixture
def indexes_api(api_client: ApiClient) -> IndexesApi:
    return IndexesApi(api_client)


@pytest.fixture
def saved_queries_api(api_client: ApiClient) -> SavedQueriesApi:
    return SavedQueriesApi(api_client)


@pytest.fixture
def secrets_api(api_client: ApiClient) -> SecretsApi:
    return SecretsApi(api_client)


@pytest.fixture
def database_context_api(api_client: ApiClient) -> DatabaseContextApi:
    return DatabaseContextApi(api_client)


@pytest.fixture
def embedding_providers_api(api_client: ApiClient) -> EmbeddingProvidersApi:
    return EmbeddingProvidersApi(api_client)


@pytest.fixture
def connection_types_api(api_client: ApiClient) -> ConnectionTypesApi:
    return ConnectionTypesApi(api_client)


@pytest.fixture
def jobs_api(api_client: ApiClient) -> JobsApi:
    return JobsApi(api_client)


@pytest.fixture
def information_schema_api(api_client: ApiClient) -> InformationSchemaApi:
    return InformationSchemaApi(api_client)


@pytest.fixture
def uploads_api(api_client: ApiClient) -> UploadsApi:
    return UploadsApi(api_client)


@pytest.fixture
def refresh_api(api_client: ApiClient) -> RefreshApi:
    return RefreshApi(api_client)


@pytest.fixture
def scratch_database(databases_api: DatabasesApi, sdkci_name) -> Iterator[str]:
    """Yields the id of a fresh, isolated database, deleting it on teardown.

    Unlike the session-scoped `database_id` (the shared `sdkci-shared` db reused
    across runs), scenarios that declare schemas/tables/contexts or attach
    catalogs need their own throwaway database so they never touch seeded data
    or collide with a parallel run. `expires_at` is a safety net: if teardown is
    interrupted, the server reclaims the database rather than leaking it.
    """
    created = databases_api.create_database(
        CreateDatabaseRequest(name=sdkci_name("scratch"), expires_at="2h")
    )
    try:
        yield created.id
    finally:
        try:
            databases_api.delete_database(created.id)
        except ApiException:
            pass
