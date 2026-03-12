# ColumnProfileInfo

Statistics for a single column.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cardinality** | **int** | Approximate number of distinct non-null values | 
**data_type** | **str** | Arrow data type (e.g. \&quot;Utf8\&quot;, \&quot;Int32\&quot;, \&quot;Timestamp(Microsecond, Some(\\\&quot;UTC\\\&quot;))\&quot;) | 
**name** | **str** | Column name | 
**null_count** | **int** | Number of null values | 
**null_percentage** | **float** | Percentage of null values (0.0 to 100.0) | 
**profile** | [**ColumnProfileDetail**](ColumnProfileDetail.md) |  | [optional] 

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


