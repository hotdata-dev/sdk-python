# TableInfo

A table and its metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[ColumnInfo]**](ColumnInfo.md) | Table columns. Present only when the request sets &#x60;include_columns&#x3D;true&#x60;. | [optional] 
**connection** | **str** | Name of the connection that holds the table. | 
**constant_per_key** | **List[str]** | Columns that hold the same value for every row sharing a key, which lets keyed mutations search fewer files; empty when none are declared. Unlike &#x60;partition_by&#x60; and &#x60;sorted_by&#x60;, this can change after creation. | 
**last_sync** | **str** | When the table&#39;s data was last loaded or synced; null if never. | [optional] 
**layout** | [**TableLayout**](TableLayout.md) | Storage layout. Fixed at creation. | 
**partition_by** | [**List[TablePartitionKey]**](TablePartitionKey.md) | Partition keys, in the order declared when the table was created; empty when it is not partitioned. Reported only for tables in a Hotdata-instant database: other tables always return an empty array. | 
**var_schema** | **str** | Schema name. | 
**sorted_by** | [**List[TableSortKey]**](TableSortKey.md) | Sort keys, in the order declared when the table was created; empty when none were declared. Reported only for tables in a Hotdata-managed database, like &#x60;partition_by&#x60;. | 
**synced** | **bool** | Whether the table has data loaded. | 
**table** | **str** | Table name. | 

## Example

```python
from hotdata.models.table_info import TableInfo

# TODO update the JSON string below
json = "{}"
# create an instance of TableInfo from a JSON string
table_info_instance = TableInfo.from_json(json)
# print the JSON string representation of the object
print(TableInfo.to_json())

# convert the object into a dict
table_info_dict = table_info_instance.to_dict()
# create an instance of TableInfo from a dict
table_info_from_dict = TableInfo.from_dict(table_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


