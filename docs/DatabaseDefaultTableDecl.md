# DatabaseDefaultTableDecl

One table declaration inside a default-catalog schema, supplied at database-create time.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**constant_per_key** | **List[str]** | Columns whose value is determined by this table&#39;s &#x60;key&#x60;: for every uploaded row, every stored row sharing its key holds the same value of these columns.  Declaring this lets a keyed mutation (&#x60;delete&#x60;, &#x60;update&#x60;, &#x60;upsert&#x60;) restrict its search for prior versions to the values the upload carries, which prunes far harder than the key alone when the key&#39;s own file statistics are weak. Omit (the default) for the unrestricted search.  **Correctness-affecting, not a hint.** If the assertion is false, a mutation supersedes one version of a key and appends beside another, silently duplicating it. Declare it only where the invariant is established. | [optional] 
**key** | **List[str]** | Columns that uniquely identify a row, enabling the key-based load modes (&#x60;delete&#x60;, &#x60;update&#x60;, &#x60;upsert&#x60;) on this table: those loads match rows by these columns&#39; values. Omit (the default) to declare no key; the table can still be loaded with &#x60;replace&#x60; and &#x60;append&#x60;, but key-based modes are then rejected. | [optional] 
**name** | **str** |  | 
**partition_by** | [**List[TablePartitionKey]**](TablePartitionKey.md) | Partition keys for this table, applied in order. Omit for no partitioning. Declared when the table is created and fixed thereafter. | [optional] 
**sorted_by** | [**List[TableSortKey]**](TableSortKey.md) | Sort keys for this table, applied in order. Omit for no sort order. Declared when the table is created and fixed thereafter. | [optional] 

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


