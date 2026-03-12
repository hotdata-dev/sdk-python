# InlineData

Inline data specification

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **Dict[str, str]** | Optional explicit column definitions. Keys are column names, values are type specs. When provided, the schema is built from these definitions instead of being inferred. | [optional] 
**content** | **str** |  | 
**format** | **str** |  | 

## Example

```python
from hotdata.models.inline_data import InlineData

# TODO update the JSON string below
json = "{}"
# create an instance of InlineData from a JSON string
inline_data_instance = InlineData.from_json(json)
# print the JSON string representation of the object
print(InlineData.to_json())

# convert the object into a dict
inline_data_dict = inline_data_instance.to_dict()
# create an instance of InlineData from a dict
inline_data_from_dict = InlineData.from_dict(inline_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


