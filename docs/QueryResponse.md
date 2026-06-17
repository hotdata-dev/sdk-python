# QueryResponse

Response body for POST /query  Query results are returned immediately along with a `result_id` for later retrieval. The actual persistence to storage happens asynchronously in the background.  To check if a result is ready for SQL queries, poll GET /results/{id} and check `status`: - `\"processing\"`: Persistence is still in progress - `\"ready\"`: Result is available for retrieval and SQL queries - `\"failed\"`: Persistence failed (check `error_message` for details)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **List[str]** |  | 
**execution_time_ms** | **int** |  | 
**nullable** | **List[bool]** | Nullable flags for each column (parallel to columns vec). True if the column allows NULL values, false if NOT NULL. | 
**preview_row_count** | **int** | Number of rows in *this* response body. Always present. For a large result this is a bounded preview, not the grand total — see &#x60;total_row_count&#x60; and &#x60;truncated&#x60;. | 
**query_run_id** | **str** | Unique identifier for the query run record (qrun...). | 
**result_id** | **str** | Unique identifier for retrieving this result via GET /results/{id}. When non-null, the result is being persisted asynchronously. Null only when the result fit entirely in this response (&#x60;truncated: false&#x60;) but could not be persisted for later retrieval — see the &#x60;warning&#x60; field. A &#x60;truncated: true&#x60; response ALWAYS carries a non-null, resolvable &#x60;result_id&#x60; (#640 F1): a truncated result that cannot be persisted fails the request with a retryable HTTP 503 (&#x60;PERSISTENCE_UNAVAILABLE&#x60;, with a &#x60;Retry-After&#x60; header) rather than returning a partial body with a dead ticket. | [optional] 
**row_count** | **int** | **Deprecated** — use &#x60;preview_row_count&#x60; (rows in this body) and &#x60;total_row_count&#x60; (grand total) instead. Retained as a back-compat alias and always equal to &#x60;preview_row_count&#x60;; for a truncated result it is the preview count, *not* the grand total — read &#x60;total_row_count&#x60; for that. Will be removed in a future release once clients migrate. | 
**rows** | **List[List[object]]** | Array of rows, where each row is an array of column values. Values can be strings, numbers, booleans, or null. | 
**total_row_count** | **int** | Grand total rows in the full result. Present (and equal to &#x60;preview_row_count&#x60;) when the whole result fit in this response; &#x60;null&#x60; while a truncated result is still being persisted. When &#x60;null&#x60;, read the authoritative total from &#x60;GET /v1/query-runs/{id}&#x60; (&#x60;row_count&#x60;) or the &#x60;X-Total-Row-Count&#x60; header on &#x60;GET /v1/results/{id}&#x60;. | [optional] 
**truncated** | **bool** | True when &#x60;rows&#x60; is a bounded preview of a larger result. Fetch the full result via &#x60;result_id&#x60;. | 
**warning** | **str** | Warning message if result persistence could not be initiated. Present only when the full result is returned inline (&#x60;truncated: false&#x60;) but could not be persisted: &#x60;result_id&#x60; is then null and the result cannot be re-fetched later, though every row is in this response. A truncated result never carries a warning — if it cannot be persisted the request fails with a retryable HTTP 503 (&#x60;PERSISTENCE_UNAVAILABLE&#x60;, with a &#x60;Retry-After&#x60; header) instead (#640 F1). | [optional] 

## Example

```python
from hotdata.models.query_response import QueryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of QueryResponse from a JSON string
query_response_instance = QueryResponse.from_json(json)
# print the JSON string representation of the object
print(QueryResponse.to_json())

# convert the object into a dict
query_response_dict = query_response_instance.to_dict()
# create an instance of QueryResponse from a dict
query_response_from_dict = QueryResponse.from_dict(query_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


