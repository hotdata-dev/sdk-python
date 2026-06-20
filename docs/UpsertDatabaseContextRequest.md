# UpsertDatabaseContextRequest

Request body for POST `/v1/databases/{database_id}/context`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** |  | 
**name** | **str** | Upsert key in the catalog. Validated with table-name rules (preserves case): ASCII letter or &#x60;_&#x60; first; then alphanumeric or &#x60;_&#x60; only; 1–128 chars; not a SQL reserved word. | 

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


