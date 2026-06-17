# QueryRunInfo

Single query run for listing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bytes_scanned** | **int** | Total bytes of table data read from storage to run this query. &#x60;null&#x60; when the query touches no table at all (for example a constant expression like &#x60;SELECT 1&#x60;). May be &#x60;0&#x60; when the query reads a table but not its row data — for example a row count served from table statistics. | [optional] 
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
**user_public_id** | **str** | Caller identity derived from the Authorization Bearer token (SHA-256 hash). Format: &#x60;user_{first_10_hex_chars}&#x60;. | [optional] 
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


