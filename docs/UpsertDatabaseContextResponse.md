# UpsertDatabaseContextResponse

Response body for POST `/v1/databases/{database_id}/context`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**context** | [**DatabaseContextEntry**](DatabaseContextEntry.md) |  | 

## Example

```python
from hotdata.models.upsert_database_context_response import UpsertDatabaseContextResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpsertDatabaseContextResponse from a JSON string
upsert_database_context_response_instance = UpsertDatabaseContextResponse.from_json(json)
# print the JSON string representation of the object
print(UpsertDatabaseContextResponse.to_json())

# convert the object into a dict
upsert_database_context_response_dict = upsert_database_context_response_instance.to_dict()
# create an instance of UpsertDatabaseContextResponse from a dict
upsert_database_context_response_from_dict = UpsertDatabaseContextResponse.from_dict(upsert_database_context_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


