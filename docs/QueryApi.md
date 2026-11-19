# hotdata.QueryApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**query**](QueryApi.md#query) | **POST** /v1/query | Execute SQL query


# **query**
> QueryResponse query(query_request, x_database_id=x_database_id)

Execute SQL query

Run a SQL query against one database. Choose the database with the `X-Database-Id` header or the `database_id` body field; if you send both, they must match. The query sees the database's `default` catalog and any catalogs attached to it, by their alias. Rows come back inline, with a `result_id` for reading the result again from the Results API.

**Async.** Set `async: true` to get a query run ID back at once and poll for the result. Add `async_after_ms` (1000 to 30000) to wait that long for an inline result first.

**Arrow.** Send `Accept: application/vnd.apache.arrow.stream` (without `application/json`) to get the rows as an Arrow IPC stream. The values the JSON body would carry come as `X-Query-Run-Id`, `X-Result-Id`, `X-Total-Row-Count`, `X-Execution-Time-Ms`, `X-Query-Warning` and `X-Rollup` headers. If the result is too large to send inline, you get a 202 with an `X-Result-Id` header; read the full result from `GET /v1/results/{id}?format=arrow`. Async runs and errors still return JSON.

**Writes.** `INSERT`, `UPDATE`, `DELETE`, `CREATE TABLE`, `CREATE TABLE … AS SELECT` and `DROP TABLE` are supported. A write needs an API key with both the `read` and `write` permissions, can only change the database's `default` catalog, and returns one row with a `rows_affected` column. `INSERT` only appends. `UPDATE` and `DELETE` do not support `RETURNING`, `LIMIT` or `ORDER BY`. `UPDATE` also refuses table aliases, `FROM`, and setting a vector-index column, or a key or `constant_per_key` column. Other changes (`ALTER`, views, `COPY`, transactions) are refused.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.query_request import QueryRequest
from hotdata.models.query_response import QueryResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://api.hotdata.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: WorkspaceId
configuration.api_key['WorkspaceId'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['WorkspaceId'] = 'Bearer'

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.QueryApi(api_client)
    query_request = hotdata.QueryRequest() # QueryRequest | 
    x_database_id = 'x_database_id_example' # str | ID of the database to query. Required unless you set the `database_id` body field. (optional)

    try:
        # Execute SQL query
        api_response = api_instance.query(query_request, x_database_id=x_database_id)
        print("The response of QueryApi->query:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QueryApi->query: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_request** | [**QueryRequest**](QueryRequest.md)|  | 
 **x_database_id** | **str**| ID of the database to query. Required unless you set the &#x60;database_id&#x60; body field. | [optional] 

### Return type

[**QueryResponse**](QueryResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/vnd.apache.arrow.stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The query ran. JSON by default, or an Arrow IPC stream if you asked for one. |  * X-Execution-Time-Ms - Arrow responses only: query execution time in milliseconds. <br>  * X-Query-Run-Id - Arrow responses only: the query run id. <br>  * X-Query-Warning - Arrow responses only: the warning the JSON body would carry, if any. <br>  * X-Result-Id - Arrow responses only: the result ID for the Results API. Absent when the result could not be saved. <br>  * X-Rollup - Arrow responses only: the &#x60;rollup&#x60; value the JSON body would carry, if any. <br>  * X-Total-Row-Count - Arrow responses only: the number of rows in the result. <br>  |
**202** | The query is running in the background. For an Arrow request, this also means the result was too large to send inline. |  * X-Result-Id - Arrow responses only: the result ID for the Results API. Absent when the result could not be saved. <br>  |
**400** | Invalid request, such as no database given, or a header and body &#x60;database_id&#x60; that do not match. |  -  |
**403** | A write statement (&#x60;INSERT&#x60;, &#x60;UPDATE&#x60;, &#x60;DELETE&#x60; and so on) sent with a credential that lacks the &#x60;read&#x60; and &#x60;write&#x60; permissions |  -  |
**404** | Database not found |  -  |
**408** | The query ran past the time limit and was stopped. A query this slow is likely to time out again: narrow it, for example with a filter, or read from a rollup or an index. |  -  |
**429** | Too many queries are running, or not enough memory is free. Retry after the &#x60;Retry-After&#x60; delay. If it continues, add a filter or &#x60;LIMIT&#x60;. |  -  |
**500** | Internal server error |  -  |
**503** | Temporarily unavailable, for example because the result could not be saved or the catalog is busy. Retry after the &#x60;Retry-After&#x60; delay. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

