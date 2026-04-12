# AsyncQueryResponse

Response returned when a query is submitted asynchronously (202 Accepted).  Poll GET /query-runs/{id} to track progress. Once status is \"succeeded\", retrieve results via GET /results/{result_id}.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query_run_id** | **str** | Unique identifier for the query run. | 
**reason** | **str** | Human-readable reason why the query went async (e.g., caching tables for the first time). | [optional] 
**status** | **str** | Current status of the query run. | 
**status_url** | **str** | URL to poll for query run status. | 

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


