# hotdata.UsageApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_usage**](UsageApi.md#get_usage) | **GET** /v1/usage | Get workspace usage snapshot


# **get_usage**
> WorkspaceUsageResponse get_usage(since=since)

Get workspace usage snapshot

Return aggregated bytes scanned and current storage size for a billing period. Pass `since` as the subscription's `current_period_start` so the meter value aligns with the Stripe invoice window rather than the calendar month.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.workspace_usage_response import WorkspaceUsageResponse
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
    api_instance = hotdata.UsageApi(api_client)
    since = 'since_example' # str | Billing period start (ISO-8601). Defaults to the start of the current UTC calendar month when omitted. (optional)

    try:
        # Get workspace usage snapshot
        api_response = api_instance.get_usage(since=since)
        print("The response of UsageApi->get_usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsageApi->get_usage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **since** | **str**| Billing period start (ISO-8601). Defaults to the start of the current UTC calendar month when omitted. | [optional] 

### Return type

[**WorkspaceUsageResponse**](WorkspaceUsageResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Workspace usage snapshot |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

