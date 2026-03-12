# ColumnInfo

Column metadata for API responses

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_type** | **str** |  | 
**name** | **str** |  | 
**nullable** | **bool** |  | 

## Example

```python
from hotdata.models.column_info import ColumnInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnInfo from a JSON string
column_info_instance = ColumnInfo.from_json(json)
# print the JSON string representation of the object
print(ColumnInfo.to_json())

# convert the object into a dict
column_info_dict = column_info_instance.to_dict()
# create an instance of ColumnInfo from a dict
column_info_from_dict = ColumnInfo.from_dict(column_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


