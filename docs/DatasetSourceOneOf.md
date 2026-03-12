# DatasetSourceOneOf

Create from a previously uploaded file

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**Dict[str, ColumnDefinition]**](ColumnDefinition.md) | Optional explicit column definitions. Keys are column names, values are type specs. When provided, the schema is built from these definitions instead of being inferred. | [optional] 
**format** | **str** |  | [optional] 
**upload_id** | **str** |  | 

## Example

```python
from hotdata.models.dataset_source_one_of import DatasetSourceOneOf

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetSourceOneOf from a JSON string
dataset_source_one_of_instance = DatasetSourceOneOf.from_json(json)
# print the JSON string representation of the object
print(DatasetSourceOneOf.to_json())

# convert the object into a dict
dataset_source_one_of_dict = dataset_source_one_of_instance.to_dict()
# create an instance of DatasetSourceOneOf from a dict
dataset_source_one_of_from_dict = DatasetSourceOneOf.from_dict(dataset_source_one_of_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


