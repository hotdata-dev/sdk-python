# NumericProfileDetail

High-cardinality numeric column (>200 distinct values).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max** | **str** | Maximum value (string to preserve precision for large integers and decimals) | 
**mean** | **float** | Arithmetic mean | 
**min** | **str** | Minimum value (string to preserve precision for large integers and decimals) | 

## Example

```python
from hotdata.models.numeric_profile_detail import NumericProfileDetail

# TODO update the JSON string below
json = "{}"
# create an instance of NumericProfileDetail from a JSON string
numeric_profile_detail_instance = NumericProfileDetail.from_json(json)
# print the JSON string representation of the object
print(NumericProfileDetail.to_json())

# convert the object into a dict
numeric_profile_detail_dict = numeric_profile_detail_instance.to_dict()
# create an instance of NumericProfileDetail from a dict
numeric_profile_detail_from_dict = NumericProfileDetail.from_dict(numeric_profile_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


