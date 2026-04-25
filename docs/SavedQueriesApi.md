# hotdata.SavedQueriesApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_saved_query**](SavedQueriesApi.md#create_saved_query) | **POST** /v1/queries | Create saved query
[**delete_saved_query**](SavedQueriesApi.md#delete_saved_query) | **DELETE** /v1/queries/{id} | Delete saved query
[**execute_saved_query**](SavedQueriesApi.md#execute_saved_query) | **POST** /v1/queries/{id}/execute | Execute saved query
[**get_saved_query**](SavedQueriesApi.md#get_saved_query) | **GET** /v1/queries/{id} | Get saved query
[**list_saved_queries**](SavedQueriesApi.md#list_saved_queries) | **GET** /v1/queries | List saved queries
[**list_saved_query_versions**](SavedQueriesApi.md#list_saved_query_versions) | **GET** /v1/queries/{id}/versions | List saved query versions
[**update_saved_query**](SavedQueriesApi.md#update_saved_query) | **PUT** /v1/queries/{id} | Update saved query


# **create_saved_query**
> SavedQueryDetail create_saved_query(create_saved_query_request)

Create saved query

Save a named SQL query. The SQL is stored as version 1 and automatically analyzed for classification metadata (category, table count, predicate/join/aggregation flags).

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.create_saved_query_request import CreateSavedQueryRequest
from hotdata.models.saved_query_detail import SavedQueryDetail
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
    api_instance = hotdata.SavedQueriesApi(api_client)
    create_saved_query_request = hotdata.CreateSavedQueryRequest() # CreateSavedQueryRequest | 

    try:
        # Create saved query
        api_response = api_instance.create_saved_query(create_saved_query_request)
        print("The response of SavedQueriesApi->create_saved_query:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavedQueriesApi->create_saved_query: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_saved_query_request** | [**CreateSavedQueryRequest**](CreateSavedQueryRequest.md)|  | 

### Return type

[**SavedQueryDetail**](SavedQueryDetail.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Saved query created |  -  |
**400** | Invalid request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_saved_query**
> delete_saved_query(id)

Delete saved query

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
    api_instance = hotdata.SavedQueriesApi(api_client)
    id = 'id_example' # str | Saved query ID

    try:
        # Delete saved query
        api_instance.delete_saved_query(id)
    except Exception as e:
        print("Exception when calling SavedQueriesApi->delete_saved_query: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Saved query ID | 

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
**204** | Saved query deleted |  -  |
**404** | Saved query not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **execute_saved_query**
> QueryResponse execute_saved_query(id, execute_saved_query_request=execute_saved_query_request)

Execute saved query

Execute a saved query. By default runs the latest version. Optionally specify a version number to execute a previous version. Returns the same response format as POST /v1/query.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.execute_saved_query_request import ExecuteSavedQueryRequest
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

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.SavedQueriesApi(api_client)
    id = 'id_example' # str | Saved query ID
    execute_saved_query_request = hotdata.ExecuteSavedQueryRequest() # ExecuteSavedQueryRequest | Optional version to execute (optional)

    try:
        # Execute saved query
        api_response = api_instance.execute_saved_query(id, execute_saved_query_request=execute_saved_query_request)
        print("The response of SavedQueriesApi->execute_saved_query:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavedQueriesApi->execute_saved_query: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Saved query ID | 
 **execute_saved_query_request** | [**ExecuteSavedQueryRequest**](ExecuteSavedQueryRequest.md)| Optional version to execute | [optional] 

### Return type

[**QueryResponse**](QueryResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Query executed |  -  |
**404** | Saved query not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_saved_query**
> SavedQueryDetail get_saved_query(id)

Get saved query

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.saved_query_detail import SavedQueryDetail
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
    api_instance = hotdata.SavedQueriesApi(api_client)
    id = 'id_example' # str | Saved query ID

    try:
        # Get saved query
        api_response = api_instance.get_saved_query(id)
        print("The response of SavedQueriesApi->get_saved_query:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavedQueriesApi->get_saved_query: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Saved query ID | 

### Return type

[**SavedQueryDetail**](SavedQueryDetail.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Saved query details |  -  |
**404** | Saved query not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_saved_queries**
> ListSavedQueriesResponse list_saved_queries(limit=limit, offset=offset)

List saved queries

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_saved_queries_response import ListSavedQueriesResponse
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
    api_instance = hotdata.SavedQueriesApi(api_client)
    limit = 56 # int | Maximum number of results (optional)
    offset = 56 # int | Pagination offset (optional)

    try:
        # List saved queries
        api_response = api_instance.list_saved_queries(limit=limit, offset=offset)
        print("The response of SavedQueriesApi->list_saved_queries:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavedQueriesApi->list_saved_queries: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of results | [optional] 
 **offset** | **int**| Pagination offset | [optional] 

### Return type

[**ListSavedQueriesResponse**](ListSavedQueriesResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of saved queries |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_saved_query_versions**
> ListSavedQueryVersionsResponse list_saved_query_versions(id, limit=limit, offset=offset)

List saved query versions

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_saved_query_versions_response import ListSavedQueryVersionsResponse
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
    api_instance = hotdata.SavedQueriesApi(api_client)
    id = 'id_example' # str | Saved query ID
    limit = 56 # int | Maximum number of versions (optional)
    offset = 56 # int | Pagination offset (optional)

    try:
        # List saved query versions
        api_response = api_instance.list_saved_query_versions(id, limit=limit, offset=offset)
        print("The response of SavedQueriesApi->list_saved_query_versions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavedQueriesApi->list_saved_query_versions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Saved query ID | 
 **limit** | **int**| Maximum number of versions | [optional] 
 **offset** | **int**| Pagination offset | [optional] 

### Return type

[**ListSavedQueryVersionsResponse**](ListSavedQueryVersionsResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of versions |  -  |
**404** | Saved query not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_saved_query**
> SavedQueryDetail update_saved_query(id, update_saved_query_request)

Update saved query

Update a saved query. If the SQL changes, a new version is created (previous versions are preserved). Name, tags, description, and classification overrides can also be updated.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.saved_query_detail import SavedQueryDetail
from hotdata.models.update_saved_query_request import UpdateSavedQueryRequest
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
    api_instance = hotdata.SavedQueriesApi(api_client)
    id = 'id_example' # str | Saved query ID
    update_saved_query_request = hotdata.UpdateSavedQueryRequest() # UpdateSavedQueryRequest | 

    try:
        # Update saved query
        api_response = api_instance.update_saved_query(id, update_saved_query_request)
        print("The response of SavedQueriesApi->update_saved_query:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavedQueriesApi->update_saved_query: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Saved query ID | 
 **update_saved_query_request** | [**UpdateSavedQueryRequest**](UpdateSavedQueryRequest.md)|  | 

### Return type

[**SavedQueryDetail**](SavedQueryDetail.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Saved query updated |  -  |
**400** | Invalid request |  -  |
**404** | Saved query not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

