# SavedQueryDatasetSource

Create dataset from a saved query result

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**saved_query_id** | **str** |  | 
**version** | **int** |  | [optional] 

## Example

```python
from hotdata.models.saved_query_dataset_source import SavedQueryDatasetSource

# TODO update the JSON string below
json = "{}"
# create an instance of SavedQueryDatasetSource from a JSON string
saved_query_dataset_source_instance = SavedQueryDatasetSource.from_json(json)
# print the JSON string representation of the object
print(SavedQueryDatasetSource.to_json())

# convert the object into a dict
saved_query_dataset_source_dict = saved_query_dataset_source_instance.to_dict()
# create an instance of SavedQueryDatasetSource from a dict
saved_query_dataset_source_from_dict = SavedQueryDatasetSource.from_dict(saved_query_dataset_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


