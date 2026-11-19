# QueryResponse

Result of a query that finished within the request.  `rows` holds the result, or a preview of it when `truncated` is true. The result is also saved in the background so you can fetch it again with `result_id`. To know when the saved copy is ready, poll `GET /v1/query-runs/{query_run_id}` (with the `X-Database-Id` header) until its `status` is `succeeded`, then read `result_id` from the run. Do not poll `GET /v1/results/{id}` for this: it returns the full result data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **List[str]** | Column names, in order. | 
**execution_time_ms** | **int** | Time the query took to run, in milliseconds. | 
**nullable** | **List[bool]** | Whether each column, in the same order as &#x60;columns&#x60;, can hold nulls. | 
**preview_row_count** | **int** | Number of rows in this response. | 
**query_run_id** | **str** | ID of the query run. | 
**result_id** | **str** | ID to fetch this result again with &#x60;GET /v1/results/{id}&#x60;. Null only when every row is in this response but the result could not be saved; see &#x60;warning&#x60;. | [optional] 
**rollup** | [**RollupUsage**](RollupUsage.md) | Whether a rollup answered the query. Absent when no table the query read has a rollup, or rollups are turned off for the query. | [optional] 
**row_count** | **int** | Deprecated: use &#x60;preview_row_count&#x60; or &#x60;total_row_count&#x60;. Always equal to &#x60;preview_row_count&#x60;. | 
**rows** | **List[List[object]]** | Result rows. Each row is an array of values in column order. | 
**total_row_count** | **int** | Number of rows in the full result. Null while a truncated result is still being saved; read &#x60;row_count&#x60; from the query run once it succeeds. | [optional] 
**truncated** | **bool** | True when &#x60;rows&#x60; is only a preview of a larger result. Fetch the full result with &#x60;result_id&#x60;. | 
**warning** | **str** | Why the result could not be saved. Present only when &#x60;result_id&#x60; is null; every row is still in this response. | [optional] 

## Example

```python
from hotdata.models.query_response import QueryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of QueryResponse from a JSON string
query_response_instance = QueryResponse.from_json(json)
# print the JSON string representation of the object
print(QueryResponse.to_json())

# convert the object into a dict
query_response_dict = query_response_instance.to_dict()
# create an instance of QueryResponse from a dict
query_response_from_dict = QueryResponse.from_dict(query_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


