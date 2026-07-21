# LoadManagedTableRequest

Request body for the managed-table load endpoints — the connection-scoped `POST /v1/connections/{connection_id}/schemas/{schema}/tables/{table}/loads` and the database-scoped equivalent.  Publishes data to the named table from one of two sources: a previously uploaded file (`upload_id`) or a persisted query result (`result_id`). Provide exactly one. CSV and JSON uploads are converted to columnar storage on load; Parquet uploads and query results are published directly. `mode` selects whether the data replaces the table's contents or is appended on top of them.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_async** | **bool** | When true, run the load as a background job and return a job ID to poll instead of blocking until it finishes. Recommended for large uploads, which can take longer than an HTTP request should stay open. | [optional] 
**async_after_ms** | **int** | If set (requires &#x60;async&#x60; &#x3D; true), wait up to this many milliseconds for the load to finish: if it completes in time the full result is returned (200), otherwise a 202 with a job ID to poll. Must be between 1000 and the server maximum; a value out of that range, or set without &#x60;async&#x60; &#x3D; true, is rejected with 400. | [optional] 
**format** | **str** | File format of the upload: &#x60;\&quot;csv\&quot;&#x60;, &#x60;\&quot;json\&quot;&#x60;, or &#x60;\&quot;parquet\&quot;&#x60;. Optional — when omitted, the format is auto-detected from the upload&#39;s &#x60;Content-Type&#x60; and, failing that, from the file contents. Provide it explicitly to override detection or when the contents are ambiguous. &#x60;\&quot;json\&quot;&#x60; expects newline-delimited JSON (one object per line), not a JSON array. Only applies to &#x60;upload_id&#x60;; query results are always parquet. | [optional] 
**key** | **List[str]** | Key columns identifying rows for &#x60;\&quot;delete\&quot;&#x60;, &#x60;\&quot;update\&quot;&#x60;, and &#x60;\&quot;upsert\&quot;&#x60; loads — the columns whose values decide which existing row an incoming row removes, updates, or replaces. Omit to use the key the table was created with. Keep the key consistent across loads of the same table: changing it re-targets which rows are matched. Ignored for &#x60;\&quot;replace\&quot;&#x60; and &#x60;\&quot;append\&quot;&#x60;. | [optional] 
**mode** | **str** | How the data is applied: &#x60;\&quot;replace\&quot;&#x60; overwrites the table&#39;s contents, &#x60;\&quot;append\&quot;&#x60; inserts the new rows on top of the existing data. | 
**result_id** | **str** | ID of a persisted query result (see &#x60;GET /v1/results/{result_id}&#x60;) to publish as the table&#39;s contents. The result is copied into the table, so the table keeps its data even after the result expires. A result can be loaded into any number of tables. Provide either this or &#x60;upload_id&#x60;, not both. | [optional] 
**upload_id** | **str** | ID of a previously-staged upload (see &#x60;POST /v1/uploads&#x60;). The upload is claimed atomically; concurrent loads against the same &#x60;upload_id&#x60; return 409. Provide either this or &#x60;result_id&#x60;, not both. | [optional] 

## Example

```python
from hotdata.models.load_managed_table_request import LoadManagedTableRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LoadManagedTableRequest from a JSON string
load_managed_table_request_instance = LoadManagedTableRequest.from_json(json)
# print the JSON string representation of the object
print(LoadManagedTableRequest.to_json())

# convert the object into a dict
load_managed_table_request_dict = load_managed_table_request_instance.to_dict()
# create an instance of LoadManagedTableRequest from a dict
load_managed_table_request_from_dict = LoadManagedTableRequest.from_dict(load_managed_table_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


