# InlineDatasetSource

Create dataset from inline data (small payloads)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inline** | [**InlineData**](InlineData.md) |  | 

## Example

```python
from hotdata.models.inline_dataset_source import InlineDatasetSource

# TODO update the JSON string below
json = "{}"
# create an instance of InlineDatasetSource from a JSON string
inline_dataset_source_instance = InlineDatasetSource.from_json(json)
# print the JSON string representation of the object
print(InlineDatasetSource.to_json())

# convert the object into a dict
inline_dataset_source_dict = inline_dataset_source_instance.to_dict()
# create an instance of InlineDatasetSource from a dict
inline_dataset_source_from_dict = InlineDatasetSource.from_dict(inline_dataset_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


