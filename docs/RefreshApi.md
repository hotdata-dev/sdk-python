# hotdata.RefreshApi

All URIs are relative to *https://app.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**refresh**](RefreshApi.md#refresh) | **POST** /v1/refresh | Refresh connection data


# **refresh**
> RefreshResponse refresh(refresh_request)

Refresh connection data

Refresh schema metadata or table data. The behavior depends on the request fields:

- **Schema refresh (all)**: omit all fields — re-discovers tables for every connection.
- **Schema refresh (single)**: set `connection_id` — re-discovers tables for one connection.
- **Data refresh (single table)**: set `connection_id`, `schema_name`, `table_name`, and `data: true`.
- **Data refresh (connection)**: set `connection_id` and `data: true` — refreshes all cached tables. Set `include_uncached: true` to also sync tables that haven't been cached yet.

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.refresh_request import RefreshRequest
from hotdata.models.refresh_response import RefreshResponse
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
    api_instance = hotdata.RefreshApi(api_client)
    refresh_request = hotdata.RefreshRequest() # RefreshRequest | 

    try:
        # Refresh connection data
        api_response = api_instance.refresh(refresh_request)
        print("The response of RefreshApi->refresh:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RefreshApi->refresh: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **refresh_request** | [**RefreshRequest**](RefreshRequest.md)|  | 

### Return type

[**RefreshResponse**](RefreshResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Refresh completed |  -  |
**400** | Invalid request |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

