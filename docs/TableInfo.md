# TableInfo

Single table metadata

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[ColumnInfo]**](ColumnInfo.md) |  | [optional] 
**connection** | **str** |  | 
**last_sync** | **object** |  | [optional] 
**var_schema** | **str** |  | 
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


