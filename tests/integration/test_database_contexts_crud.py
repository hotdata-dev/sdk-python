"""Scenario: database_contexts_crud.

Against a fresh scratch database: upsert a named context document, read it back,
confirm it appears in list_database_contexts, upsert the same name again to
verify replace-on-write, delete the context, and confirm it's gone. The
`scratch_database` fixture creates and tears down the owning database.
"""

from __future__ import annotations

import pytest

from hotdata.api.database_context_api import DatabaseContextApi
from hotdata.exceptions import ApiException
from hotdata.models.upsert_database_context_request import (
    UpsertDatabaseContextRequest,
)


def test_database_contexts_crud(
    database_context_api: DatabaseContextApi, scratch_database: str, sdkci_name
) -> None:
    db_id = scratch_database
    # Context keys follow dataset table-name rules (letter/underscore first).
    name = "sdkci_" + sdkci_name("ctx").replace("-", "_")
    initial = "First revision of the context document."
    replaced = "Second revision — replace-on-write."

    upserted = database_context_api.upsert_database_context(
        db_id, UpsertDatabaseContextRequest(name=name, content=initial)
    )
    assert upserted.context.name == name
    assert upserted.context.content == initial

    got = database_context_api.get_database_context(db_id, name)
    assert got.context.name == name
    assert got.context.content == initial

    listing = database_context_api.list_database_contexts(db_id)
    assert any(c.name == name for c in listing.contexts), (
        f"context {name} not in list_database_contexts"
    )

    # Upsert reuses the same name: content is replaced, not appended.
    database_context_api.upsert_database_context(
        db_id, UpsertDatabaseContextRequest(name=name, content=replaced)
    )
    got2 = database_context_api.get_database_context(db_id, name)
    assert got2.context.content == replaced

    database_context_api.delete_database_context(db_id, name)

    with pytest.raises(ApiException) as excinfo:
        database_context_api.get_database_context(db_id, name)
    assert excinfo.value.status == 404
