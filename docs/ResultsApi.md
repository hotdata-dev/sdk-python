# hotdata.ResultsApi

All URIs are relative to *https://app.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_result_handler**](ResultsApi.md#get_result_handler) | **GET** /v1/results/{id} | Get result
[**list_results_handler**](ResultsApi.md#list_results_handler) | **GET** /v1/results | List results


# **get_result_handler**
> GetResultResponse get_result_handler(id)

Get result

Retrieve a persisted query result by ID. If the result is still being processed, only the status is returned. Once ready, the full column and row data is included in the response.

### Example


```python
import hotdata
from hotdata.models.get_result_response import GetResultResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.ResultsApi(api_client)
    id = 'id_example' # str | Result ID

    try:
        # Get result
        api_response = api_instance.get_result_handler(id)
        print("The response of ResultsApi->get_result_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->get_result_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Result ID | 

### Return type

[**GetResultResponse**](GetResultResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Result data |  -  |
**404** | Result not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_results_handler**
> ListResultsResponse list_results_handler(limit=limit, offset=offset)

List results

### Example


```python
import hotdata
from hotdata.models.list_results_response import ListResultsResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.ResultsApi(api_client)
    limit = 56 # int | Maximum number of results (default: 100, max: 1000) (optional)
    offset = 56 # int | Pagination offset (default: 0) (optional)

    try:
        # List results
        api_response = api_instance.list_results_handler(limit=limit, offset=offset)
        print("The response of ResultsApi->list_results_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->list_results_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of results (default: 100, max: 1000) | [optional] 
 **offset** | **int**| Pagination offset (default: 0) | [optional] 

### Return type

[**ListResultsResponse**](ListResultsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of results |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

