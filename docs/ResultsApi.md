# hotdata.ResultsApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_result**](ResultsApi.md#get_result) | **GET** /v1/results/{id} | Get result
[**list_results**](ResultsApi.md#list_results) | **GET** /v1/results | List results


# **get_result**
> GetResultResponse get_result(id, x_database_id, offset=offset, limit=limit, format=format)

Get result

Retrieve a persisted query result by ID. The response format for the `ready` state is selected by `Accept` header or `?format=` query param; non-ready states use the same status codes and JSON body shape regardless of format.

| Result status         | Status × body                                                                |
|-----------------------|------------------------------------------------------------------------------|
| `ready` + JSON        | 200 `application/json` — `GetResultResponse` with `columns`, `rows`, etc.    |
| `ready` + Arrow       | 200 `application/vnd.apache.arrow.stream` — schema, RecordBatches, EOS       |
| `ready` + CSV         | 200 `text/csv; charset=utf-8` — single header row, streamed batch-by-batch   |
| `ready` + Markdown    | 200 `text/markdown; charset=utf-8` — GitHub-flavored pipe table, streamed   |
| `ready` + Parquet     | 200 `application/vnd.apache.parquet` — raw parquet bytes (no conversion)     |
| `pending`/`processing`| 202 `application/json` `{status, result_id}` + `Retry-After`                 |
| `failed`              | 409 `application/json` `{status, result_id, error_message}`                  |
| not found             | 404 `application/json` (`ApiErrorResponse`)                                  |

`?format=` accepts `arrow`, `json`, `csv`, `md`, `parquet` and takes precedence over `Accept`. `markdown` is accepted as a runtime alias for `md`. Use `?offset=N&limit=M` to slice the result; `offset` defaults to 0 and `limit` is unbounded by default. Both must be non-negative; invalid values return 400. When a finite `limit` doesn't reach the end of the result, a `Link` header with `rel="next"` points at the following page. `?offset`/`?limit` are ignored for `format=parquet` since that path returns the underlying file unchanged.

Ready responses (Arrow, CSV, Markdown, JSON) carry `X-Total-Row-Count` (the full result row count, independent of offset/limit). Responses are streamed end-to-end, so a client can disconnect at any time and the server stops reading.

IEEE special floats (`±Inf`, `NaN`) have no canonical JSON representation. For cross-format consistency the JSON, CSV, and Markdown paths emit them as `null` / empty cells, and JSON `nullable[]` is widened to match. The Arrow IPC and Parquet bodies are binary round-trip formats and preserve the raw IEEE values; callers cross-checking a result across CSV and Parquet should not byte-compare those slots.

### Example

* Api Key Authentication (WorkspaceId):
* Api Key Authentication (SessionId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.get_result_response import GetResultResponse
from hotdata.models.results_format_query import ResultsFormatQuery
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

# Configure API key authorization: SessionId
configuration.api_key['SessionId'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['SessionId'] = 'Bearer'

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.ResultsApi(api_client)
    id = 'id_example' # str | Result ID
    x_database_id = 'x_database_id_example' # str | Database the result belongs to (required)
    offset = 56 # int | Rows to skip (default: 0) (optional)
    limit = 56 # int | Maximum rows to return (default: unbounded) (optional)
    format = hotdata.ResultsFormatQuery() # ResultsFormatQuery | `arrow`, `json`, `csv`, `md`, or `parquet` — overrides the `Accept` header. `markdown` is also accepted at runtime as an alias for `md`. (optional)

    try:
        # Get result
        api_response = api_instance.get_result(id, x_database_id, offset=offset, limit=limit, format=format)
        print("The response of ResultsApi->get_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->get_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Result ID | 
 **x_database_id** | **str**| Database the result belongs to (required) | 
 **offset** | **int**| Rows to skip (default: 0) | [optional] 
 **limit** | **int**| Maximum rows to return (default: unbounded) | [optional] 
 **format** | [**ResultsFormatQuery**](.md)| &#x60;arrow&#x60;, &#x60;json&#x60;, &#x60;csv&#x60;, &#x60;md&#x60;, or &#x60;parquet&#x60; — overrides the &#x60;Accept&#x60; header. &#x60;markdown&#x60; is also accepted at runtime as an alias for &#x60;md&#x60;. | [optional] 

### Return type

[**GetResultResponse**](GetResultResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [SessionId](../README.md#SessionId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.apache.arrow.stream, text/csv, text/markdown, application/vnd.apache.parquet

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Result data. The body depends on the negotiated format: JSON callers receive &#x60;GetResultResponse&#x60;; Arrow callers receive an Arrow IPC stream; CSV callers receive comma-separated text (LF-terminated, double-quote escaped, RFC 4180-style quoting but not RFC 4180-strict on line endings); Markdown callers receive a single GitHub-flavored pipe table; Parquet callers receive the raw parquet bytes, served as-is. Non-finite floats (&#x60;±Inf&#x60;, &#x60;NaN&#x60;) render as &#x60;null&#x60; (JSON) or empty cells (CSV, Markdown) for cross-format consistency. &#x60;Accept&#x60; is treated as a flat content-type list — &#x60;q&#x3D;&#x60; quality values are ignored; use &#x60;?format&#x3D;&#x60; to disambiguate. |  * Link - RFC 5988 &#x60;Link&#x60; header with &#x60;rel&#x3D;\&quot;next\&quot;&#x60; pointing at the next page when a finite &#x60;limit&#x60; does not reach the end of the result. <br>  * X-Total-Row-Count - Total rows in the full result, ignoring offset/limit. Present only when status is &#x60;ready&#x60;. <br>  |
**202** | Result is still being computed (&#x60;pending&#x60; or &#x60;processing&#x60;). Poll the same URL. |  * Retry-After - Suggested seconds before the next poll. <br>  |
**400** | Invalid offset, limit, or format. |  -  |
**404** | Result not found. |  -  |
**409** | Result computation failed. Body carries &#x60;error_message&#x60; describing the failure. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_results**
> ListResultsResponse list_results(x_database_id, limit=limit, offset=offset)

List results

List stored results for the database named by the required X-Database-Id header.

### Example

* Api Key Authentication (WorkspaceId):
* Api Key Authentication (SessionId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_results_response import ListResultsResponse
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

# Configure API key authorization: SessionId
configuration.api_key['SessionId'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['SessionId'] = 'Bearer'

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.ResultsApi(api_client)
    x_database_id = 'x_database_id_example' # str | Database to scope the results to (required)
    limit = 56 # int | Maximum number of results (default: 100, max: 1000) (optional)
    offset = 56 # int | Pagination offset (default: 0) (optional)

    try:
        # List results
        api_response = api_instance.list_results(x_database_id, limit=limit, offset=offset)
        print("The response of ResultsApi->list_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->list_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_database_id** | **str**| Database to scope the results to (required) | 
 **limit** | **int**| Maximum number of results (default: 100, max: 1000) | [optional] 
 **offset** | **int**| Pagination offset (default: 0) | [optional] 

### Return type

[**ListResultsResponse**](ListResultsResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [SessionId](../README.md#SessionId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of results |  -  |
**400** | Missing or malformed X-Database-Id header |  -  |
**404** | Database not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

