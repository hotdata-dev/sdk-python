# hotdata.WorkspacesApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_workspace**](WorkspacesApi.md#create_workspace) | **POST** /v1/workspaces | Create a workspace
[**delete_workspace**](WorkspacesApi.md#delete_workspace) | **DELETE** /v1/workspaces/{public_id} | Delete a workspace
[**list_workspaces**](WorkspacesApi.md#list_workspaces) | **GET** /v1/workspaces | List workspaces


# **create_workspace**
> CreateWorkspaceResponse create_workspace(create_workspace_request)

Create a workspace

Creates a new workspace in the specified organization.

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.create_workspace_request import CreateWorkspaceRequest
from hotdata.models.create_workspace_response import CreateWorkspaceResponse
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

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.WorkspacesApi(api_client)
    create_workspace_request = hotdata.CreateWorkspaceRequest() # CreateWorkspaceRequest | 

    try:
        # Create a workspace
        api_response = api_instance.create_workspace(create_workspace_request)
        print("The response of WorkspacesApi->create_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->create_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_workspace_request** | [**CreateWorkspaceRequest**](CreateWorkspaceRequest.md)|  | 

### Return type

[**CreateWorkspaceResponse**](CreateWorkspaceResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Workspace created |  -  |
**400** | Invalid JSON body |  -  |
**401** | Missing or invalid authorization |  -  |
**403** | Forbidden |  -  |
**404** | Organization not found |  -  |
**422** | Validation error (e.g. name required) |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_workspace**
> delete_workspace(public_id)

Delete a workspace

Hard-deletes the workspace. Namespace, storage, and catalog deprovisioning runs asynchronously after the row is removed.

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
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

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.WorkspacesApi(api_client)
    public_id = 'public_id_example' # str | Public id of the workspace.

    try:
        # Delete a workspace
        api_instance.delete_workspace(public_id)
    except Exception as e:
        print("Exception when calling WorkspacesApi->delete_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **public_id** | **str**| Public id of the workspace. | 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Workspace deleted |  -  |
**401** | Missing or invalid authorization |  -  |
**403** | Workspace-scoped tokens are not allowed |  -  |
**404** | Workspace not found, or caller is not a member of its organization |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_workspaces**
> ListWorkspacesResponse list_workspaces(organization_public_id=organization_public_id)

List workspaces

Lists all workspaces in the user's organization.

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_workspaces_response import ListWorkspacesResponse
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

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.WorkspacesApi(api_client)
    organization_public_id = 'organization_public_id_example' # str | Filter by organization. Defaults to the user's current organization. (optional)

    try:
        # List workspaces
        api_response = api_instance.list_workspaces(organization_public_id=organization_public_id)
        print("The response of WorkspacesApi->list_workspaces:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->list_workspaces: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_public_id** | **str**| Filter by organization. Defaults to the user&#39;s current organization. | [optional] 

### Return type

[**ListWorkspacesResponse**](ListWorkspacesResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**401** | Missing or invalid authorization |  -  |
**403** | Forbidden — not a member of the organization or workspace token used |  -  |
**404** | Organization not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

