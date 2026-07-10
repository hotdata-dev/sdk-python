# AddManagedTableDecl

One table declaration inside an add-schema request body.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **List[str]** | Columns that uniquely identify a row, enabling the key-based load modes (&#x60;delete&#x60;, &#x60;update&#x60;, &#x60;upsert&#x60;) on this table: those loads match rows by these columns&#39; values. Omit (the default) to declare no key; the table can still be loaded with &#x60;replace&#x60; and &#x60;append&#x60;, but key-based modes are then rejected. | [optional] 
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


