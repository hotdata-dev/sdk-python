# hotdata.ResultsApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_result**](ResultsApi.md#get_result) | **GET** /v1/results/{id} | Get result
[**list_results**](ResultsApi.md#list_results) | **GET** /v1/results | List results


# **get_result**
> GetResultResponse get_result(id)

Get result

Retrieve a persisted query result by ID. If the result is still being processed, only the status is returned. Once ready, the full column and row data is included in the response.

### Example

* Api Key Authentication (WorkspaceId):
* Api Key Authentication (SessionId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.get_result_response import GetResultResponse
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

    try:
        # Get result
        api_response = api_instance.get_result(id)
        print("The response of ResultsApi->get_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->get_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Result ID | 

### Return type

[**GetResultResponse**](GetResultResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [SessionId](../README.md#SessionId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Result data |  -  |
**404** | Result not found |  -  |

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

