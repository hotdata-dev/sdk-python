# UpsertDatabaseContextRequest

Request body for POST `/v1/databases/{database_id}/context`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** | Text or Markdown, up to 512,000 characters. | 
**name** | **str** | Name of the entry; an existing entry with this name is replaced. 1 to 128 ASCII letters, digits or &#x60;_&#x60;, not starting with a digit, and not a SQL reserved word. | 

## Example

```python
from hotdata.models.upsert_database_context_request import UpsertDatabaseContextRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpsertDatabaseContextRequest from a JSON string
upsert_database_context_request_instance = UpsertDatabaseContextRequest.from_json(json)
# print the JSON string representation of the object
print(UpsertDatabaseContextRequest.to_json())

# convert the object into a dict
upsert_database_context_request_dict = upsert_database_context_request_instance.to_dict()
# create an instance of UpsertDatabaseContextRequest from a dict
upsert_database_context_request_from_dict = UpsertDatabaseContextRequest.from_dict(upsert_database_context_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


