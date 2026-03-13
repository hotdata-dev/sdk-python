# QueryRunInfo

Single query run for listing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**completed_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | 
**error_message** | **str** |  | [optional] 
**execution_time_ms** | **int** |  | [optional] 
**id** | **str** |  | 
**result_id** | **str** |  | [optional] 
**row_count** | **int** |  | [optional] 
**saved_query_id** | **str** |  | [optional] 
**saved_query_version** | **int** |  | [optional] 
**snapshot_id** | **str** |  | 
**sql_hash** | **str** |  | 
**sql_text** | **str** |  | 
**status** | **str** |  | 
**trace_id** | **str** |  | [optional] 
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


