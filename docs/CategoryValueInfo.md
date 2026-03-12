# CategoryValueInfo

A distinct value with its frequency count, used in categorical profiles.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of occurrences | 
**value** | **object** | The distinct value (as a string, or null) | 

## Example

```python
from hotdata.models.category_value_info import CategoryValueInfo

# TODO update the JSON string below
json = "{}"
# create an instance of CategoryValueInfo from a JSON string
category_value_info_instance = CategoryValueInfo.from_json(json)
# print the JSON string representation of the object
print(CategoryValueInfo.to_json())

# convert the object into a dict
category_value_info_dict = category_value_info_instance.to_dict()
# create an instance of CategoryValueInfo from a dict
category_value_info_from_dict = CategoryValueInfo.from_dict(category_value_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


