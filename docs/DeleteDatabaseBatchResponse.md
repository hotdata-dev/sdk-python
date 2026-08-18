# DeleteDatabaseBatchResponse

Response body for DELETE /databases/bulk/{batch_id}.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**batch_id** | **str** |  | 
**deleted_count** | **int** | How many databases were removed. | 

## Example

```python
from hotdata.models.delete_database_batch_response import DeleteDatabaseBatchResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteDatabaseBatchResponse from a JSON string
delete_database_batch_response_instance = DeleteDatabaseBatchResponse.from_json(json)
# print the JSON string representation of the object
print(DeleteDatabaseBatchResponse.to_json())

# convert the object into a dict
delete_database_batch_response_dict = delete_database_batch_response_instance.to_dict()
# create an instance of DeleteDatabaseBatchResponse from a dict
delete_database_batch_response_from_dict = DeleteDatabaseBatchResponse.from_dict(delete_database_batch_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


