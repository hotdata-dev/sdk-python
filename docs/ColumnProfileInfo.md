# ColumnProfileInfo

Statistics for a single column.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cardinality** | **int** | Approximate number of distinct non-null values | 
**data_type** | **str** | Column data type, such as &#x60;Utf8&#x60; or &#x60;Int32&#x60;. | 
**name** | **str** | Column name | 
**null_count** | **int** | Number of null values | 
**null_percentage** | **float** | Percentage of null values (0.0 to 100.0) | 
**profile** | [**ColumnProfileDetail**](ColumnProfileDetail.md) | Statistics for the column&#39;s type. Absent when the column is all null or its type is not profiled. | [optional] 

## Example

```python
from hotdata.models.column_profile_info import ColumnProfileInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnProfileInfo from a JSON string
column_profile_info_instance = ColumnProfileInfo.from_json(json)
# print the JSON string representation of the object
print(ColumnProfileInfo.to_json())

# convert the object into a dict
column_profile_info_dict = column_profile_info_instance.to_dict()
# create an instance of ColumnProfileInfo from a dict
column_profile_info_from_dict = ColumnProfileInfo.from_dict(column_profile_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


