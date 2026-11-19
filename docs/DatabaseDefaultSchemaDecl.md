# DatabaseDefaultSchemaDecl

A schema to create with the database.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**tables** | [**List[DatabaseDefaultTableDecl]**](DatabaseDefaultTableDecl.md) | Tables to create in the schema. You can also add tables later. | [optional] 

## Example

```python
from hotdata.models.database_default_schema_decl import DatabaseDefaultSchemaDecl

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseDefaultSchemaDecl from a JSON string
database_default_schema_decl_instance = DatabaseDefaultSchemaDecl.from_json(json)
# print the JSON string representation of the object
print(DatabaseDefaultSchemaDecl.to_json())

# convert the object into a dict
database_default_schema_decl_dict = database_default_schema_decl_instance.to_dict()
# create an instance of DatabaseDefaultSchemaDecl from a dict
database_default_schema_decl_from_dict = DatabaseDefaultSchemaDecl.from_dict(database_default_schema_decl_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


