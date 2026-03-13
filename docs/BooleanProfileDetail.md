# BooleanProfileDetail

Boolean column.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**false_count** | **int** | Number of false values | 
**true_count** | **int** | Number of true values | 

## Example

```python
from hotdata.models.boolean_profile_detail import BooleanProfileDetail

# TODO update the JSON string below
json = "{}"
# create an instance of BooleanProfileDetail from a JSON string
boolean_profile_detail_instance = BooleanProfileDetail.from_json(json)
# print the JSON string representation of the object
print(BooleanProfileDetail.to_json())

# convert the object into a dict
boolean_profile_detail_dict = boolean_profile_detail_instance.to_dict()
# create an instance of BooleanProfileDetail from a dict
boolean_profile_detail_from_dict = BooleanProfileDetail.from_dict(boolean_profile_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


