# AsyncQueryResponse

Returned with 202 when a query runs in the background.  Poll `status_url` with the same `X-Database-Id` header until the run's `status` is `succeeded`, then fetch the result with its `result_id`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query_run_id** | **str** | ID of the query run. | 
**reason** | **str** | Why the query went to the background, when known. | [optional] 
**status** | **str** | Status of the query run. Always &#x60;running&#x60; here. | 
**status_url** | **str** | URL to poll for the run&#39;s status. Send the same &#x60;X-Database-Id&#x60; header. | 

## Example

```python
from hotdata.models.async_query_response import AsyncQueryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AsyncQueryResponse from a JSON string
async_query_response_instance = AsyncQueryResponse.from_json(json)
# print the JSON string representation of the object
print(AsyncQueryResponse.to_json())

# convert the object into a dict
async_query_response_dict = async_query_response_instance.to_dict()
# create an instance of AsyncQueryResponse from a dict
async_query_response_from_dict = AsyncQueryResponse.from_dict(async_query_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


