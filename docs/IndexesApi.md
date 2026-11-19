# hotdata.IndexesApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_index**](IndexesApi.md#create_index) | **POST** /v1/connections/{connection_id}/tables/{schema}/{table}/indexes | Create an index on a table
[**delete_index**](IndexesApi.md#delete_index) | **DELETE** /v1/connections/{connection_id}/tables/{schema}/{table}/indexes/{index_name} | Delete an index
[**list_indexes**](IndexesApi.md#list_indexes) | **GET** /v1/connections/{connection_id}/tables/{schema}/{table}/indexes | List indexes on a table
[**list_indexes_collection**](IndexesApi.md#list_indexes_collection) | **GET** /v1/indexes | List indexes across tables in a database


# **create_index**
> IndexInfoResponse create_index(connection_id, var_schema, table, create_index_request)

Create an index on a table

Create a sorted, BM25 full-text or vector index on a table. The table must hold loaded data and must not declare `sorted_by`.

A table can have only one vector index. A vector index that generates its own embeddings (with `embedding_provider_id`) must be the only index on its table. Requests that break these rules return 400, even with `async` set.

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
    connection_id = 'connection_id_example' # str | The database's `default_connection_id`
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
 **connection_id** | **str**| The database&#39;s &#x60;default_connection_id&#x60; | 
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
**202** | The index is building in the background. Poll the returned job. |  -  |
**400** | Invalid request |  -  |
**404** | Table not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_index**
> delete_index(connection_id, var_schema, table, index_name)

Delete an index

Delete an index from a table. Returns 409 while a load into the table is running; retry when it finishes. Deleting a vector index that generated its own embeddings keeps the embedding column in the table.

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
    connection_id = 'connection_id_example' # str | The database's `default_connection_id`
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
 **connection_id** | **str**| The database&#39;s &#x60;default_connection_id&#x60; | 
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
**409** | A load into the table is running. Retry when it finishes. |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_indexes**
> ListIndexesResponse list_indexes(connection_id, var_schema, table)

List indexes on a table

List the indexes on a table.

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
    connection_id = 'connection_id_example' # str | The database's `default_connection_id`
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
 **connection_id** | **str**| The database&#39;s &#x60;default_connection_id&#x60; | 
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

# **list_indexes_collection**
> ListIndexesPageResponse list_indexes_collection(x_database_id, connection_id=connection_id, var_schema=var_schema, table=table, index_type=index_type, limit=limit, cursor=cursor)

List indexes across tables in a database

List the indexes in the database named by the `X-Database-Id` header, one page at a time. Filter by connection, schema, table or index type.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_indexes_page_response import ListIndexesPageResponse
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
    x_database_id = 'x_database_id_example' # str | Database ID. Required.
    connection_id = 'connection_id_example' # str | Filter by connection ID (optional)
    var_schema = 'var_schema_example' # str | Filter by schema name (optional)
    table = 'table_example' # str | Filter by table name (optional)
    index_type = 'index_type_example' # str | Filter by index type: `sorted`, `bm25` or `vector` (optional)
    limit = 56 # int | Indexes per page. Default 100, maximum 1000. (optional)
    cursor = 'cursor_example' # str | The `next_cursor` from the previous page (optional)

    try:
        # List indexes across tables in a database
        api_response = api_instance.list_indexes_collection(x_database_id, connection_id=connection_id, var_schema=var_schema, table=table, index_type=index_type, limit=limit, cursor=cursor)
        print("The response of IndexesApi->list_indexes_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndexesApi->list_indexes_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_database_id** | **str**| Database ID. Required. | 
 **connection_id** | **str**| Filter by connection ID | [optional] 
 **var_schema** | **str**| Filter by schema name | [optional] 
 **table** | **str**| Filter by table name | [optional] 
 **index_type** | **str**| Filter by index type: &#x60;sorted&#x60;, &#x60;bm25&#x60; or &#x60;vector&#x60; | [optional] 
 **limit** | **int**| Indexes per page. Default 100, maximum 1000. | [optional] 
 **cursor** | **str**| The &#x60;next_cursor&#x60; from the previous page | [optional] 

### Return type

[**ListIndexesPageResponse**](ListIndexesPageResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Indexes listed |  -  |
**400** | Missing &#x60;X-Database-Id&#x60;, a bad filter value, or a bad cursor |  -  |
**404** | Database not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

