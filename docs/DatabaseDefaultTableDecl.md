# DatabaseDefaultTableDecl

One table declaration inside a default-catalog schema, supplied at database-create time.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **List[str]** | Columns that uniquely identify a row, enabling the key-based load modes (&#x60;delete&#x60;, &#x60;update&#x60;, &#x60;upsert&#x60;) on this table: those loads match rows by these columns&#39; values. Omit (the default) to declare no key; the table can still be loaded with &#x60;replace&#x60; and &#x60;append&#x60;, but key-based modes are then rejected. | [optional] 
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


