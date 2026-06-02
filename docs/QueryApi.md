# hotdata.QueryApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**query**](QueryApi.md#query) | **POST** /v1/query | Execute SQL query


# **query**
> QueryResponse query(query_request, x_database_id=x_database_id)

Execute SQL query

Execute a SQL query scoped to a database. A database is the only window into catalogs: the query sees only that database's auto `default` catalog plus any catalogs explicitly attached to it. Select the database with EITHER the `X-Database-Id` header OR the `database_id` body field (exactly one must be given; if both are sent and disagree, that's a 400). Use standard Postgres-compatible SQL; reference the default catalog as `default.<schema>.<table>` (or just `<schema>.<table>` / `<table>`) and attached catalogs by their alias. Results are returned inline and a `result_id` is provided for later retrieval via the Results API.

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
    x_database_id = 'x_database_id_example' # str | Database id to scope the query to. Required unless the `database_id` body field is set; if both are present they must match. Only that database's catalogs are visible during planning. A malformed value is a 400; an unknown database id is a 404. (optional)

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
 **x_database_id** | **str**| Database id to scope the query to. Required unless the &#x60;database_id&#x60; body field is set; if both are present they must match. Only that database&#39;s catalogs are visible during planning. A malformed value is a 400; an unknown database id is a 404. | [optional] 

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
**400** | Invalid request (no database specified, or header/body database_id conflict) |  -  |
**404** | Database not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

