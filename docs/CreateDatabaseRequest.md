# CreateDatabaseRequest

Request body for POST /databases

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Optional free-form display label (for UIs/CLIs). Not unique. Not an identifier — databases are always addressed by &#x60;id&#x60;. | [optional] 
**schemas** | [**List[DatabaseDefaultSchemaDecl]**](DatabaseDefaultSchemaDecl.md) | Optional schemas/tables to declare on the database&#39;s auto-created &#x60;default&#x60; catalog. Mirrors the &#x60;config.schemas&#x60; field of a managed &#x60;POST /v1/connections&#x60;. Tables declared here can be loaded via the standard managed-table load endpoint targeting &#x60;default_connection_id&#x60;. Omitted or empty means the default catalog starts empty. | [optional] 

## Example

```python
from hotdata.models.create_database_request import CreateDatabaseRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDatabaseRequest from a JSON string
create_database_request_instance = CreateDatabaseRequest.from_json(json)
# print the JSON string representation of the object
print(CreateDatabaseRequest.to_json())

# convert the object into a dict
create_database_request_dict = create_database_request_instance.to_dict()
# create an instance of CreateDatabaseRequest from a dict
create_database_request_from_dict = CreateDatabaseRequest.from_dict(create_database_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


