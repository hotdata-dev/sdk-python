# CategoricalProfileDetail

Text or numeric column with 200 or fewer distinct values.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**values** | [**List[CategoryValueInfo]**](CategoryValueInfo.md) | Distinct values with their counts, ordered by count descending | 

## Example

```python
from hotdata.models.categorical_profile_detail import CategoricalProfileDetail

# TODO update the JSON string below
json = "{}"
# create an instance of CategoricalProfileDetail from a JSON string
categorical_profile_detail_instance = CategoricalProfileDetail.from_json(json)
# print the JSON string representation of the object
print(CategoricalProfileDetail.to_json())

# convert the object into a dict
categorical_profile_detail_dict = categorical_profile_detail_instance.to_dict()
# create an instance of CategoricalProfileDetail from a dict
categorical_profile_detail_from_dict = CategoricalProfileDetail.from_dict(categorical_profile_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


