# ColumnProfileDetailOneOf1

High-cardinality text column (>200 distinct values).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**avg_length** | **float** | Average string length | 
**max_length** | **int** | Longest string length in the column | 
**min_length** | **int** | Shortest string length in the column | 
**type** | **str** |  | 

## Example

```python
from hotdata.models.column_profile_detail_one_of1 import ColumnProfileDetailOneOf1

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnProfileDetailOneOf1 from a JSON string
column_profile_detail_one_of1_instance = ColumnProfileDetailOneOf1.from_json(json)
# print the JSON string representation of the object
print(ColumnProfileDetailOneOf1.to_json())

# convert the object into a dict
column_profile_detail_one_of1_dict = column_profile_detail_one_of1_instance.to_dict()
# create an instance of ColumnProfileDetailOneOf1 from a dict
column_profile_detail_one_of1_from_dict = ColumnProfileDetailOneOf1.from_dict(column_profile_detail_one_of1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


