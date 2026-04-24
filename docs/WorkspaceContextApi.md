# hotdata.WorkspaceContextApi

All URIs are relative to *https://app.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_workspace_context**](WorkspaceContextApi.md#get_workspace_context) | **GET** /v1/context/{name} | Get one workspace context
[**list_workspace_contexts**](WorkspaceContextApi.md#list_workspace_contexts) | **GET** /v1/context | List workspace contexts
[**upsert_workspace_context**](WorkspaceContextApi.md#upsert_workspace_context) | **POST** /v1/context | Create or update workspace context


# **get_workspace_context**
> GetWorkspaceContextResponse get_workspace_context(name)

Get one workspace context

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.get_workspace_context_response import GetWorkspaceContextResponse
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
    api_instance = hotdata.WorkspaceContextApi(api_client)
    name = 'name_example' # str | Context key: same character rules as a dataset table name (letter or underscore first; no hyphens)

    try:
        # Get one workspace context
        api_response = api_instance.get_workspace_context(name)
        print("The response of WorkspaceContextApi->get_workspace_context:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceContextApi->get_workspace_context: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Context key: same character rules as a dataset table name (letter or underscore first; no hyphens) | 

### Return type

[**GetWorkspaceContextResponse**](GetWorkspaceContextResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Context found |  -  |
**400** | Invalid request |  -  |
**404** | Context not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_workspace_contexts**
> ListWorkspaceContextsResponse list_workspace_contexts()

List workspace contexts

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_workspace_contexts_response import ListWorkspaceContextsResponse
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
    api_instance = hotdata.WorkspaceContextApi(api_client)

    try:
        # List workspace contexts
        api_response = api_instance.list_workspace_contexts()
        print("The response of WorkspaceContextApi->list_workspace_contexts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceContextApi->list_workspace_contexts: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListWorkspaceContextsResponse**](ListWorkspaceContextsResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Contexts |  -  |
**400** | Invalid request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upsert_workspace_context**
> UpsertWorkspaceContextResponse upsert_workspace_context(upsert_workspace_context_request)

Create or update workspace context

Stores a named document (for example Markdown). Reuses the same name to replace content. Scoped to the deployment catalog like other metadata (connections, secrets, etc.).

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.upsert_workspace_context_request import UpsertWorkspaceContextRequest
from hotdata.models.upsert_workspace_context_response import UpsertWorkspaceContextResponse
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
    api_instance = hotdata.WorkspaceContextApi(api_client)
    upsert_workspace_context_request = hotdata.UpsertWorkspaceContextRequest() # UpsertWorkspaceContextRequest | 

    try:
        # Create or update workspace context
        api_response = api_instance.upsert_workspace_context(upsert_workspace_context_request)
        print("The response of WorkspaceContextApi->upsert_workspace_context:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceContextApi->upsert_workspace_context: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **upsert_workspace_context_request** | [**UpsertWorkspaceContextRequest**](UpsertWorkspaceContextRequest.md)|  | 

### Return type

[**UpsertWorkspaceContextResponse**](UpsertWorkspaceContextResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Context saved |  -  |
**400** | Invalid request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

