# GetDatabaseContextResponse

Response body for GET `/v1/databases/{database_id}/context/{name}`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**context** | [**DatabaseContextEntry**](DatabaseContextEntry.md) |  | 

## Example

```python
from hotdata.models.get_database_context_response import GetDatabaseContextResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetDatabaseContextResponse from a JSON string
get_database_context_response_instance = GetDatabaseContextResponse.from_json(json)
# print the JSON string representation of the object
print(GetDatabaseContextResponse.to_json())

# convert the object into a dict
get_database_context_response_dict = get_database_context_response_instance.to_dict()
# create an instance of GetDatabaseContextResponse from a dict
get_database_context_response_from_dict = GetDatabaseContextResponse.from_dict(get_database_context_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


