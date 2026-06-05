"""Scenario: embedding_providers_crud.

Register an embedding provider, read it, confirm it appears in
list_embedding_providers, update it, then delete it.

The scenario calls for a credential-free provider. It nominally asks for
`provider_type=local`, but the runtime currently rejects `local`
("not yet supported; use 'service'"), so we register a `service` provider with
**no** api_key/secret_name. A service provider's key is only consulted when
embeddings are actually generated (indexing) — never at create/get/update — so
this exercises the full CRUD surface without any real external credential and
without auto-creating a secret that would need cleanup.
"""

from __future__ import annotations

import pytest

from hotdata.api.embedding_providers_api import EmbeddingProvidersApi
from hotdata.exceptions import ApiException
from hotdata.models.create_embedding_provider_request import (
    CreateEmbeddingProviderRequest,
)
from hotdata.models.update_embedding_provider_request import (
    UpdateEmbeddingProviderRequest,
)


def test_embedding_providers_crud(
    embedding_providers_api: EmbeddingProvidersApi, sdkci_name
) -> None:
    name = sdkci_name("embprov")
    updated_name = sdkci_name("embprov-updated")
    provider_id: str | None = None

    try:
        created = embedding_providers_api.create_embedding_provider(
            CreateEmbeddingProviderRequest(
                name=name,
                provider_type="service",
                config={"model": "text-embedding-3-small"},
            )
        )
        provider_id = created.id
        assert created.id
        assert created.name == name
        assert created.provider_type == "service"

        got = embedding_providers_api.get_embedding_provider(provider_id)
        assert got.id == provider_id
        assert got.name == name

        listing = embedding_providers_api.list_embedding_providers()
        assert any(p.id == provider_id for p in listing.embedding_providers), (
            f"created provider {provider_id} not in list_embedding_providers"
        )

        updated = embedding_providers_api.update_embedding_provider(
            provider_id, UpdateEmbeddingProviderRequest(name=updated_name)
        )
        assert updated.id == provider_id
        assert updated.name == updated_name

        # Read-after-update reflects the rename.
        assert embedding_providers_api.get_embedding_provider(provider_id).name == (
            updated_name
        )

        embedding_providers_api.delete_embedding_provider(provider_id)
        provider_id = None

        with pytest.raises(ApiException) as excinfo:
            embedding_providers_api.get_embedding_provider(created.id)
        assert excinfo.value.status == 404
    finally:
        if provider_id is not None:
            try:
                embedding_providers_api.delete_embedding_provider(provider_id)
            except ApiException:
                pass
