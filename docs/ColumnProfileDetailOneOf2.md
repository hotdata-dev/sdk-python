# ColumnProfileDetailOneOf2


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max** | **str** | Maximum value (string to preserve precision for large integers and decimals) | 
**mean** | **float** | Arithmetic mean | 
**min** | **str** | Minimum value (string to preserve precision for large integers and decimals) | 
**type** | **str** |  | 

## Example

```python
from hotdata.models.column_profile_detail_one_of2 import ColumnProfileDetailOneOf2

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnProfileDetailOneOf2 from a JSON string
column_profile_detail_one_of2_instance = ColumnProfileDetailOneOf2.from_json(json)
# print the JSON string representation of the object
print(ColumnProfileDetailOneOf2.to_json())

# convert the object into a dict
column_profile_detail_one_of2_dict = column_profile_detail_one_of2_instance.to_dict()
# create an instance of ColumnProfileDetailOneOf2 from a dict
column_profile_detail_one_of2_from_dict = ColumnProfileDetailOneOf2.from_dict(column_profile_detail_one_of2_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


