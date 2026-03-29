# QueryRequest

Request body for POST /query

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_async** | **bool** | When true, execute the query asynchronously and return a query run ID for polling via GET /query-runs/{id}. The query results can be retrieved via GET /results/{id} once the query run status is \&quot;succeeded\&quot;. | [optional] 
**async_after_ms** | **int** | If set with async&#x3D;true, wait up to this many milliseconds for the query to complete synchronously before returning an async response. Minimum 1000ms. Ignored if async is false. | [optional] 
**sql** | **str** |  | 

## Example

```python
from hotdata.models.query_request import QueryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of QueryRequest from a JSON string
query_request_instance = QueryRequest.from_json(json)
# print the JSON string representation of the object
print(QueryRequest.to_json())

# convert the object into a dict
query_request_dict = query_request_instance.to_dict()
# create an instance of QueryRequest from a dict
query_request_from_dict = QueryRequest.from_dict(query_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


