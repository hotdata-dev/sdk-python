# DatasetSummary

Dataset summary for listing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**id** | **str** |  | 
**label** | **str** |  | 
**latest_version** | **int** |  | 
**pinned_version** | **int** |  | [optional] 
**table_name** | **str** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from hotdata.models.dataset_summary import DatasetSummary

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetSummary from a JSON string
dataset_summary_instance = DatasetSummary.from_json(json)
# print the JSON string representation of the object
print(DatasetSummary.to_json())

# convert the object into a dict
dataset_summary_dict = dataset_summary_instance.to_dict()
# create an instance of DatasetSummary from a dict
dataset_summary_from_dict = DatasetSummary.from_dict(dataset_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


