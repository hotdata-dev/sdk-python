# AddManagedSchemaRequest

A schema to add to a database or connection.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**tables** | [**List[AddManagedTableDecl]**](AddManagedTableDecl.md) | Tables to create in the schema. You can also add tables later. | [optional] 

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


