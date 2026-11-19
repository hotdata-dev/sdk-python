# QueryRunInfo

One execution of a query.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bytes_scanned** | **int** | Bytes the query read from storage. Cached data is not counted, so a repeated query often reports &#x60;0&#x60;; null when the query read no table. | [optional] 
**completed_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | 
**error_message** | **str** | Why the run failed. | [optional] 
**execution_time_ms** | **int** |  | [optional] 
**id** | **str** |  | 
**result_id** | **str** | ID of the saved result, ready to fetch once &#x60;status&#x60; is &#x60;succeeded&#x60;. Absent when no result was saved; &#x60;warning_message&#x60; then says why. | [optional] 
**rollup** | [**RollupUsage**](RollupUsage.md) | Whether a rollup answered the query. Absent when no table the query read has a rollup, rollups were turned off for the query, or the run has not been planned yet. On a failed run it says what planning chose. | [optional] 
**row_count** | **int** | Number of rows in the full result. | [optional] 
**rows_scanned** | **int** | Rows the query read, before filtering or aggregation. Null when the query read no table. | [optional] 
**saved_query_id** | **str** | ID of the saved query this run executed, if any. | [optional] 
**saved_query_version** | **int** | Version of the saved query this run executed, if any. | [optional] 
**server_processing_ms** | **int** | Time from query start until the result was ready, in milliseconds. Excludes network time. | [optional] 
**snapshot_id** | **str** |  | 
**sql_hash** | **str** |  | 
**sql_text** | **str** |  | 
**status** | **str** | &#x60;running&#x60;, &#x60;succeeded&#x60;, &#x60;failed&#x60; or &#x60;interrupted&#x60;. An interrupted run stopped before finishing and is safe to retry. | 
**trace_id** | **str** |  | [optional] 
**user_public_id** | **str** | Account that ran the query, taken from the access token. A credential with no account gets a stable &#x60;user_&#x60;-prefixed ID instead. | [optional] 
**warning_message** | **str** | A problem that did not fail the run, such as a result that could not be saved. | [optional] 

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


