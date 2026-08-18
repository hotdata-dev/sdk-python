# LoadManagedTableRequest

Request body for the managed-table load endpoints — the connection-scoped `POST /v1/connections/{connection_id}/schemas/{schema}/tables/{table}/loads` and the database-scoped equivalent.  Publishes data to the named table from one of three sources: a previously uploaded file (`upload_id`), a persisted query result (`result_id`), or data sent inline in this request (`data`). Provide exactly one. `mode` selects whether the data replaces the table's contents or is appended on top of them.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_async** | **bool** | When true, run the load as a background job and return a job ID to poll instead of blocking until it finishes. Recommended for large uploads, which can take longer than an HTTP request should stay open. | [optional] [default to False]
**async_after_ms** | **int** | If set (requires &#x60;async&#x60; &#x3D; true), wait up to this many milliseconds for the load to finish: if it completes in time the full result is returned (200), otherwise a 202 with a job ID to poll. Must be between 1000 and the server maximum; a value out of that range, or set without &#x60;async&#x60; &#x3D; true, is rejected with 400. | [optional] 
**columns** | [**Dict[str, ColumnDefinition]**](ColumnDefinition.md) | Column types for inline &#x60;data&#x60;, keyed by column name. Optional — types are detected from the data when omitted.  Each value is either a type name (&#x60;\&quot;VARCHAR\&quot;&#x60;, &#x60;\&quot;BIGINT\&quot;&#x60;, &#x60;\&quot;DECIMAL(10,2)\&quot;&#x60;) or an object carrying explicit parameters (&#x60;{\&quot;type\&quot;: \&quot;DECIMAL\&quot;, \&quot;precision\&quot;: 10, \&quot;scale\&quot;: 2}&#x60;). Supported types: &#x60;VARCHAR&#x60;, &#x60;TEXT&#x60;, &#x60;STRING&#x60;, &#x60;CHAR&#x60;, &#x60;BOOLEAN&#x60;, &#x60;TINYINT&#x60;, &#x60;SMALLINT&#x60;, &#x60;INTEGER&#x60;, &#x60;BIGINT&#x60;, &#x60;UTINYINT&#x60;, &#x60;USMALLINT&#x60;, &#x60;UINTEGER&#x60;, &#x60;UBIGINT&#x60;, &#x60;REAL&#x60;, &#x60;FLOAT&#x60;, &#x60;DOUBLE&#x60;, &#x60;DECIMAL&#x60;, &#x60;NUMERIC&#x60;, &#x60;DATE&#x60;, &#x60;TIME&#x60;, &#x60;TIMESTAMP&#x60;, &#x60;TIMESTAMPTZ&#x60;, &#x60;BINARY&#x60;, &#x60;BLOB&#x60;, &#x60;UUID&#x60;, and &#x60;JSON&#x60;.  When given, it must name every column in the CSV header and no others. Only valid together with &#x60;data&#x60;. | [optional] 
**data** | **str** | The data to load, sent inline in this request instead of being uploaded first — the quickest way to get a small table in. CSV text with a header row, up to 2 MiB.  Larger payloads are rejected with &#x60;413&#x60; and the error code &#x60;INLINE_DATA_TOO_LARGE&#x60;; upload the file (see &#x60;POST /v1/uploads&#x60;) and load it by &#x60;upload_id&#x60; instead. Column types are detected from the data unless &#x60;columns&#x60; declares them. Provide exactly one of this, &#x60;upload_id&#x60;, or &#x60;result_id&#x60;. | [optional] 
**format** | **str** | File format of the upload: &#x60;\&quot;csv\&quot;&#x60;, &#x60;\&quot;json\&quot;&#x60;, or &#x60;\&quot;parquet\&quot;&#x60;. Optional — when omitted, the format is auto-detected from the upload&#39;s &#x60;Content-Type&#x60; and, failing that, from the file contents. Provide it explicitly to override detection or when the contents are ambiguous. &#x60;\&quot;json\&quot;&#x60; expects newline-delimited JSON (one object per line), not a JSON array.  With inline &#x60;data&#x60; the only accepted value is &#x60;\&quot;csv\&quot;&#x60; (the default); upload the file and load it by &#x60;upload_id&#x60; for any other format. Not valid with &#x60;result_id&#x60; — query results are always parquet. | [optional] 
**idempotency_key** | **str** | A key of your own that makes this load safe to retry. Send the same key again — after a timeout, a dropped connection, or any answer you did not receive — and the load runs at most once: the retry returns the original result instead of loading the rows a second time.  Generate the key before the first attempt (a UUID is a good choice) and reuse it for every retry of that same data. Use a new key for the next batch: sending different data under a key already used returns &#x60;409&#x60;, and loads nothing.  A retry sent while the first attempt is still running also returns &#x60;409&#x60;, because the table is busy with it; wait and send the same key again. A &#x60;409&#x60; never means the data was loaded twice — under one key it is loaded once or not at all.  Only valid with inline &#x60;data&#x60;. A load from &#x60;upload_id&#x60; is already safe to retry — re-send the same &#x60;upload_id&#x60;. Keys are at most 255 characters. | [optional] 
**key** | **List[str]** | Key columns identifying rows for &#x60;\&quot;delete\&quot;&#x60;, &#x60;\&quot;update\&quot;&#x60;, and &#x60;\&quot;upsert\&quot;&#x60; loads — the columns whose values decide which existing row an incoming row removes, updates, or replaces. Omit to use the key the table was created with. Keep the key consistent across loads of the same table: changing it re-targets which rows are matched. Ignored for &#x60;\&quot;replace\&quot;&#x60; and &#x60;\&quot;append\&quot;&#x60;. | [optional] 
**mode** | **str** | How the data is applied: &#x60;\&quot;replace\&quot;&#x60; overwrites the table&#39;s contents, &#x60;\&quot;append\&quot;&#x60; inserts the new rows on top of the existing data. | 
**result_id** | **str** | ID of a persisted query result (see &#x60;GET /v1/results/{result_id}&#x60;) to publish as the table&#39;s contents. The result is copied into the table, so the table keeps its data even after the result expires. A result can be loaded into any number of tables. Provide exactly one of this, &#x60;upload_id&#x60;, or &#x60;data&#x60;. | [optional] 
**upload_id** | **str** | ID of a previously-staged upload (see &#x60;POST /v1/uploads&#x60;). The upload is claimed atomically; concurrent loads against the same &#x60;upload_id&#x60; return 409. Provide exactly one of this, &#x60;result_id&#x60;, or &#x60;data&#x60;. | [optional] 

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


