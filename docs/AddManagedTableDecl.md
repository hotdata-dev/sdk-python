# AddManagedTableDecl

One table declaration inside an add-schema request body.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 

## Example

```python
from hotdata.models.add_managed_table_decl import AddManagedTableDecl

# TODO update the JSON string below
json = "{}"
# create an instance of AddManagedTableDecl from a JSON string
add_managed_table_decl_instance = AddManagedTableDecl.from_json(json)
# print the JSON string representation of the object
print(AddManagedTableDecl.to_json())

# convert the object into a dict
add_managed_table_decl_dict = add_managed_table_decl_instance.to_dict()
# create an instance of AddManagedTableDecl from a dict
add_managed_table_decl_from_dict = AddManagedTableDecl.from_dict(add_managed_table_decl_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


