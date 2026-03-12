# ColumnProfileDetailOneOf3

Date or timestamp column.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max** | **str** | Latest value as ISO-8601 string | 
**min** | **str** | Earliest value as ISO-8601 string | 
**type** | **str** |  | 

## Example

```python
from hotdata.models.column_profile_detail_one_of3 import ColumnProfileDetailOneOf3

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnProfileDetailOneOf3 from a JSON string
column_profile_detail_one_of3_instance = ColumnProfileDetailOneOf3.from_json(json)
# print the JSON string representation of the object
print(ColumnProfileDetailOneOf3.to_json())

# convert the object into a dict
column_profile_detail_one_of3_dict = column_profile_detail_one_of3_instance.to_dict()
# create an instance of ColumnProfileDetailOneOf3 from a dict
column_profile_detail_one_of3_from_dict = ColumnProfileDetailOneOf3.from_dict(column_profile_detail_one_of3_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


