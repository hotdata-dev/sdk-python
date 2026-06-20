# hotdata.DatabaseContextApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_database_context**](DatabaseContextApi.md#delete_database_context) | **DELETE** /v1/databases/{database_id}/context/{name} | Delete database context
[**get_database_context**](DatabaseContextApi.md#get_database_context) | **GET** /v1/databases/{database_id}/context/{name} | Get one database context
[**list_database_contexts**](DatabaseContextApi.md#list_database_contexts) | **GET** /v1/databases/{database_id}/context | List database contexts
[**upsert_database_context**](DatabaseContextApi.md#upsert_database_context) | **POST** /v1/databases/{database_id}/context | Create or update database context


# **delete_database_context**
> delete_database_context(database_id, name)

Delete database context

Removes a named context document from a database.

### Example

* Api Key Authentication (WorkspaceId):
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
    api_instance = hotdata.DatabaseContextApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    name = 'name_example' # str | Context key: same character rules as a table name

    try:
        # Delete database context
        api_instance.delete_database_context(database_id, name)
    except Exception as e:
        print("Exception when calling DatabaseContextApi->delete_database_context: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
 **name** | **str**| Context key: same character rules as a table name | 

### Return type

void (empty response body)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Context deleted |  -  |
**400** | Invalid request |  -  |
**404** | Database or context not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_database_context**
> GetDatabaseContextResponse get_database_context(database_id, name)

Get one database context

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.get_database_context_response import GetDatabaseContextResponse
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
    api_instance = hotdata.DatabaseContextApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    name = 'name_example' # str | Context key: same character rules as a table name

    try:
        # Get one database context
        api_response = api_instance.get_database_context(database_id, name)
        print("The response of DatabaseContextApi->get_database_context:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabaseContextApi->get_database_context: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
 **name** | **str**| Context key: same character rules as a table name | 

### Return type

[**GetDatabaseContextResponse**](GetDatabaseContextResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Context found |  -  |
**400** | Invalid request |  -  |
**404** | Database or context not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_database_contexts**
> ListDatabaseContextsResponse list_database_contexts(database_id)

List database contexts

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_database_contexts_response import ListDatabaseContextsResponse
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
    api_instance = hotdata.DatabaseContextApi(api_client)
    database_id = 'database_id_example' # str | Database ID

    try:
        # List database contexts
        api_response = api_instance.list_database_contexts(database_id)
        print("The response of DatabaseContextApi->list_database_contexts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabaseContextApi->list_database_contexts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 

### Return type

[**ListDatabaseContextsResponse**](ListDatabaseContextsResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Contexts |  -  |
**404** | Database not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upsert_database_context**
> UpsertDatabaseContextResponse upsert_database_context(database_id, upsert_database_context_request)

Create or update database context

Stores a named document (for example Markdown) scoped to a database. Reuses the same name to replace content.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.upsert_database_context_request import UpsertDatabaseContextRequest
from hotdata.models.upsert_database_context_response import UpsertDatabaseContextResponse
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
    api_instance = hotdata.DatabaseContextApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    upsert_database_context_request = hotdata.UpsertDatabaseContextRequest() # UpsertDatabaseContextRequest | 

    try:
        # Create or update database context
        api_response = api_instance.upsert_database_context(database_id, upsert_database_context_request)
        print("The response of DatabaseContextApi->upsert_database_context:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabaseContextApi->upsert_database_context: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
 **upsert_database_context_request** | [**UpsertDatabaseContextRequest**](UpsertDatabaseContextRequest.md)|  | 

### Return type

[**UpsertDatabaseContextResponse**](UpsertDatabaseContextResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Context saved |  -  |
**400** | Invalid request |  -  |
**404** | Database not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

