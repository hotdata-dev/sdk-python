# AddManagedSchemaRequest

Request body for adding a schema to an existing managed catalog: `POST /v1/connections/{id}/schemas` and `POST /v1/databases/{id}/schemas`. `tables` is optional — omit it to declare an empty schema and add tables later.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**tables** | [**List[AddManagedTableDecl]**](AddManagedTableDecl.md) |  | [optional] 

## Example

```python
from hotdata.models.add_managed_schema_request import AddManagedSchemaRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddManagedSchemaRequest from a JSON string
add_managed_schema_request_instance = AddManagedSchemaRequest.from_json(json)
# print the JSON string representation of the object
print(AddManagedSchemaRequest.to_json())

# convert the object into a dict
add_managed_schema_request_dict = add_managed_schema_request_instance.to_dict()
# create an instance of AddManagedSchemaRequest from a dict
add_managed_schema_request_from_dict = AddManagedSchemaRequest.from_dict(add_managed_schema_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


