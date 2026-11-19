# hotdata.QueryRunsApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_query_run**](QueryRunsApi.md#get_query_run) | **GET** /v1/query-runs/{id} | Get query run
[**list_query_runs**](QueryRunsApi.md#list_query_runs) | **GET** /v1/query-runs | List query runs


# **get_query_run**
> QueryRunInfo get_query_run(id, x_database_id)

Get query run

Get a query run's status and details. Send the `X-Database-Id` header of the database the query ran in.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.query_run_info import QueryRunInfo
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
    api_instance = hotdata.QueryRunsApi(api_client)
    id = 'id_example' # str | Query run ID
    x_database_id = 'x_database_id_example' # str | ID of the database the query ran in. Required.

    try:
        # Get query run
        api_response = api_instance.get_query_run(id, x_database_id)
        print("The response of QueryRunsApi->get_query_run:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QueryRunsApi->get_query_run: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Query run ID | 
 **x_database_id** | **str**| ID of the database the query ran in. Required. | 

### Return type

[**QueryRunInfo**](QueryRunInfo.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Query run details |  -  |
**400** | Missing or malformed &#x60;X-Database-Id&#x60; header |  -  |
**404** | Query run or database not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_query_runs**
> ListQueryRunsResponse list_query_runs(x_database_id, limit=limit, cursor=cursor, status=status, saved_query_id=saved_query_id)

List query runs

List the query runs in the database named by the `X-Database-Id` header, newest first, one page at a time. If `has_more` is true, pass `next_cursor` as `cursor` to get the next page.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_query_runs_response import ListQueryRunsResponse
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
    api_instance = hotdata.QueryRunsApi(api_client)
    x_database_id = 'x_database_id_example' # str | Database ID. Required.
    limit = 56 # int | Runs per page. Default 100, maximum 1000. (optional)
    cursor = 'cursor_example' # str | The `next_cursor` from the previous page (optional)
    status = 'status_example' # str | Filter by status, comma-separated, for example `status=running,failed`. Values: `running`, `succeeded`, `failed`, `interrupted`. (optional)
    saved_query_id = 'saved_query_id_example' # str | Filter by saved query ID (optional)

    try:
        # List query runs
        api_response = api_instance.list_query_runs(x_database_id, limit=limit, cursor=cursor, status=status, saved_query_id=saved_query_id)
        print("The response of QueryRunsApi->list_query_runs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QueryRunsApi->list_query_runs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_database_id** | **str**| Database ID. Required. | 
 **limit** | **int**| Runs per page. Default 100, maximum 1000. | [optional] 
 **cursor** | **str**| The &#x60;next_cursor&#x60; from the previous page | [optional] 
 **status** | **str**| Filter by status, comma-separated, for example &#x60;status&#x3D;running,failed&#x60;. Values: &#x60;running&#x60;, &#x60;succeeded&#x60;, &#x60;failed&#x60;, &#x60;interrupted&#x60;. | [optional] 
 **saved_query_id** | **str**| Filter by saved query ID | [optional] 

### Return type

[**ListQueryRunsResponse**](ListQueryRunsResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of query runs |  -  |
**400** | Missing or malformed &#x60;X-Database-Id&#x60; header |  -  |
**404** | Database not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

