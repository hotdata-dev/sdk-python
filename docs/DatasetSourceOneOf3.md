# DatasetSourceOneOf3


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **Dict[str, str]** | Optional explicit column definitions. Keys are column names, values are type specs. | [optional] 
**format** | **str** |  | [optional] 
**url** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from hotdata.models.dataset_source_one_of3 import DatasetSourceOneOf3

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetSourceOneOf3 from a JSON string
dataset_source_one_of3_instance = DatasetSourceOneOf3.from_json(json)
# print the JSON string representation of the object
print(DatasetSourceOneOf3.to_json())

# convert the object into a dict
dataset_source_one_of3_dict = dataset_source_one_of3_instance.to_dict()
# create an instance of DatasetSourceOneOf3 from a dict
dataset_source_one_of3_from_dict = DatasetSourceOneOf3.from_dict(dataset_source_one_of3_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


