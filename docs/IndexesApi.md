# hotdata.IndexesApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_index**](IndexesApi.md#create_index) | **POST** /v1/connections/{connection_id}/tables/{schema}/{table}/indexes | Create an index on a table
[**delete_index**](IndexesApi.md#delete_index) | **DELETE** /v1/connections/{connection_id}/tables/{schema}/{table}/indexes/{index_name} | Delete an index
[**list_indexes**](IndexesApi.md#list_indexes) | **GET** /v1/connections/{connection_id}/tables/{schema}/{table}/indexes | List indexes on a table


# **create_index**
> IndexInfoResponse create_index(connection_id, var_schema, table, create_index_request)

Create an index on a table

Create a sorted or BM25 full-text index on a cached table.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.create_index_request import CreateIndexRequest
from hotdata.models.index_info_response import IndexInfoResponse
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
    api_instance = hotdata.IndexesApi(api_client)
    connection_id = 'connection_id_example' # str | Connection identifier
    var_schema = 'var_schema_example' # str | Schema name
    table = 'table_example' # str | Table name
    create_index_request = hotdata.CreateIndexRequest() # CreateIndexRequest | 

    try:
        # Create an index on a table
        api_response = api_instance.create_index(connection_id, var_schema, table, create_index_request)
        print("The response of IndexesApi->create_index:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndexesApi->create_index: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection identifier | 
 **var_schema** | **str**| Schema name | 
 **table** | **str**| Table name | 
 **create_index_request** | [**CreateIndexRequest**](CreateIndexRequest.md)|  | 

### Return type

[**IndexInfoResponse**](IndexInfoResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Index created |  -  |
**400** | Invalid request |  -  |
**404** | Table not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_index**
> delete_index(connection_id, var_schema, table, index_name)

Delete an index

Delete a specific index from a cached table.

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
    api_instance = hotdata.IndexesApi(api_client)
    connection_id = 'connection_id_example' # str | Connection identifier
    var_schema = 'var_schema_example' # str | Schema name
    table = 'table_example' # str | Table name
    index_name = 'index_name_example' # str | Index name

    try:
        # Delete an index
        api_instance.delete_index(connection_id, var_schema, table, index_name)
    except Exception as e:
        print("Exception when calling IndexesApi->delete_index: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection identifier | 
 **var_schema** | **str**| Schema name | 
 **table** | **str**| Table name | 
 **index_name** | **str**| Index name | 

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
**204** | Index deleted |  -  |
**404** | Index not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_indexes**
> ListIndexesResponse list_indexes(connection_id, var_schema, table)

List indexes on a table

List all indexes created on a cached table.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_indexes_response import ListIndexesResponse
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
    api_instance = hotdata.IndexesApi(api_client)
    connection_id = 'connection_id_example' # str | Connection identifier
    var_schema = 'var_schema_example' # str | Schema name
    table = 'table_example' # str | Table name

    try:
        # List indexes on a table
        api_response = api_instance.list_indexes(connection_id, var_schema, table)
        print("The response of IndexesApi->list_indexes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndexesApi->list_indexes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection identifier | 
 **var_schema** | **str**| Schema name | 
 **table** | **str**| Table name | 

### Return type

[**ListIndexesResponse**](ListIndexesResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Indexes listed |  -  |
**404** | Table not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

