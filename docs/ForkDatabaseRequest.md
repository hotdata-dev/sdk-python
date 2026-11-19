# ForkDatabaseRequest

Request body for POST /databases/{database_id}/fork

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Why the fork was taken, shown in the fork&#39;s lineage. Up to 4096 bytes. | [optional] 
**expires_at** | **str** | When the fork expires: a future RFC 3339 timestamp, or a duration such as &#x60;24h&#x60; or &#x60;7d&#x60;. Defaults to the source&#39;s expiry, if it has one. | [optional] 
**name** | **str** | Display name for the fork. Defaults to the source&#39;s name plus a short suffix. | [optional] 

## Example

```python
from hotdata.models.fork_database_request import ForkDatabaseRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ForkDatabaseRequest from a JSON string
fork_database_request_instance = ForkDatabaseRequest.from_json(json)
# print the JSON string representation of the object
print(ForkDatabaseRequest.to_json())

# convert the object into a dict
fork_database_request_dict = fork_database_request_instance.to_dict()
# create an instance of ForkDatabaseRequest from a dict
fork_database_request_from_dict = ForkDatabaseRequest.from_dict(fork_database_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


