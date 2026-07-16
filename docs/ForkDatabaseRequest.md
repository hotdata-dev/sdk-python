# ForkDatabaseRequest

Request body for POST /databases/{database_id}/fork

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expires_at** | **str** | When the fork expires. Accepts either an RFC 3339 timestamp (e.g. &#x60;\&quot;2026-06-01T00:00:00Z\&quot;&#x60;) or a relative duration suffixed with &#x60;h&#x60; (hours), &#x60;m&#x60; (minutes), or &#x60;d&#x60; (days) — for example &#x60;\&quot;24h\&quot;&#x60; or &#x60;\&quot;7d\&quot;&#x60;. When omitted, a still-future expiry on the source is carried over; otherwise the fork never expires. | [optional] 
**name** | **str** | Optional display label for the fork. When omitted, the source database&#39;s name (if any) is carried over. | [optional] 

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


