"""Scenario: connections_read.

Read-only lifecycle ops on the seeded connection — get, list, health check,
and cache purge. Does not create or delete connections in prod (would require
real datastore credentials in CI secrets).
"""

from __future__ import annotations

from hotdata.api.connections_api import ConnectionsApi


def test_connections_read(connections_api: ConnectionsApi, connection_id: str) -> None:
    detail = connections_api.get_connection(connection_id)
    assert detail.id == connection_id
    assert detail.source_type
    assert detail.name

    listing = connections_api.list_connections()
    assert any(c.id == connection_id for c in listing.connections), (
        f"seeded connection {connection_id} not in list_connections"
    )

    health = connections_api.check_connection_health(connection_id)
    assert health.connection_id == connection_id
    assert health.healthy, f"seeded connection unhealthy: {health.error}"

    # purge_connection_cache returns None on success.
    connections_api.purge_connection_cache(connection_id)
