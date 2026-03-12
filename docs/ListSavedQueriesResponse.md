# ListSavedQueriesResponse

Response body for GET /v1/queries

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | 
**has_more** | **bool** |  | 
**limit** | **int** |  | 
**offset** | **int** |  | 
**queries** | [**List[SavedQuerySummary]**](SavedQuerySummary.md) |  | 

## Example

```python
from hotdata.models.list_saved_queries_response import ListSavedQueriesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListSavedQueriesResponse from a JSON string
list_saved_queries_response_instance = ListSavedQueriesResponse.from_json(json)
# print the JSON string representation of the object
print(ListSavedQueriesResponse.to_json())

# convert the object into a dict
list_saved_queries_response_dict = list_saved_queries_response_instance.to_dict()
# create an instance of ListSavedQueriesResponse from a dict
list_saved_queries_response_from_dict = ListSavedQueriesResponse.from_dict(list_saved_queries_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


