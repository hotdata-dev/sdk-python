# hotdata

Official Python client for the [Hotdata](https://www.hotdata.dev) HTTP API: workspaces, connections, datasets, SQL queries, results, secrets, uploads, indexes, jobs, embedding providers, and workspace context.

## Requirements

Python 3.9+

## Install

```sh
pip install hotdata
```

For an unreleased revision:

```sh
pip install "git+https://github.com/hotdata-dev/sdk-python.git"
```

From a local checkout (editable):

```sh
pip install -e .
```

## Authentication

The API uses an **API key** sent as `Authorization: Bearer <key>`, plus an **`X-Workspace-Id`** header on requests scoped to a workspace.

```python
import hotdata

configuration = hotdata.Configuration(
    api_key="YOUR_API_KEY",
    workspace_id="YOUR_WORKSPACE_ID",
)
```

`host` defaults to `https://api.hotdata.dev`. Override it if you target another environment.

## Usage

```python
import hotdata
from hotdata.rest import ApiException

configuration = hotdata.Configuration(
    api_key="YOUR_API_KEY",
    workspace_id="YOUR_WORKSPACE_ID",
)

with hotdata.ApiClient(configuration) as api_client:
    workspaces = hotdata.WorkspacesApi(api_client)
    try:
        response = workspaces.list_workspaces()
    except ApiException as e:
        print(f"API error: {e.status} {e.reason}\n{e.body}")
```

Each `Api` class groups endpoints by resource. Construct the client, then call the typed methods you need.

## Arrow results

Query results can be fetched as an [Apache Arrow](https://arrow.apache.org/) IPC stream instead of JSON, which is faster and far more memory-efficient for large result sets. Install the optional extra:

```sh
pip install 'hotdata[arrow]'
```

Use `hotdata.arrow.ResultsApi` (a drop-in subclass of `ResultsApi` that adds Arrow methods):

```python
from hotdata import ApiClient, Configuration
from hotdata.arrow import ResultsApi

with ApiClient(Configuration(api_key="...", workspace_id="...")) as client:
    results = ResultsApi(client)

    # Buffered: returns a pyarrow.Table.
    table = results.get_result_arrow(result_id)

    # Streaming: yields a pyarrow.RecordBatchStreamReader without
    # materializing the full table in memory.
    with results.stream_result_arrow(result_id) as reader:
        for batch in reader:
            ...
```

Both methods accept `offset` and `limit` for pagination. They raise `hotdata.arrow.ResultNotReadyError` if the result is still pending or processing — poll `results.get_result(result_id)` until `status == "ready"` first.

## File uploads

`hotdata.uploads.UploadsApi` (also the default `hotdata.UploadsApi`) adds
`upload_file`, which uploads a local file **directly to object storage** and
finalizes it in one call. It opens an upload session, `PUT`s the bytes straight
to storage — a single `PUT` for a small file, concurrent part `PUT`s for a large
one — then finalizes. The bytes never round-trip through the API.

```python
from hotdata import ApiClient, Configuration, UploadsApi

with ApiClient(Configuration(api_key="...", workspace_id="...")) as client:
    uploads = UploadsApi(client)

    finalized = uploads.upload_file(
        "data.parquet",
        content_type="application/parquet",
        progress=lambda done, total: print(f"{done}/{total} bytes"),
    )

    # Pass finalized.upload_id to the managed-table load endpoint.
    print(finalized.upload_id)
```

`upload_file` accepts a path, raw `bytes`, or a seekable binary file object
(`size` is inferred for all three; a file object is read from its current
position to the end). The SDK picks single vs. multipart from the size,
auto-scales the part size, and bounds part concurrency to a peak-memory budget
(override with `part_size` / `max_concurrency` / `part_retry`). Storage `PUT`s go
through a dedicated, header-isolated connection pool, so the SDK's auth and
workspace headers never reach object storage (which would otherwise reject the
upload). Finalize is sent with retries disabled so the exactly-once call is never
accidentally replayed.

Failures surface as a typed hierarchy under `hotdata.uploads.UploadError`:
`StorageError` (storage returned a non-2xx), `StorageTransportError` (the PUT
failed before any response), `MissingETagError`, `MalformedSessionError`, and
`SizeLimitError`. Opening the session or finalizing raises the usual
`hotdata.exceptions.ApiException` — for example a `501` `PRESIGN_UNSUPPORTED`,
meaning the backend cannot issue upload URLs.

For that fallback (or to upload from a non-seekable stream), use `upload_stream`,
which sends the bytes to the legacy `POST /v1/files` endpoint in one request,
streaming a file object without buffering it in memory:

```python
with open("data.parquet", "rb") as f:
    resp = uploads.upload_stream(f, content_type="application/parquet")
print(resp.id)
```

Note `upload_file` shadows the generated raw-body `upload_file(body=...)`; that
raw operation is still reachable at
`hotdata.api.uploads_api.UploadsApi.upload_file`.

## API reference

Generated Markdown for every operation and model is in [`docs/`](https://github.com/hotdata-dev/sdk-python/tree/main/docs):

- Resource APIs: `docs/*Api.md` (for example [`QueryApi.md`](https://github.com/hotdata-dev/sdk-python/blob/main/docs/QueryApi.md))
- Request and response models: `docs/<ModelName>.md`

## Support

Questions and issues: [github.com/hotdata-dev/sdk-python](https://github.com/hotdata-dev/sdk-python).
