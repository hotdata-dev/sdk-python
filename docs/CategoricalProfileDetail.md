# CategoricalProfileDetail

Type-specific column profile detail. The `type` discriminator field determines which variant is present. Profile type is chosen based on the column's Arrow data type and cardinality:  - **categorical**: Text or numeric columns with ≤200 distinct values. Lists each value with its frequency. - **text**: Text columns with >200 distinct values. Reports string length statistics. - **numeric**: Numeric columns with >200 distinct values. Reports min, max, and mean. - **temporal**: Date and timestamp columns. Reports min and max as ISO-8601 strings. - **boolean**: Boolean columns. Reports true and false counts.   Low-cardinality column (≤200 distinct values). Values sorted by frequency descending.

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


