# DatasetVersionSummary

Dataset version summary

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**id** | **str** |  | 
**source_type** | **str** |  | 
**version** | **int** |  | 

## Example

```python
from hotdata.models.dataset_version_summary import DatasetVersionSummary

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetVersionSummary from a JSON string
dataset_version_summary_instance = DatasetVersionSummary.from_json(json)
# print the JSON string representation of the object
print(DatasetVersionSummary.to_json())

# convert the object into a dict
dataset_version_summary_dict = dataset_version_summary_instance.to_dict()
# create an instance of DatasetVersionSummary from a dict
dataset_version_summary_from_dict = DatasetVersionSummary.from_dict(dataset_version_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


