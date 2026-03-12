# QueryResponse

Response body for POST /query  Query results are returned immediately along with a `result_id` for later retrieval. The actual persistence to storage happens asynchronously in the background.  To check if a result is ready for SQL queries, poll GET /results/{id} and check `status`: - `\"processing\"`: Persistence is still in progress - `\"ready\"`: Result is available for retrieval and SQL queries - `\"failed\"`: Persistence failed (check `error_message` for details)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **List[str]** |  | 
**execution_time_ms** | **int** |  | 
**nullable** | **List[bool]** | Nullable flags for each column (parallel to columns vec). True if the column allows NULL values, false if NOT NULL. | 
**query_run_id** | **str** | Unique identifier for the query run record (qrun...). | 
**result_id** | **object** | Unique identifier for retrieving this result via GET /results/{id}. Null if catalog registration failed (see &#x60;warning&#x60; field for details). When non-null, the result is being persisted asynchronously. | [optional] 
**row_count** | **int** |  | 
**rows** | **List[List[object]]** |  | 
**warning** | **object** | Warning message if result persistence could not be initiated. When present, &#x60;result_id&#x60; will be null and the result cannot be retrieved later. The query results are still returned in this response. | [optional] 

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


