# ListDatasetVersionsResponse

Response body for GET /v1/datasets/{id}/versions

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | 
**dataset_id** | **str** |  | 
**has_more** | **bool** |  | 
**limit** | **int** |  | 
**offset** | **int** |  | 
**versions** | [**List[DatasetVersionSummary]**](DatasetVersionSummary.md) |  | 

## Example

```python
from hotdata.models.list_dataset_versions_response import ListDatasetVersionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListDatasetVersionsResponse from a JSON string
list_dataset_versions_response_instance = ListDatasetVersionsResponse.from_json(json)
# print the JSON string representation of the object
print(ListDatasetVersionsResponse.to_json())

# convert the object into a dict
list_dataset_versions_response_dict = list_dataset_versions_response_instance.to_dict()
# create an instance of ListDatasetVersionsResponse from a dict
list_dataset_versions_response_from_dict = ListDatasetVersionsResponse.from_dict(list_dataset_versions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


