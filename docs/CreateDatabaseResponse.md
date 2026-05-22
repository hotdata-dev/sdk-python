# CreateDatabaseResponse

Response body for POST /databases

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_connection_id** | **str** | Internal id of the connection that backs this database&#39;s &#x60;default&#x60; catalog. Workspace-level connection endpoints (list, get, health, delete, cache purge) refuse to act on this id — it is exposed only for the managed-tables load endpoint (&#x60;POST /v1/connections/{id}/schemas/{s}/tables/{t}/loads&#x60;) so callers can publish parquet into tables declared at database-create time. Addressing it directly in SQL is not the recommended path — use &#x60;default&#x60; inside an &#x60;X-Database-Id&#x60; scope instead. | 
**description** | **str** |  | [optional] 
**id** | **str** |  | 

## Example

```python
from hotdata.models.create_database_response import CreateDatabaseResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDatabaseResponse from a JSON string
create_database_response_instance = CreateDatabaseResponse.from_json(json)
# print the JSON string representation of the object
print(CreateDatabaseResponse.to_json())

# convert the object into a dict
create_database_response_dict = create_database_response_instance.to_dict()
# create an instance of CreateDatabaseResponse from a dict
create_database_response_from_dict = CreateDatabaseResponse.from_dict(create_database_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


