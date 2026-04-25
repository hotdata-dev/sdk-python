"""Scenario: secrets_crud.

Create, read, update, delete a secret. Critically: confirm that get_secret /
list_secrets never echo the plaintext value back. The SDK's typed response
model has no `value` field, but we also defensively scan the raw payload to
catch a server-side regression where the value leaks through.
"""

from __future__ import annotations

import json

import pytest

from hotdata.api.secrets_api import SecretsApi
from hotdata.exceptions import ApiException
from hotdata.models.create_secret_request import CreateSecretRequest
from hotdata.models.update_secret_request import UpdateSecretRequest


def test_secrets_crud(secrets_api: SecretsApi, sdkci_name) -> None:
    # Server normalizes secret names — pass through whatever sdkci_name returns.
    secret_name = sdkci_name("secrets-crud").replace("-", "_")
    initial_value = "INITIAL_PLAINTEXT_VALUE_DO_NOT_LEAK"
    updated_value = "UPDATED_PLAINTEXT_VALUE_DO_NOT_LEAK"
    created = False

    try:
        create_resp = secrets_api.create_secret(
            CreateSecretRequest(name=secret_name, value=initial_value)
        )
        created = True
        assert create_resp.name == secret_name
        # Defensive: typed model shouldn't have a `value` field, but if a
        # server-side regression added one, dump and check.
        dumped = json.dumps(create_resp.to_dict(), default=str)
        assert initial_value not in dumped, "create_secret response leaked plaintext value"

        got = secrets_api.get_secret(secret_name)
        assert got.name == secret_name
        assert initial_value not in json.dumps(got.to_dict(), default=str), (
            "get_secret response leaked plaintext value"
        )

        listing = secrets_api.list_secrets()
        names = [s.name for s in listing.secrets]
        assert secret_name in names
        assert initial_value not in json.dumps(listing.to_dict(), default=str), (
            "list_secrets response leaked plaintext value"
        )

        secrets_api.update_secret(secret_name, UpdateSecretRequest(value=updated_value))

        got2 = secrets_api.get_secret(secret_name)
        assert updated_value not in json.dumps(got2.to_dict(), default=str)
        assert initial_value not in json.dumps(got2.to_dict(), default=str)

        secrets_api.delete_secret(secret_name)
        created = False

        with pytest.raises(ApiException) as excinfo:
            secrets_api.get_secret(secret_name)
        assert excinfo.value.status == 404
    finally:
        if created:
            try:
                secrets_api.delete_secret(secret_name)
            except ApiException:
                pass
