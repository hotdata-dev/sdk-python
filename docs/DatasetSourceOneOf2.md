# DatasetSourceOneOf2


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Optional description for the auto-created saved query. | [optional] 
**name** | **str** | Optional name for the auto-created saved query. Defaults to the dataset label. | [optional] 
**sql** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from hotdata.models.dataset_source_one_of2 import DatasetSourceOneOf2

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetSourceOneOf2 from a JSON string
dataset_source_one_of2_instance = DatasetSourceOneOf2.from_json(json)
# print the JSON string representation of the object
print(DatasetSourceOneOf2.to_json())

# convert the object into a dict
dataset_source_one_of2_dict = dataset_source_one_of2_instance.to_dict()
# create an instance of DatasetSourceOneOf2 from a dict
dataset_source_one_of2_from_dict = DatasetSourceOneOf2.from_dict(dataset_source_one_of2_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


