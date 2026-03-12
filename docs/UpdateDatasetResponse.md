# UpdateDatasetResponse

Response body for PUT /v1/datasets/{id}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**label** | **str** |  | 
**table_name** | **str** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from hotdata.models.update_dataset_response import UpdateDatasetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateDatasetResponse from a JSON string
update_dataset_response_instance = UpdateDatasetResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateDatasetResponse.to_json())

# convert the object into a dict
update_dataset_response_dict = update_dataset_response_instance.to_dict()
# create an instance of UpdateDatasetResponse from a dict
update_dataset_response_from_dict = UpdateDatasetResponse.from_dict(update_dataset_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


