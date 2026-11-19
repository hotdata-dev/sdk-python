# DatabaseBatchResponse

A bulk-create batch. List its databases with `GET /v1/databases?batch=<batch_id>`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**batch_id** | **str** |  | 
**cancel_requested** | **bool** | True once cancellation is requested. Databases already created are kept. | 
**count** | **int** | Number of databases requested. | 
**created_count** | **int** | Number of databases created so far. | 
**expires_at** | **datetime** |  | [optional] 
**job_id** | **str** | ID of the job creating the databases. Poll it for status. | [optional] 
**status_url** | **str** |  | [optional] 

## Example

```python
from hotdata.models.database_batch_response import DatabaseBatchResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseBatchResponse from a JSON string
database_batch_response_instance = DatabaseBatchResponse.from_json(json)
# print the JSON string representation of the object
print(DatabaseBatchResponse.to_json())

# convert the object into a dict
database_batch_response_dict = database_batch_response_instance.to_dict()
# create an instance of DatabaseBatchResponse from a dict
database_batch_response_from_dict = DatabaseBatchResponse.from_dict(database_batch_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


