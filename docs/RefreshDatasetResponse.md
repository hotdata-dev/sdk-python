# RefreshDatasetResponse

Response body for POST /v1/datasets/{id}/refresh

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**id** | **str** |  | 
**status** | **str** |  | 
**version** | **int** |  | 

## Example

```python
from hotdata.models.refresh_dataset_response import RefreshDatasetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RefreshDatasetResponse from a JSON string
refresh_dataset_response_instance = RefreshDatasetResponse.from_json(json)
# print the JSON string representation of the object
print(RefreshDatasetResponse.to_json())

# convert the object into a dict
refresh_dataset_response_dict = refresh_dataset_response_instance.to_dict()
# create an instance of RefreshDatasetResponse from a dict
refresh_dataset_response_from_dict = RefreshDatasetResponse.from_dict(refresh_dataset_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


