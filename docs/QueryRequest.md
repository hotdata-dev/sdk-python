# QueryRequest

Request body for POST /query

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_async** | **bool** | When true, execute the query asynchronously and return a query run ID for polling via GET /query-runs/{id}. The query results can be retrieved via GET /results/{id} once the query run status is \&quot;succeeded\&quot;. | [optional] [default to False]
**async_after_ms** | **int** | If set (requires &#x60;async&#x60; &#x3D; true), first attempt the query synchronously and wait up to this many milliseconds: if it finishes in time the full result is returned, otherwise an async response (a run id to poll) is returned. Must be at least 1000 and at most the server&#39;s configured maximum; a value out of that range, or set without &#x60;async&#x60; &#x3D; true, is rejected with 400. | [optional] 
**database_id** | **str** | Database to scope the query to (its id). Alternative to the &#x60;X-Database-Id&#x60; header — exactly one source must be provided. If both this field and the header are set and they disagree, the request is rejected with a 400. | [optional] 
**default_catalog** | **str** | Catalog that unqualified table references resolve against within the query&#39;s database scope. Must name a catalog visible in the database (&#x60;default&#x60;, an attached catalog alias, or a system catalog). Defaults to &#x60;default&#x60; when omitted. | [optional] 
**default_schema** | **str** | Schema that unqualified table references resolve against within the query&#39;s database scope. Defaults to &#x60;main&#x60; when omitted. Existence is not validated up front — an unknown schema surfaces as a \&quot;table not found\&quot; error at planning time. | [optional] 
**dialect** | **str** | SQL dialect the &#x60;sql&#x60; field is written in. One of &#x60;hotsql&#x60; (the default), &#x60;duckdb&#x60;, &#x60;postgres&#x60;, or &#x60;snowflake&#x60;. When set to anything other than &#x60;hotsql&#x60;, the query is translated to HotSQL before it runs, so you can use idioms from that dialect (for example Snowflake &#x60;IFF(...)&#x60; or Postgres &#x60;MOD(a, b)&#x60;). Only read-only queries are accepted. An unrecognized value is rejected with a 400. | [optional] 
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


