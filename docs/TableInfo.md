# TableInfo

Single table metadata

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[ColumnInfo]**](ColumnInfo.md) |  | [optional] 
**connection** | **str** |  | 
**last_sync** | **str** |  | [optional] 
**partition_by** | [**List[TablePartitionKey]**](TablePartitionKey.md) | The table&#39;s partition keys, in the order they were declared when the table was created. Empty when the table is not partitioned.  A table&#39;s storage layout is fixed when the table is created and cannot be changed afterwards, so this is how to confirm a table really was created with the layout that was asked for. The field is always present: an empty array means \&quot;no partitioning declared\&quot;, which is not the same as a response that omits the field entirely.  Reported for tables in a hotdata-managed database, which are the only ones whose layout is declared here. A table discovered from an external connection always reports an empty array — its layout belongs to the upstream system, so an empty array there means \&quot;not known from here\&quot;, not \&quot;confirmed unpartitioned\&quot;. | 
**var_schema** | **str** |  | 
**sorted_by** | [**List[TableSortKey]**](TableSortKey.md) | The table&#39;s sort keys, in the order they were declared when the table was created. Empty when no sort order was declared. Always present, and limited to tables in a hotdata-managed database, for the same reasons as &#x60;partition_by&#x60;. | 
**synced** | **bool** |  | 
**table** | **str** |  | 

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


