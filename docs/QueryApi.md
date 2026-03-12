# hotdata.QueryApi

All URIs are relative to *https://app.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**query_handler**](QueryApi.md#query_handler) | **POST** /v1/query | Execute SQL query


# **query_handler**
> QueryResponse query_handler(query_request)

Execute SQL query

Execute a SQL query against all registered connections and datasets. Use standard Postgres-compatible SQL to reference tables from any connection using the format `connection_name.schema.table`. Results are returned inline and a `result_id` is provided for later retrieval via the Results API.

### Example


```python
import hotdata
from hotdata.models.query_request import QueryRequest
from hotdata.models.query_response import QueryResponse
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
    api_instance = hotdata.QueryApi(api_client)
    query_request = hotdata.QueryRequest() # QueryRequest | 

    try:
        # Execute SQL query
        api_response = api_instance.query_handler(query_request)
        print("The response of QueryApi->query_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QueryApi->query_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_request** | [**QueryRequest**](QueryRequest.md)|  | 

### Return type

[**QueryResponse**](QueryResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Query executed successfully |  -  |
**400** | Invalid request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

