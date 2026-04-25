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

## API reference

Generated Markdown for every operation and model is in [`docs/`](https://github.com/hotdata-dev/sdk-python/tree/main/docs):

- Resource APIs: `docs/*Api.md` (for example [`QueryApi.md`](https://github.com/hotdata-dev/sdk-python/blob/main/docs/QueryApi.md))
- Request and response models: `docs/<ModelName>.md`

Use your editor or GitHub file search there instead of duplicating large tables in this file.

## Support

Questions and issues: [github.com/hotdata-dev/sdk-python](https://github.com/hotdata-dev/sdk-python).
