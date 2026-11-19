# LoadManagedTableRequest

Data to load into a table. Give exactly one source: `upload_id`, `result_id`, or inline `data`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_async** | **bool** | Run the load in the background and return a job ID to poll. | [optional] [default to False]
**async_after_ms** | **int** | With &#x60;async: true&#x60;, wait up to this many milliseconds for the load before falling back to a job ID. Must be between 1000 and 30000. | [optional] 
**columns** | [**Dict[str, ColumnDefinition]**](ColumnDefinition.md) | Column types for inline &#x60;data&#x60;, by column name. Must list every CSV column; omit to detect types from the data. Each value is a type name such as &#x60;BIGINT&#x60; or &#x60;DECIMAL(10,2)&#x60;, or an object such as &#x60;{\&quot;type\&quot;: \&quot;DECIMAL\&quot;, \&quot;precision\&quot;: 10, \&quot;scale\&quot;: 2}&#x60;.  Types: &#x60;VARCHAR&#x60;, &#x60;TEXT&#x60;, &#x60;STRING&#x60;, &#x60;CHAR&#x60;, &#x60;BOOLEAN&#x60;, &#x60;TINYINT&#x60;, &#x60;SMALLINT&#x60;, &#x60;INTEGER&#x60;, &#x60;BIGINT&#x60;, &#x60;UTINYINT&#x60;, &#x60;USMALLINT&#x60;, &#x60;UINTEGER&#x60;, &#x60;UBIGINT&#x60;, &#x60;REAL&#x60;, &#x60;FLOAT&#x60;, &#x60;DOUBLE&#x60;, &#x60;DECIMAL&#x60;, &#x60;NUMERIC&#x60;, &#x60;DATE&#x60;, &#x60;TIME&#x60;, &#x60;TIMESTAMP&#x60;, &#x60;TIMESTAMPTZ&#x60;, &#x60;BINARY&#x60;, &#x60;BLOB&#x60;, &#x60;UUID&#x60;, &#x60;JSON&#x60;. | [optional] 
**data** | **str** | CSV text with a header row, up to 2 MiB. Larger data fails with 413 (&#x60;INLINE_DATA_TOO_LARGE&#x60;); upload it and use &#x60;upload_id&#x60; instead. | [optional] 
**format** | **str** | File format of the upload: &#x60;csv&#x60;, &#x60;json&#x60; (one object per line) or &#x60;parquet&#x60;. Defaults to detection from the upload&#39;s content type, then its contents. Inline &#x60;data&#x60; accepts only &#x60;csv&#x60;; not allowed with &#x60;result_id&#x60;. | [optional] 
**idempotency_key** | **str** | Your own key, such as a UUID, that makes a load of inline &#x60;data&#x60; safe to retry: a retry with the same key returns the first result and loads nothing. Up to 255 characters. Reusing a key for different data returns 409 &#x60;IDEMPOTENCY_KEY_CONFLICT&#x60;; a retry while the first attempt still runs returns a different 409, so wait and retry. | [optional] 
**key** | **List[str]** | Key columns for &#x60;delete&#x60;, &#x60;update&#x60; and &#x60;upsert&#x60;, overriding the table&#39;s key. Use the same key on every load of a table. | [optional] 
**mode** | **str** | How to apply the data. The first load into a table must be &#x60;replace&#x60;.  - &#x60;replace&#x60;: the data becomes the table&#39;s contents. - &#x60;append&#x60;: adds the rows. They must include every existing column (use   null for missing values); new columns are added. - &#x60;delete&#x60;: removes rows whose key matches a row in the data. - &#x60;update&#x60;: replaces rows whose key matches; other rows in the data are   ignored. - &#x60;upsert&#x60;: like &#x60;update&#x60;, but inserts rows whose key does not match.  &#x60;delete&#x60;, &#x60;update&#x60; and &#x60;upsert&#x60; need a key, from the table or from &#x60;key&#x60;. | 
**result_id** | **str** | ID of a saved query result. The rows are copied, so the table keeps them after the result expires. | [optional] 
**upload_id** | **str** | ID of a finalized upload. Two loads cannot use the same upload at once; the second gets 409. | [optional] 

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


