# ColumnProfileDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**values** | [**List[CategoryValueInfo]**](CategoryValueInfo.md) | Distinct values with their counts, ordered by count descending | 
**type** | **str** |  | 
**avg_length** | **float** | Average string length | 
**max_length** | **int** | Longest string length in the column | 
**min_length** | **int** | Shortest string length in the column | 
**max** | **str** | Latest value as ISO-8601 string | 
**mean** | **float** | Arithmetic mean | 
**min** | **str** | Earliest value as ISO-8601 string | 
**false_count** | **int** | Number of false values | 
**true_count** | **int** | Number of true values | 

## Example

```python
from hotdata.models.column_profile_detail import ColumnProfileDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnProfileDetail from a JSON string
column_profile_detail_instance = ColumnProfileDetail.from_json(json)
# print the JSON string representation of the object
print(ColumnProfileDetail.to_json())

# convert the object into a dict
column_profile_detail_dict = column_profile_detail_instance.to_dict()
# create an instance of ColumnProfileDetail from a dict
column_profile_detail_from_dict = ColumnProfileDetail.from_dict(column_profile_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


