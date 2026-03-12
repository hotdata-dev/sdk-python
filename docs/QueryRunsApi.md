# hotdata.QueryRunsApi

All URIs are relative to *https://app.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_query_runs**](QueryRunsApi.md#list_query_runs) | **GET** /v1/query-runs | List query runs


# **list_query_runs**
> ListQueryRunsResponse list_query_runs(limit=limit, cursor=cursor)

List query runs

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_query_runs_response import ListQueryRunsResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.QueryRunsApi(api_client)
    limit = 56 # int | Maximum number of results (optional)
    cursor = 'cursor_example' # str | Pagination cursor (optional)

    try:
        # List query runs
        api_response = api_instance.list_query_runs(limit=limit, cursor=cursor)
        print("The response of QueryRunsApi->list_query_runs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QueryRunsApi->list_query_runs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of results | [optional] 
 **cursor** | **str**| Pagination cursor | [optional] 

### Return type

[**ListQueryRunsResponse**](ListQueryRunsResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of query runs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

