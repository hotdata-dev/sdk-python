# QueryRequest

Request body for POST /query

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_async** | **bool** | When true, execute the query asynchronously and return a query run ID for polling via GET /query-runs/{id}. The query results can be retrieved via GET /results/{id} once the query run status is \&quot;succeeded\&quot;. | [optional] 
**async_after_ms** | **int** | If set with async&#x3D;true, wait up to this many milliseconds for the query to complete synchronously before returning an async response. Minimum 1000ms. Ignored if async is false. | [optional] 
**database_id** | **str** | Database to scope the query to (its id). Alternative to the &#x60;X-Database-Id&#x60; header — exactly one source must be provided. If both this field and the header are set and they disagree, the request is rejected with a 400. | [optional] 
**default_catalog** | **str** | Catalog that unqualified table references resolve against within the query&#39;s database scope. Must name a catalog visible in the database (&#x60;default&#x60;, an attached catalog alias, or a system catalog). Defaults to &#x60;default&#x60; when omitted. | [optional] 
**default_schema** | **str** | Schema that unqualified table references resolve against within the query&#39;s database scope. Defaults to &#x60;main&#x60; when omitted. Existence is not validated up front — an unknown schema surfaces as a \&quot;table not found\&quot; error at planning time. | [optional] 
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


