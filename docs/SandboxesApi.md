# hotdata.SandboxesApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_sandbox**](SandboxesApi.md#create_sandbox) | **POST** /v1/sandboxes | Create a sandbox
[**delete_sandbox**](SandboxesApi.md#delete_sandbox) | **DELETE** /v1/sandboxes/{public_id} | Delete sandbox
[**get_sandbox**](SandboxesApi.md#get_sandbox) | **GET** /v1/sandboxes/{public_id} | Get sandbox
[**list_sandboxes**](SandboxesApi.md#list_sandboxes) | **GET** /v1/sandboxes | List sandboxes
[**update_sandbox**](SandboxesApi.md#update_sandbox) | **PATCH** /v1/sandboxes/{public_id} | Update sandbox


# **create_sandbox**
> SandboxResponse create_sandbox(create_sandbox_request)

Create a sandbox

Creates a sandbox in the requested workspace. The returned `public_id` is the value to pass as `X-Session-Id` on scoped ops.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.create_sandbox_request import CreateSandboxRequest
from hotdata.models.sandbox_response import SandboxResponse
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
    api_instance = hotdata.SandboxesApi(api_client)
    create_sandbox_request = hotdata.CreateSandboxRequest() # CreateSandboxRequest | 

    try:
        # Create a sandbox
        api_response = api_instance.create_sandbox(create_sandbox_request)
        print("The response of SandboxesApi->create_sandbox:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SandboxesApi->create_sandbox: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_sandbox_request** | [**CreateSandboxRequest**](CreateSandboxRequest.md)|  | 

### Return type

[**SandboxResponse**](SandboxResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Sandbox created |  -  |
**400** | Invalid JSON body or missing X-Workspace-Id header |  -  |
**401** | Missing or invalid authorization |  -  |
**403** | Not a member of the target workspace&#39;s organization |  -  |
**404** | Workspace not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_sandbox**
> DeleteSandboxResponse delete_sandbox(public_id)

Delete sandbox

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.delete_sandbox_response import DeleteSandboxResponse
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
    api_instance = hotdata.SandboxesApi(api_client)
    public_id = 'public_id_example' # str | Public id of the sandbox.

    try:
        # Delete sandbox
        api_response = api_instance.delete_sandbox(public_id)
        print("The response of SandboxesApi->delete_sandbox:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SandboxesApi->delete_sandbox: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **public_id** | **str**| Public id of the sandbox. | 

### Return type

[**DeleteSandboxResponse**](DeleteSandboxResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Sandbox deleted |  -  |
**401** | Missing or invalid authorization |  -  |
**403** | Not a member of the target workspace&#39;s organization |  -  |
**404** | Sandbox not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sandbox**
> SandboxResponse get_sandbox(public_id)

Get sandbox

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.sandbox_response import SandboxResponse
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
    api_instance = hotdata.SandboxesApi(api_client)
    public_id = 'public_id_example' # str | Public id of the sandbox.

    try:
        # Get sandbox
        api_response = api_instance.get_sandbox(public_id)
        print("The response of SandboxesApi->get_sandbox:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SandboxesApi->get_sandbox: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **public_id** | **str**| Public id of the sandbox. | 

### Return type

[**SandboxResponse**](SandboxResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**401** | Missing or invalid authorization |  -  |
**403** | Not a member of the target workspace&#39;s organization |  -  |
**404** | Sandbox not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_sandboxes**
> ListSandboxesResponse list_sandboxes()

List sandboxes

Lists sandboxes for the caller in the requested workspace.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_sandboxes_response import ListSandboxesResponse
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
    api_instance = hotdata.SandboxesApi(api_client)

    try:
        # List sandboxes
        api_response = api_instance.list_sandboxes()
        print("The response of SandboxesApi->list_sandboxes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SandboxesApi->list_sandboxes: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListSandboxesResponse**](ListSandboxesResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Missing or invalid X-Workspace-Id header |  -  |
**401** | Missing or invalid authorization |  -  |
**403** | Not a member of the target workspace&#39;s organization |  -  |
**404** | Workspace not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_sandbox**
> SandboxResponse update_sandbox(public_id, update_sandbox_request)

Update sandbox

Partial update. Only the provided fields are changed.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.sandbox_response import SandboxResponse
from hotdata.models.update_sandbox_request import UpdateSandboxRequest
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
    api_instance = hotdata.SandboxesApi(api_client)
    public_id = 'public_id_example' # str | Public id of the sandbox.
    update_sandbox_request = hotdata.UpdateSandboxRequest() # UpdateSandboxRequest | 

    try:
        # Update sandbox
        api_response = api_instance.update_sandbox(public_id, update_sandbox_request)
        print("The response of SandboxesApi->update_sandbox:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SandboxesApi->update_sandbox: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **public_id** | **str**| Public id of the sandbox. | 
 **update_sandbox_request** | [**UpdateSandboxRequest**](UpdateSandboxRequest.md)|  | 

### Return type

[**SandboxResponse**](SandboxResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Sandbox updated |  -  |
**400** | Invalid JSON body |  -  |
**401** | Missing or invalid authorization |  -  |
**403** | Not a member of the target workspace&#39;s organization |  -  |
**404** | Sandbox not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

