# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [0.3.4] - 2026-06-15

### Changed

- feat(queries): add preview and total row count fields

## [0.3.3] - 2026-06-10

### Changed

- chore: regenerate client, drop orphaned sandbox files

## [0.3.1] - 2026-06-06

### Security

- Raised dependency floors to patched releases: `pyarrow >= 14.0.1` (CVE-2023-47248, RCE via unsafe deserialization) and `pydantic >= 2.4.0` (CVE-2024-3772, regex denial of service).

## [0.3.0] - 2026-06-05

### Added

- Transparent API-token → JWT exchange: the client now exchanges an opaque API token for a short-lived JWT on first use and keeps it refreshed, so the wire always carries a current token. Credentials already shaped like a JWT pass through unchanged. Set `HOTDATA_DISABLE_JWT_EXCHANGE` to an affirmative value (`1`, `true`, `yes`, `on`) as a hard escape hatch.
- Managed-catalog editing endpoints: `add_managed_schema` and `add_managed_table` on `ConnectionsApi` and `DatabasesApi`, with new models `AddManagedSchemaRequest`, `AddManagedTableDecl`, `AddManagedTableRequest`, `ManagedSchemaResponse`, and `ManagedTableResponse`.
- Typed `x_database_id` parameter on `SavedQueriesApi.execute_saved_query` (required) and `DatasetsApi.create_dataset`, scoping execution to a database the same way `QueryApi.query` does — no more `_headers` override.
- `database_id` field on `QueryRequest` as a body-level alternative to the `X-Database-Id` header.
- `storage_backend` field on `CreateDatabaseRequest` to select the default catalog's physical backend (`parquet` or `ducklake`).
- `default_catalog` field on `CreateDatabaseRequest` to name the database's auto-created default catalog within its query scope, surfaced on `CreateDatabaseResponse`, `DatabaseDetailResponse`, and `DatabaseSummary`.

## [0.2.6] - 2026-05-29

### Added

- `default_catalog` and `default_schema` fields on `QueryRequest` to control how unqualified table references resolve within an `X-Database-Id` scope.

## [0.2.5] - 2026-05-27

### Changed

- Release 0.2.5

## [0.2.4] - 2026-05-27

### Changed

- Release 0.2.4

## [0.2.3] - 2026-05-22

### Added

- Databases API client (`DatabasesApi`) — create, get, list, delete databases and manage catalog attachments.
- New models: `CreateDatabaseRequest`, `CreateDatabaseResponse`, `DatabaseDetailResponse`, `DatabaseSummary`, `DatabaseAttachmentInfo`, `DatabaseDefaultSchemaDecl`, `DatabaseDefaultTableDecl`, `ListDatabasesResponse`, `AttachDatabaseCatalogRequest`.
- `expires_at` field on `CreateDatabaseRequest` for setting database expiry.
- `connection_types` field on `ListConnectionTypesResponse`; updated `ConnectionTypeDetail` and `ConnectionTypeSummary` models.

## [0.2.2] - 2026-05-20

### Fixed

- Add `ApiClient.close()` and `RESTClientObject.close()` so callers can release urllib3 connection pools and use context managers safely.

## [0.2.1] - 2026-05-20

### Changed

- Regenerated Results API client from the latest OpenAPI spec.

## [0.2.0] - 2026-05-19

### Changed

- Managed database API updates and publish workflow.

## [0.1.0] - 2026-04-25

### Changed

- Initial published release.
