# ListIndexesPageResponse

A page of indexes, across tables.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of indexes on this page. | 
**has_more** | **bool** | Whether more indexes follow. Fetch them with &#x60;next_cursor&#x60;. | 
**indexes** | [**List[IndexEntryResponse]**](IndexEntryResponse.md) | Indexes on this page. | 
**limit** | **int** | Page size used. | 
**next_cursor** | **str** | Cursor for the next page, present only when &#x60;has_more&#x60; is true. Pass it as the &#x60;cursor&#x60; query parameter. | [optional] 

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


