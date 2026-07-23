# ListDatabasesResponse

Response body for GET /databases. Results are returned one page at a time, newest first. When `has_more` is true, pass `next_cursor` back as the `cursor` query parameter to fetch the following page.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of databases returned in this page. | 
**databases** | [**List[DatabaseSummary]**](DatabaseSummary.md) |  | 
**has_more** | **bool** | Whether more databases exist beyond this page. | 
**limit** | **int** | Page size applied to this response (after clamping to the maximum). | 
**next_cursor** | **str** | Opaque cursor for the next page; present only when &#x60;has_more&#x60; is true. | [optional] 

## Example

```python
from hotdata.models.list_databases_response import ListDatabasesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListDatabasesResponse from a JSON string
list_databases_response_instance = ListDatabasesResponse.from_json(json)
# print the JSON string representation of the object
print(ListDatabasesResponse.to_json())

# convert the object into a dict
list_databases_response_dict = list_databases_response_instance.to_dict()
# create an instance of ListDatabasesResponse from a dict
list_databases_response_from_dict = ListDatabasesResponse.from_dict(list_databases_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


