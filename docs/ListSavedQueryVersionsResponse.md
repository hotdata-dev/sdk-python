# ListSavedQueryVersionsResponse

Response body for GET /v1/queries/{id}/versions

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | 
**has_more** | **bool** |  | 
**limit** | **int** |  | 
**offset** | **int** |  | 
**saved_query_id** | **str** |  | 
**versions** | [**List[SavedQueryVersionInfo]**](SavedQueryVersionInfo.md) |  | 

## Example

```python
from hotdata.models.list_saved_query_versions_response import ListSavedQueryVersionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListSavedQueryVersionsResponse from a JSON string
list_saved_query_versions_response_instance = ListSavedQueryVersionsResponse.from_json(json)
# print the JSON string representation of the object
print(ListSavedQueryVersionsResponse.to_json())

# convert the object into a dict
list_saved_query_versions_response_dict = list_saved_query_versions_response_instance.to_dict()
# create an instance of ListSavedQueryVersionsResponse from a dict
list_saved_query_versions_response_from_dict = ListSavedQueryVersionsResponse.from_dict(list_saved_query_versions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


