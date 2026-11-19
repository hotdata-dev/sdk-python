# ColumnInfo

A table column.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_type** | **str** | Column type, such as &#x60;Int64&#x60;, &#x60;Utf8&#x60; or &#x60;Timestamp(µs)&#x60;. | 
**name** | **str** | Column name. | 
**nullable** | **bool** | Whether the column can hold nulls. | 

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


