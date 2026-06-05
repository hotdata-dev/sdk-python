"""Scenario: connection_types_read.

Read-only: list_connection_types returns the available connector catalog, and
get_connection_type fetches one by name with its config schema. Mutates nothing.
"""

from __future__ import annotations

from hotdata.api.connection_types_api import ConnectionTypesApi


def test_connection_types_read(connection_types_api: ConnectionTypesApi) -> None:
    listing = connection_types_api.list_connection_types()
    assert listing.connection_types, "connector catalog is unexpectedly empty"
    for ct in listing.connection_types:
        assert ct.name
        assert ct.label

    # Fetch one by name; prefer postgres if present, else the first entry.
    names = [ct.name for ct in listing.connection_types]
    target = "postgres" if "postgres" in names else names[0]

    detail = connection_types_api.get_connection_type(target)
    assert detail.name == target
    assert detail.label
    # Each connector advertises a config schema clients use to build a request.
    assert detail.config_schema is not None
