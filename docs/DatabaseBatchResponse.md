# DatabaseBatchResponse

A bulk-creation batch: the handle for progress, listing, and cancellation.  The databases themselves are listed with `GET /databases?batch=<batch_id>`; this carries the batch's own state rather than its members.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**batch_id** | **str** |  | 
**cancel_requested** | **bool** | True once stopping has been requested. Databases already created are kept; only further creation stops. | 
**count** | **int** | How many databases the batch was asked to create. | 
**created_count** | **int** | How many exist so far. Advances as the batch fills. | 
**expires_at** | **datetime** |  | [optional] 
**job_id** | **str** | Job filling this batch. Poll it for status. | [optional] 
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


