# QueryResponse

Response body for POST /query  Query results are returned immediately along with a `result_id` for later retrieval. Saving the result for later retrieval happens asynchronously in the background.  To wait until the saved result can be retrieved, poll `GET /query-runs/{id}` with this response's `query_run_id` and read the run's `status`. Send the `X-Database-Id` header for the database the query ran in: that endpoint is scoped by the header alone and returns 400 without it, including when the query itself was scoped with the `database_id` body field instead. - `\"running\"`: still executing, or still being saved - `\"succeeded\"`: finished. A `result_id` on the run names a saved result that   is ready to retrieve, and needs no second check against `GET /results/{id}`   — the result is saved and marked ready before the run is marked succeeded,   never after. A run carrying no `result_id` saved nothing; see below - `\"failed\"`: the query or the save failed — see the run's `error_message` - `\"interrupted\"`: the run was interrupted before it finished, for example   because the server handling it was replaced. Terminal, and safe to retry  Read `result_id` off the query run rather than off this body, and treat `succeeded` and \"there is a result to fetch\" as two questions. A run can succeed having saved nothing: when every row was returned here but the result could not be saved for later retrieval, the run is `succeeded` with no `result_id` at all — the field is omitted from the run, not sent as null, so test for its absence — and the run's `warning_message` says why. This response body's `result_id` is issued while the save is still in flight, so on its own it does not mean the result can be retrieved.  Do not poll `GET /results/{id}` to wait for readiness. That endpoint returns the result *data*: once the result is ready, a JSON response carries all of it, so a status check made against it transfers the entire result to read one field. It also stops working as the result grows, and the two refusals mean opposite things to a caller: a JSON body that cannot fit the per-fetch memory budget at all is refused with 413 and will be refused again, while one that would fit alone but not alongside the JSON fetches already in flight is refused with 429 and can be retried. `GET /query-runs/{id}` returns no rows at any size.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **List[str]** |  | 
**execution_time_ms** | **int** |  | 
**nullable** | **List[bool]** | Nullable flags for each column (parallel to columns vec). True if the column allows NULL values, false if NOT NULL. | 
**preview_row_count** | **int** | Number of rows in *this* response body. Always present. For a large result this is a bounded preview, not the grand total — see &#x60;total_row_count&#x60; and &#x60;truncated&#x60;. | 
**query_run_id** | **str** | Unique identifier for the query run record (qrun...). | 
**result_id** | **str** | Unique identifier for retrieving this result via GET /results/{id}. When non-null, the result is being persisted asynchronously. Null only when the result fit entirely in this response (&#x60;truncated: false&#x60;) but could not be persisted for later retrieval — see the &#x60;warning&#x60; field. A &#x60;truncated: true&#x60; response ALWAYS carries a non-null, resolvable &#x60;result_id&#x60;: a truncated result that cannot be persisted fails the request with a retryable HTTP 503 (&#x60;PERSISTENCE_UNAVAILABLE&#x60;, with a &#x60;Retry-After&#x60; header) rather than returning a partial body with a dead ticket. | [optional] 
**row_count** | **int** | **Deprecated** — use &#x60;preview_row_count&#x60; (rows in this body) and &#x60;total_row_count&#x60; (grand total) instead. Retained as a back-compat alias and always equal to &#x60;preview_row_count&#x60;; for a truncated result it is the preview count, *not* the grand total — read &#x60;total_row_count&#x60; for that. Will be removed in a future release once clients migrate. | 
**rows** | **List[List[object]]** | Array of rows, where each row is an array of column values. Values can be strings, numbers, booleans, or null. | 
**total_row_count** | **int** | Grand total rows in the full result. Present (and equal to &#x60;preview_row_count&#x60;) when the whole result fit in this response; &#x60;null&#x60; while a truncated result is still being persisted. When &#x60;null&#x60;, read the authoritative total from &#x60;GET /v1/query-runs/{id}&#x60; (&#x60;row_count&#x60;) or the &#x60;X-Total-Row-Count&#x60; header on &#x60;GET /v1/results/{id}&#x60;. | [optional] 
**truncated** | **bool** | True when &#x60;rows&#x60; is a bounded preview of a larger result. Fetch the full result via &#x60;result_id&#x60;. | 
**warning** | **str** | Warning message if result persistence could not be initiated. Present only when the full result is returned inline (&#x60;truncated: false&#x60;) but could not be persisted: &#x60;result_id&#x60; is then null and the result cannot be re-fetched later, though every row is in this response. A truncated result never carries a warning — if it cannot be persisted the request fails with a retryable HTTP 503 (&#x60;PERSISTENCE_UNAVAILABLE&#x60;, with a &#x60;Retry-After&#x60; header) instead. | [optional] 

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


