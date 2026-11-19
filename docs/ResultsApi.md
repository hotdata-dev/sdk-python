# hotdata.ResultsApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_result**](ResultsApi.md#get_result) | **GET** /v1/results/{id} | Get result
[**list_results**](ResultsApi.md#list_results) | **GET** /v1/results | List results


# **get_result**
> GetResultResponse get_result(id, x_database_id, offset=offset, limit=limit, format=format)

Get result

Get a saved query result by ID. Send the `X-Database-Id` header of the database it belongs to. Choose the format with `?format=` (`json`, `arrow`, `csv`, `md` or `parquet`) or the `Accept` header. `?format=` wins; an unknown value is ignored.

| Result status              | Response                                        |
|----------------------------|-------------------------------------------------|
| `ready`                    | 200 with the rows in the chosen format          |
| `pending` or `processing`  | 202 with a `Retry-After` header. Poll again.    |
| `failed`                   | 409 with `error_message`                        |

Use `offset` and `limit` to read part of the result. When more rows follow, a `Link` header with `rel="next"` points to the next page. Rows have no guaranteed order, so paging is not a reliable way to read a whole result. Parquet ignores `offset` and `limit` and returns the whole file.

JSON responses have a size limit: a result too large to return as JSON gets 413 `RESULT_TOO_LARGE`. Arrow, CSV, Markdown and Parquet stream with no size limit, so use them for large results. All formats except Parquet carry `X-Total-Row-Count`, the row count of the whole result.

JSON, CSV and Markdown write `NaN` and `±Inf` as `null` or an empty cell. Arrow and Parquet keep the original values.

### Example

* Api Key Authentication (WorkspaceId):
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

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.ResultsApi(api_client)
    id = 'id_example' # str | Result ID
    x_database_id = 'x_database_id_example' # str | ID of the database the result belongs to. Required.
    offset = 56 # int | Rows to skip. Default 0. (optional)
    limit = 56 # int | Maximum rows to return. Default: all rows. (optional)
    format = hotdata.ResultsFormatQuery() # ResultsFormatQuery | `json`, `arrow`, `csv`, `md` (or `markdown`) or `parquet`. Overrides the `Accept` header. (optional)

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
 **x_database_id** | **str**| ID of the database the result belongs to. Required. | 
 **offset** | **int**| Rows to skip. Default 0. | [optional] 
 **limit** | **int**| Maximum rows to return. Default: all rows. | [optional] 
 **format** | [**ResultsFormatQuery**](.md)| &#x60;json&#x60;, &#x60;arrow&#x60;, &#x60;csv&#x60;, &#x60;md&#x60; (or &#x60;markdown&#x60;) or &#x60;parquet&#x60;. Overrides the &#x60;Accept&#x60; header. | [optional] 

### Return type

[**GetResultResponse**](GetResultResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.apache.arrow.stream, text/csv, text/markdown, application/vnd.apache.parquet

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result rows. JSON returns &#x60;GetResultResponse&#x60;. Arrow returns an IPC stream. CSV uses LF line endings and double-quote escaping. Markdown returns one pipe table. Parquet returns the stored file. &#x60;q&#x3D;&#x60; values in &#x60;Accept&#x60; are ignored; use &#x60;?format&#x3D;&#x60; to choose. |  * Link - Link to the next page (&#x60;rel&#x3D;\&quot;next\&quot;&#x60;), when &#x60;limit&#x60; stops before the end of the result <br>  * X-Total-Row-Count - Rows in the whole result, ignoring &#x60;offset&#x60; and &#x60;limit&#x60; <br>  |
**202** | The result is not ready yet. Poll the same URL. |  * Retry-After - Suggested seconds before retrying. <br>  |
**400** | Invalid &#x60;offset&#x60; or &#x60;limit&#x60; |  -  |
**404** | Result not found |  -  |
**409** | The query failed. &#x60;error_message&#x60; says why. |  -  |
**413** | JSON only: the rows are too large to return as JSON (&#x60;RESULT_TOO_LARGE&#x60;). Retrying will not help. Request &#x60;arrow&#x60;, &#x60;csv&#x60;, &#x60;md&#x60; or &#x60;parquet&#x60; instead. |  -  |
**429** | JSON only: too many large JSON reads are running. Retry shortly, or use a streaming format. |  -  |
**503** | JSON only: the result&#39;s size could not be checked. Retry shortly, or use a streaming format. |  * Retry-After - Suggested seconds before retrying. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_results**
> ListResultsResponse list_results(x_database_id, limit=limit, offset=offset)

List results

List saved query results in the database named by the `X-Database-Id` header, newest first.

### Example

* Api Key Authentication (WorkspaceId):
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

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.ResultsApi(api_client)
    x_database_id = 'x_database_id_example' # str | Database ID. Required.
    limit = 56 # int | Results to return. Default 100, maximum 1000. (optional)
    offset = 56 # int | Number of results to skip. Default 0. (optional)

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
 **x_database_id** | **str**| Database ID. Required. | 
 **limit** | **int**| Results to return. Default 100, maximum 1000. | [optional] 
 **offset** | **int**| Number of results to skip. Default 0. | [optional] 

### Return type

[**ListResultsResponse**](ListResultsResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of results |  -  |
**400** | Missing or malformed &#x60;X-Database-Id&#x60; header |  -  |
**404** | Database not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

