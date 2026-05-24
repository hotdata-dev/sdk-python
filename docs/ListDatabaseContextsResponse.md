# ListDatabaseContextsResponse

Response body for GET `/v1/databases/{database_id}/context`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contexts** | [**List[DatabaseContextEntry]**](DatabaseContextEntry.md) |  | 

## Example

```python
from hotdata.models.list_database_contexts_response import ListDatabaseContextsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListDatabaseContextsResponse from a JSON string
list_database_contexts_response_instance = ListDatabaseContextsResponse.from_json(json)
# print the JSON string representation of the object
print(ListDatabaseContextsResponse.to_json())

# convert the object into a dict
list_database_contexts_response_dict = list_database_contexts_response_instance.to_dict()
# create an instance of ListDatabaseContextsResponse from a dict
list_database_contexts_response_from_dict = ListDatabaseContextsResponse.from_dict(list_database_contexts_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


