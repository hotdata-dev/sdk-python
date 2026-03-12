# ListQueryRunsResponse

Response body for GET /query-runs

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | 
**has_more** | **bool** |  | 
**limit** | **int** |  | 
**next_cursor** | **str** |  | [optional] 
**query_runs** | [**List[QueryRunInfo]**](QueryRunInfo.md) |  | 

## Example

```python
from hotdata.models.list_query_runs_response import ListQueryRunsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListQueryRunsResponse from a JSON string
list_query_runs_response_instance = ListQueryRunsResponse.from_json(json)
# print the JSON string representation of the object
print(ListQueryRunsResponse.to_json())

# convert the object into a dict
list_query_runs_response_dict = list_query_runs_response_instance.to_dict()
# create an instance of ListQueryRunsResponse from a dict
list_query_runs_response_from_dict = ListQueryRunsResponse.from_dict(list_query_runs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


