# hotdata.QueryApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**query**](QueryApi.md#query) | **POST** /v1/query | Execute SQL query


# **query**
> QueryResponse query(query_request)

Execute SQL query

Execute a SQL query against all registered connections and datasets. Use standard Postgres-compatible SQL to reference tables from any connection using the format `connection_name.schema.table`. Results are returned inline and a `result_id` is provided for later retrieval via the Results API.

Set `async: true` to execute asynchronously — returns a query run ID for polling. Optionally set `async_after_ms` to attempt synchronous execution first, falling back to async if the query exceeds the timeout.

### Example

* Api Key Authentication (WorkspaceId):
* Api Key Authentication (SessionId):
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
    api_instance = hotdata.QueryApi(api_client)
    query_request = hotdata.QueryRequest() # QueryRequest | 

    try:
        # Execute SQL query
        api_response = api_instance.query(query_request)
        print("The response of QueryApi->query:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QueryApi->query: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_request** | [**QueryRequest**](QueryRequest.md)|  | 

### Return type

[**QueryResponse**](QueryResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [SessionId](../README.md#SessionId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Query executed successfully |  -  |
**202** | Query submitted asynchronously |  -  |
**400** | Invalid request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

