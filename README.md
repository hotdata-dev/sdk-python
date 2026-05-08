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

## API reference

Generated Markdown for every operation and model is in [`docs/`](https://github.com/hotdata-dev/sdk-python/tree/main/docs):

- Resource APIs: `docs/*Api.md` (for example [`QueryApi.md`](https://github.com/hotdata-dev/sdk-python/blob/main/docs/QueryApi.md))
- Request and response models: `docs/<ModelName>.md`

## Support

Questions and issues: [github.com/hotdata-dev/sdk-python](https://github.com/hotdata-dev/sdk-python).
