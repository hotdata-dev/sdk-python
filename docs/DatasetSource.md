# DatasetSource

Dataset source specification.  Internally tagged on `type`, e.g. `{\"type\": \"upload\", \"upload_id\": \"...\"}`. Discriminator values: `upload`, `saved_query`, `sql_query`, `url`, `inline`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **Dict[str, str]** | Optional explicit column definitions. Keys are column names, values are type specs. | [optional] 
**format** | **str** |  | [optional] 
**upload_id** | **str** |  | 
**type** | **str** |  | 
**saved_query_id** | **str** |  | 
**version** | **int** |  | [optional] 
**description** | **str** | Optional description for the auto-created saved query. | [optional] 
**name** | **str** | Optional name for the auto-created saved query. Defaults to the dataset label. | [optional] 
**sql** | **str** |  | 
**url** | **str** |  | 
**inline** | [**InlineData**](InlineData.md) |  | 

## Example

```python
from hotdata.models.dataset_source import DatasetSource

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetSource from a JSON string
dataset_source_instance = DatasetSource.from_json(json)
# print the JSON string representation of the object
print(DatasetSource.to_json())

# convert the object into a dict
dataset_source_dict = dataset_source_instance.to_dict()
# create an instance of DatasetSource from a dict
dataset_source_from_dict = DatasetSource.from_dict(dataset_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


