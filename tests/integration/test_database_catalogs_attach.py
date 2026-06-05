"""Scenario: database_catalogs_attach.

Attach the seeded connection to a fresh scratch database as a catalog (under an
alias), confirm it's reachable via get_database, then detach it. Reversible and
idempotent — it never mutates the connection itself, only the scratch
database's attachment list (which is torn down with the database).
"""

from __future__ import annotations

from hotdata.api.databases_api import DatabasesApi
from hotdata.models.attach_database_catalog_request import (
    AttachDatabaseCatalogRequest,
)


def test_database_catalogs_attach(
    databases_api: DatabasesApi, scratch_database: str, connection_id: str
) -> None:
    db_id = scratch_database
    alias = "sdkci_cat"

    databases_api.attach_database_catalog(
        db_id,
        AttachDatabaseCatalogRequest(connection_id=connection_id, alias=alias),
    )

    detail = databases_api.get_database(db_id)
    attached = [a for a in detail.attachments if a.connection_id == connection_id]
    assert attached, (
        f"connection {connection_id} not in attachments after attach"
    )
    assert any(a.alias == alias for a in attached), (
        f"alias {alias!r} not reflected in attachment list"
    )

    databases_api.detach_database_catalog(db_id, connection_id)

    detail_after = databases_api.get_database(db_id)
    assert all(a.connection_id != connection_id for a in detail_after.attachments), (
        f"connection {connection_id} still attached after detach"
    )
