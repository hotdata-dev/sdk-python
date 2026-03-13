# ColumnProfileDetailOneOf


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**values** | [**List[CategoryValueInfo]**](CategoryValueInfo.md) | Distinct values with their counts, ordered by count descending | 
**type** | **str** |  | 

## Example

```python
from hotdata.models.column_profile_detail_one_of import ColumnProfileDetailOneOf

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnProfileDetailOneOf from a JSON string
column_profile_detail_one_of_instance = ColumnProfileDetailOneOf.from_json(json)
# print the JSON string representation of the object
print(ColumnProfileDetailOneOf.to_json())

# convert the object into a dict
column_profile_detail_one_of_dict = column_profile_detail_one_of_instance.to_dict()
# create an instance of ColumnProfileDetailOneOf from a dict
column_profile_detail_one_of_from_dict = ColumnProfileDetailOneOf.from_dict(column_profile_detail_one_of_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


