# ListIndexesPageResponse

Response body for `GET /v1/indexes` (paginated, cross-table).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | 
**has_more** | **bool** |  | 
**indexes** | [**List[IndexEntryResponse]**](IndexEntryResponse.md) |  | 
**limit** | **int** |  | 
**next_cursor** | **str** |  | [optional] 

## Example

```python
from hotdata.models.list_indexes_page_response import ListIndexesPageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListIndexesPageResponse from a JSON string
list_indexes_page_response_instance = ListIndexesPageResponse.from_json(json)
# print the JSON string representation of the object
print(ListIndexesPageResponse.to_json())

# convert the object into a dict
list_indexes_page_response_dict = list_indexes_page_response_instance.to_dict()
# create an instance of ListIndexesPageResponse from a dict
list_indexes_page_response_from_dict = ListIndexesPageResponse.from_dict(list_indexes_page_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


