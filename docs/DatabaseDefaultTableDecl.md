# DatabaseDefaultTableDecl

One table declaration inside a default-catalog schema at database-create time. Mirrors `crate::source::ManagedTableDecl` shape so the controller can convert with a simple `.map`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 

## Example

```python
from hotdata.models.database_default_table_decl import DatabaseDefaultTableDecl

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseDefaultTableDecl from a JSON string
database_default_table_decl_instance = DatabaseDefaultTableDecl.from_json(json)
# print the JSON string representation of the object
print(DatabaseDefaultTableDecl.to_json())

# convert the object into a dict
database_default_table_decl_dict = database_default_table_decl_instance.to_dict()
# create an instance of DatabaseDefaultTableDecl from a dict
database_default_table_decl_from_dict = DatabaseDefaultTableDecl.from_dict(database_default_table_decl_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


