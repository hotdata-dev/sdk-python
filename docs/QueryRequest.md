# QueryRequest

Request body for POST /query

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_async** | **bool** | Run the query in the background and return a query run ID right away. Poll &#x60;GET /v1/query-runs/{id}&#x60; for its status. | [optional] [default to False]
**async_after_ms** | **int** | With &#x60;async: true&#x60;, wait up to this many milliseconds for the result before falling back to a query run ID. Must be between 1000 and 30000. | [optional] 
**database_id** | **str** | ID of the database to query. Use this or the &#x60;X-Database-Id&#x60; header; if both are set they must match, or the request fails with 400. | [optional] 
**default_catalog** | **str** | Catalog that unqualified table names resolve to. Defaults to the database&#39;s default catalog; an unknown catalog fails with 400. | [optional] 
**default_schema** | **str** | Schema that unqualified table names resolve to. Defaults to the database&#39;s &#x60;default_schema&#x60;; a schema that does not exist makes unqualified tables fail with \&quot;table not found\&quot;. | [optional] 
**dialect** | **str** | SQL dialect of &#x60;sql&#x60;: &#x60;hotsql&#x60; (default), &#x60;duckdb&#x60;, &#x60;postgres&#x60;, &#x60;snowflake&#x60; or &#x60;clickhouse&#x60;. Other dialects are translated to HotSQL before the query runs. | [optional] 
**params** | **object** | Values for the parameters &#x60;sql&#x60; names as &#x60;$name&#x60;, by name. A value is bound as a value, never as SQL text, so it cannot change what the statement does. Works in reads and in &#x60;INSERT&#x60;, &#x60;UPDATE&#x60; and &#x60;DELETE&#x60;. Every &#x60;$name&#x60; in the SQL needs a value and every value must be used, or the request fails with 400.  Each value takes the type the SQL gives its parameter: &#x60;ts &gt;&#x3D; $start&#x60; reads &#x60;start&#x60; as a timestamp string, &#x60;id &#x3D; $id&#x60; as the type of &#x60;id&#x60;, and a value that does not fit that type is refused. Where the SQL gives the parameter no type (&#x60;SELECT $x&#x60;), a string, number or boolean keeps its own type; write &#x60;CAST($x AS ...)&#x60; to choose another, and a null needs a typed position. Parameters are not available in other dialects, and cannot be arguments of &#x60;vector_search&#x60;, &#x60;bm25_search&#x60; or the vector distance functions. | [optional] 
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


