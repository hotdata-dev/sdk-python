# hotdata.ResultsApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_result**](ResultsApi.md#get_result) | **GET** /v1/results/{id} | Get result
[**list_results**](ResultsApi.md#list_results) | **GET** /v1/results | List results


# **get_result**
> GetResultResponse get_result(id, offset=offset, limit=limit, format=format)

Get result

Retrieve a persisted query result by ID. The response format for the `ready` state is selected by `Accept` header or `?format=` query param; non-ready states use the same status codes and JSON body shape regardless of format.

| Result status         | Status × body                                                                |
|-----------------------|------------------------------------------------------------------------------|
| `ready` + JSON        | 200 `application/json` — `GetResultResponse` with `columns`, `rows`, etc.    |
| `ready` + Arrow       | 200 `application/vnd.apache.arrow.stream` — schema, RecordBatches, EOS       |
| `pending`/`processing`| 202 `application/json` `{status, result_id}` + `Retry-After`                 |
| `failed`              | 409 `application/json` `{status, result_id, error_message}`                  |
| not found             | 404 `application/json` (`ApiErrorResponse`)                                  |

`?format=arrow` (or `?format=json`) takes precedence over `Accept`. Use `?offset=N&limit=M` to slice the result; `offset` defaults to 0 and `limit` is unbounded by default. Both must be non-negative; invalid values return 400. When a finite `limit` doesn't reach the end of the result, a `Link` header with `rel="next"` points at the following page.

Ready responses (both formats) carry `X-Total-Row-Count` (full result row count from parquet metadata, independent of offset/limit). The Arrow path streams end-to-end with no spawned task between the parquet reader and the wire — clients can disconnect at any time and the server stops reading.

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
    offset = 56 # int | Rows to skip (default: 0) (optional)
    limit = 56 # int | Maximum rows to return (default: unbounded) (optional)
    format = hotdata.ResultsFormatQuery() # ResultsFormatQuery | `arrow` or `json` — overrides the `Accept` header. (optional)

    try:
        # Get result
        api_response = api_instance.get_result(id, offset=offset, limit=limit, format=format)
        print("The response of ResultsApi->get_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->get_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Result ID | 
 **offset** | **int**| Rows to skip (default: 0) | [optional] 
 **limit** | **int**| Maximum rows to return (default: unbounded) | [optional] 
 **format** | [**ResultsFormatQuery**](.md)| &#x60;arrow&#x60; or &#x60;json&#x60; — overrides the &#x60;Accept&#x60; header. | [optional] 

### Return type

[**GetResultResponse**](GetResultResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [SessionId](../README.md#SessionId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.apache.arrow.stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Result data. JSON callers receive &#x60;GetResultResponse&#x60;. Arrow callers receive an Arrow IPC stream — a sequence of IPC messages: schema header, then RecordBatch messages, then EOS. |  * Link - RFC 5988 &#x60;Link&#x60; header with &#x60;rel&#x3D;\&quot;next\&quot;&#x60; pointing at the next page when a finite &#x60;limit&#x60; does not reach the end of the result. <br>  * X-Total-Row-Count - Total rows in the full result, ignoring offset/limit. Present only when status is &#x60;ready&#x60;. <br>  |
**202** | Result is still being computed (&#x60;pending&#x60; or &#x60;processing&#x60;). Poll the same URL. |  * Retry-After - Suggested seconds before the next poll. <br>  |
**400** | Invalid offset, limit, or format. |  -  |
**404** | Result not found. |  -  |
**409** | Result computation failed. Body carries &#x60;error_message&#x60; describing the failure. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_results**
> ListResultsResponse list_results(limit=limit, offset=offset)

List results

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
    limit = 56 # int | Maximum number of results (default: 100, max: 1000) (optional)
    offset = 56 # int | Pagination offset (default: 0) (optional)

    try:
        # List results
        api_response = api_instance.list_results(limit=limit, offset=offset)
        print("The response of ResultsApi->list_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->list_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

