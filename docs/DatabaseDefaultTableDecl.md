# DatabaseDefaultTableDecl

A table to create with the database. Its columns come from the first data you load.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**constant_per_key** | **List[str]** | Columns that always hold the same value for rows with the same &#x60;key&#x60;. Makes keyed loads faster, but if it is not true, keyed loads silently duplicate rows. | [optional] 
**key** | **List[str]** | Columns that identify a row. Required for &#x60;delete&#x60;, &#x60;update&#x60; and &#x60;upsert&#x60; loads unless the load request gives its own &#x60;key&#x60;. | [optional] 
**layout** | [**TableLayout**](TableLayout.md) | &#x60;analytical&#x60; (default) for fast scans, or &#x60;point_lookup&#x60; for fast fetches of single rows, as vector search does. Cannot be changed later. | [optional] 
**name** | **str** |  | 
**partition_by** | [**List[TablePartitionKey]**](TablePartitionKey.md) | Columns to partition the table by, in order. Cannot be changed later. | [optional] 
**sorted_by** | [**List[TableSortKey]**](TableSortKey.md) | Columns to sort the table by, in order. Cannot be changed later, and a sorted table cannot be indexed. | [optional] 

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


