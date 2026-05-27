# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]



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
