# QueryRunInfo

Single query run for listing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bytes_scanned** | **int** | Bytes this query actually fetched from storage. Not a measure of how much data the query covered — it counts the reads that reached storage, so the same SQL over the same rows reports a different number depending on what was already cached.  &#x60;null&#x60; means the query touched no table at all (for example a constant expression like &#x60;SELECT 1&#x60;).  &#x60;0&#x60; means the query read a table but fetched nothing from storage. It is a normal, common answer, not an error or a missing measurement, and it does not mean the query did no work — &#x60;rows_scanned&#x60; shows the rows it went through. The usual cause is a warm cache: re-running a query whose data or file metadata is already held in memory reports far fewer bytes than the first run, frequently &#x60;0&#x60;, with &#x60;rows_scanned&#x60; unchanged. A query answered from table statistics alone (a row count, say) also reports &#x60;0&#x60;.  Because of this, &#x60;bytes_scanned&#x60; is not a proxy for query cost or query volume. &#x60;GET /v1/usage&#x60; sums this field over a period, so that total is the storage read a workspace caused, not the work its queries did: repeating one query cheaply adds little or nothing to it. | [optional] 
**completed_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | 
**error_message** | **str** |  | [optional] 
**execution_time_ms** | **int** |  | [optional] 
**id** | **str** |  | 
**result_id** | **str** |  | [optional] 
**row_count** | **int** |  | [optional] 
**rows_scanned** | **int** | Total rows read from storage to run this query, before any filtering or aggregation. Distinct from &#x60;row_count&#x60;, which is how many rows the query returned. &#x60;null&#x60; when the query reads no table data from storage. | [optional] 
**saved_query_id** | **str** |  | [optional] 
**saved_query_version** | **int** |  | [optional] 
**server_processing_ms** | **int** | Total server-side processing time for this query (milliseconds). Measured from query start to result ready. Includes SQL execution, task spawning, and result preparation. Does not include network transit. Populated for all completed query runs (sync and async). | [optional] 
**snapshot_id** | **str** |  | 
**sql_hash** | **str** |  | 
**sql_text** | **str** |  | 
**status** | **str** |  | 
**trace_id** | **str** |  | [optional] 
**user_public_id** | **str** | Who ran this query: the account id from the access token the request was made with. Use it to group a caller&#39;s query history.  Requests made with a credential that identifies no account instead record an opaque &#x60;user_&#x60;-prefixed identifier, which is stable for that credential but cannot be resolved to an account. | [optional] 
**warning_message** | **str** |  | [optional] 

## Example

```python
from hotdata.models.query_run_info import QueryRunInfo

# TODO update the JSON string below
json = "{}"
# create an instance of QueryRunInfo from a JSON string
query_run_info_instance = QueryRunInfo.from_json(json)
# print the JSON string representation of the object
print(QueryRunInfo.to_json())

# convert the object into a dict
query_run_info_dict = query_run_info_instance.to_dict()
# create an instance of QueryRunInfo from a dict
query_run_info_from_dict = QueryRunInfo.from_dict(query_run_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


