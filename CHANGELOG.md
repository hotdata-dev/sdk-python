# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- feat(databases): add search parameter to list endpoint
- chore(databases): make pagination fields nullable

### Removed

- The legacy `POST /v1/files` upload endpoints have been removed in favor of the
  presigned upload flow. This drops `hotdata.UploadsApi.upload_stream`, the raw
  `upload_file(body=...)` / `list_uploads` operations, and the `UploadResponse`,
  `UploadInfo`, and `ListUploadsResponse` models. Use
  `hotdata.UploadsApi.upload_file(source, ...)` (direct-to-storage) instead.

## [0.8.0] - 2026-07-20

### Changed

- feat(loads): add key parameter to load requests
- feat(databases): add fork endpoint

## [0.7.0] - 2026-07-14

### Changed

- feat(schemas): add key field to table definitions
- feat(tables): support loading from query results

## [0.6.0] - 2026-07-07

### Changed

- feat: support async table loads and append mode
- feat(uploads): support streaming uploads with on-demand part URLs
- **Breaking:** results and query runs are now scoped to a database via the
  required `X-Database-Id` header. The generated `ResultsApi` / `QueryRunsApi`
  methods (`get_result`, `list_results`, `get_query_run`, `list_query_runs`)
  gain a required `x_database_id` argument, and the hand-written ergonomic
  helpers match: `hotdata.arrow.ResultsApi.get_result_arrow` /
  `stream_result_arrow` and `hotdata.query.QueryApi.wait_for_result` take the
  database id, and `QueryApi.query`'s truncation auto-follow forwards the
  query's database scope (the `X-Database-Id` header, or the request-body
  `database_id` when no header is set) to its result and query-run fetches.

## [0.5.0] - 2026-06-28

### Added

- `hotdata.UploadsApi` gains `upload_file(source, ...)`, a transparent
  direct-to-storage upload. Give it a file path, raw `bytes`, or a seekable
  binary file object and it opens an upload session, sends the data **straight
  to object storage** (a single request for a small file, concurrent multipart
  for a large one), and finalizes — returning the `FinalizeUploadResponse`. Your
  bytes never round-trip through the API. Supports a progress callback, an
  auto-scaled (or caller-set) part size, bounded concurrency with a peak-memory
  budget, and idempotent per-part retry (tunable via `part_retry`). Failures
  raise a typed hierarchy under `UploadError`: `StorageError`,
  `StorageTransportError`, `MissingETagError`, `MalformedSessionError`, and
  `SizeLimitError`.
- `hotdata.UploadsApi.upload_stream` uploads `bytes` or a binary stream
  (streamed without buffering) in a single request — the fallback for when
  direct-to-storage uploads aren't available or the source isn't seekable.
- Table loads now accept CSV and JSON source files in addition to Parquet.

### Changed

- Regenerated the client from the updated Hotdata OpenAPI spec.
- Documentation: removed stale datasets references and refreshed the MCP + CLI
  reference.

### Removed

- The datasets API and its related job types have been removed.

## [0.4.1] - 2026-06-19

### Changed

- `Configuration` now defaults to a retry policy that transparently retries
  pre-response connection resets (stale pooled keep-alive connections, e.g.
  `ProtocolError('Connection aborted.', ConnectionResetError)`) on **every**
  method, including `POST`. Such a reset happens before the request reaches the
  server, so retrying on a fresh connection cannot double-execute. Read timeouts
  and status retries stay idempotent-only. Pass an explicit `retries` to
  override (#118).
- chore: make api doc language end-user focused

## [0.4.0] - 2026-06-16

### Added

- `hotdata.query.QueryApi`: enhanced query client that transparently retries
  HTTP 429 (`OVERLOADED`) admission shedding honoring `Retry-After`, and
  auto-follows truncated results to materialize the full row set, guarded by
  configurable `max_auto_rows` (default 1M) and `max_auto_bytes` (default
  64 MiB) ceilings (#688).
- `ResultError` base class for the result-lifecycle exceptions
  (`ResultFailedError`, `ResultTimeoutError`, `ResultTooLargeError`,
  `ResultIncompleteError`, `ResultUnavailableError`) so callers can catch them
  with a single `except`.

### Changed

- `from hotdata import QueryApi` / `ResultsApi` now resolve to the enhanced
  clients (429 retry + truncation auto-follow; Arrow IPC fetch) instead of the
  bare generated classes, so the default happy path gets the safe behavior the
  query contract needs. The raw generated classes remain importable from
  `hotdata.api.query_api` / `hotdata.api.results_api`.

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
