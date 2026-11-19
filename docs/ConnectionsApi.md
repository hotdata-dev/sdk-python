# hotdata.ConnectionsApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_managed_schema**](ConnectionsApi.md#add_managed_schema) | **POST** /v1/connections/{connection_id}/schemas | Add managed schema
[**add_managed_table**](ConnectionsApi.md#add_managed_table) | **POST** /v1/connections/{connection_id}/schemas/{schema}/tables | Add managed table
[**create_connection**](ConnectionsApi.md#create_connection) | **POST** /v1/connections | Create connection
[**delete_connection**](ConnectionsApi.md#delete_connection) | **DELETE** /v1/connections/{connection_id} | Delete connection
[**delete_managed_table**](ConnectionsApi.md#delete_managed_table) | **DELETE** /v1/connections/{connection_id}/schemas/{schema}/tables/{table} | Delete managed table
[**get_connection**](ConnectionsApi.md#get_connection) | **GET** /v1/connections/{connection_id} | Get connection
[**get_table_profile**](ConnectionsApi.md#get_table_profile) | **GET** /v1/connections/{connection_id}/tables/{schema}/{table}/profile | Get table profile
[**list_connections**](ConnectionsApi.md#list_connections) | **GET** /v1/connections | List connections
[**load_managed_table**](ConnectionsApi.md#load_managed_table) | **POST** /v1/connections/{connection_id}/schemas/{schema}/tables/{table}/loads | Load managed table from inline data, upload, or query result
[**set_managed_table_constant_per_key**](ConnectionsApi.md#set_managed_table_constant_per_key) | **PUT** /v1/connections/{connection_id}/schemas/{schema}/tables/{table}/constant-per-key | Declare which columns are constant per key


# **add_managed_schema**
> ManagedSchemaResponse add_managed_schema(connection_id, add_managed_schema_request)

Add managed schema

Add a schema, and optionally its tables, to a `managed` connection. Names are stored in lowercase. To add a schema to a database, use `POST /v1/databases/{database_id}/schemas`.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.add_managed_schema_request import AddManagedSchemaRequest
from hotdata.models.managed_schema_response import ManagedSchemaResponse
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
    api_instance = hotdata.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | Connection ID
    add_managed_schema_request = hotdata.AddManagedSchemaRequest() # AddManagedSchemaRequest | 

    try:
        # Add managed schema
        api_response = api_instance.add_managed_schema(connection_id, add_managed_schema_request)
        print("The response of ConnectionsApi->add_managed_schema:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->add_managed_schema: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 
 **add_managed_schema_request** | [**AddManagedSchemaRequest**](AddManagedSchemaRequest.md)|  | 

### Return type

[**ManagedSchemaResponse**](ManagedSchemaResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Schema added |  -  |
**400** | The connection is not &#x60;managed&#x60;, or a name is invalid |  -  |
**404** | Connection not found |  -  |
**409** | Schema already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_managed_table**
> ManagedTableResponse add_managed_table(connection_id, var_schema, add_managed_table_request)

Add managed table

Add an empty table to a schema in a `managed` connection. Names are stored in lowercase. You do not have to declare tables first: a load creates the table if it is missing.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.add_managed_table_request import AddManagedTableRequest
from hotdata.models.managed_table_response import ManagedTableResponse
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
    api_instance = hotdata.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | Connection ID
    var_schema = 'var_schema_example' # str | Schema name
    add_managed_table_request = hotdata.AddManagedTableRequest() # AddManagedTableRequest | 

    try:
        # Add managed table
        api_response = api_instance.add_managed_table(connection_id, var_schema, add_managed_table_request)
        print("The response of ConnectionsApi->add_managed_table:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->add_managed_table: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 
 **var_schema** | **str**| Schema name | 
 **add_managed_table_request** | [**AddManagedTableRequest**](AddManagedTableRequest.md)|  | 

### Return type

[**ManagedTableResponse**](ManagedTableResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Table added |  -  |
**400** | The connection is not &#x60;managed&#x60;, or a name is invalid |  -  |
**404** | Connection or schema not found |  -  |
**409** | Table already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_connection**
> CreateConnectionResponse create_connection(create_connection_request)

Create connection

Create a catalog that holds data you load into it. `source_type` must be `managed`; other source types are refused with a 400. A managed connection takes no credentials. You can declare its schemas and tables in `config` now, or add them later.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.create_connection_request import CreateConnectionRequest
from hotdata.models.create_connection_response import CreateConnectionResponse
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
    api_instance = hotdata.ConnectionsApi(api_client)
    create_connection_request = hotdata.CreateConnectionRequest() # CreateConnectionRequest | 

    try:
        # Create connection
        api_response = api_instance.create_connection(create_connection_request)
        print("The response of ConnectionsApi->create_connection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->create_connection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_connection_request** | [**CreateConnectionRequest**](CreateConnectionRequest.md)|  | 

### Return type

[**CreateConnectionResponse**](CreateConnectionResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Connection created |  -  |
**400** | Invalid request |  -  |
**409** | A connection with this name already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_connection**
> delete_connection(connection_id)

Delete connection

Delete a connection and all of its tables and data.

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
    api_instance = hotdata.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | Connection ID

    try:
        # Delete connection
        api_instance.delete_connection(connection_id)
    except Exception as e:
        print("Exception when calling ConnectionsApi->delete_connection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 

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
**204** | Connection deleted |  -  |
**404** | Connection not found |  -  |
**409** | The connection is attached to a database, or is a database&#39;s &#x60;default&#x60; catalog. Detach it with &#x60;DELETE /v1/databases/{database_id}/catalogs/{connection_id}&#x60;, or delete the database. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_managed_table**
> delete_managed_table(connection_id, var_schema, table)

Delete managed table

Delete a table and its data from a `managed` connection.

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
    api_instance = hotdata.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | Connection ID
    var_schema = 'var_schema_example' # str | Schema name
    table = 'table_example' # str | Table name

    try:
        # Delete managed table
        api_instance.delete_managed_table(connection_id, var_schema, table)
    except Exception as e:
        print("Exception when calling ConnectionsApi->delete_managed_table: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 
 **var_schema** | **str**| Schema name | 
 **table** | **str**| Table name | 

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
**204** | Managed table deleted |  -  |
**400** | The connection is not &#x60;managed&#x60; |  -  |
**404** | Connection or table not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connection**
> GetConnectionResponse get_connection(connection_id)

Get connection

Get a connection, with its table count and how many of its tables hold loaded data.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.get_connection_response import GetConnectionResponse
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
    api_instance = hotdata.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | Connection ID

    try:
        # Get connection
        api_response = api_instance.get_connection(connection_id)
        print("The response of ConnectionsApi->get_connection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->get_connection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 

### Return type

[**GetConnectionResponse**](GetConnectionResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Connection details |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_table_profile**
> TableProfileResponse get_table_profile(connection_id, var_schema, table)

Get table profile

Get column statistics for a table: row count, null counts, cardinality, and per-type details such as top values, min/max, or text lengths. Returns 404 if the table has no stored profile.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.table_profile_response import TableProfileResponse
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
    api_instance = hotdata.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | Connection ID
    var_schema = 'var_schema_example' # str | Schema name
    table = 'table_example' # str | Table name

    try:
        # Get table profile
        api_response = api_instance.get_table_profile(connection_id, var_schema, table)
        print("The response of ConnectionsApi->get_table_profile:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->get_table_profile: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 
 **var_schema** | **str**| Schema name | 
 **table** | **str**| Table name | 

### Return type

[**TableProfileResponse**](TableProfileResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Column profile statistics |  -  |
**404** | Table not found, or the table has no profile |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_connections**
> ListConnectionsResponse list_connections()

List connections

List the connections in this workspace.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_connections_response import ListConnectionsResponse
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
    api_instance = hotdata.ConnectionsApi(api_client)

    try:
        # List connections
        api_response = api_instance.list_connections()
        print("The response of ConnectionsApi->list_connections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->list_connections: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListConnectionsResponse**](ListConnectionsResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of connections |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **load_managed_table**
> LoadManagedTableResponse load_managed_table(connection_id, var_schema, table, load_managed_table_request)

Load managed table from inline data, upload, or query result

Load data into a table in a `managed` connection. Give exactly one source: `data` (inline CSV, up to 2 MiB), `upload_id` (a CSV, JSON or Parquet file from `POST /v1/uploads`) or `result_id` (a saved query result). The table and its schema are created if they do not exist. `mode` sets how the rows apply.

Set `async` to run an upload or inline load as a background job; a `result_id` load always runs inline. If maintenance is running on the table, the load waits up to 60 seconds before it starts. If another write holds the table, you get 409 with `RESOURCE_LOCKED` and a `Retry-After` header.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.load_managed_table_request import LoadManagedTableRequest
from hotdata.models.load_managed_table_response import LoadManagedTableResponse
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
    api_instance = hotdata.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | Connection ID
    var_schema = 'var_schema_example' # str | Schema name
    table = 'table_example' # str | Table name
    load_managed_table_request = {"mode":"replace","data":"order_id,customer_id,amount\n1001,42,1999\n1002,7,4550\n","format":"csv","columns":{"order_id":"BIGINT","customer_id":"BIGINT","amount":{"type":"DECIMAL","precision":10,"scale":2}}} # LoadManagedTableRequest | 

    try:
        # Load managed table from inline data, upload, or query result
        api_response = api_instance.load_managed_table(connection_id, var_schema, table, load_managed_table_request)
        print("The response of ConnectionsApi->load_managed_table:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->load_managed_table: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 
 **var_schema** | **str**| Schema name | 
 **table** | **str**| Table name | 
 **load_managed_table_request** | [**LoadManagedTableRequest**](LoadManagedTableRequest.md)|  | 

### Return type

[**LoadManagedTableResponse**](LoadManagedTableResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Managed table loaded |  -  |
**202** | The load is running in the background. Poll the returned job. |  -  |
**400** | Invalid request, such as a bad &#x60;mode&#x60;, not exactly one data source, data that cannot be parsed, a connection that is not &#x60;managed&#x60;, or a result that failed to compute |  -  |
**404** | Connection, upload, or result not found, or the table was deleted |  -  |
**409** | Conflict: the upload was already used or is in use, the result is not ready, or the data changes a column&#39;s type in a way that cannot be widened. The table is unchanged. With &#x60;RESOURCE_LOCKED&#x60;, another write holds the table; retry after the &#x60;Retry-After&#x60; delay. |  -  |
**413** | Inline &#x60;data&#x60; is over 2 MiB (&#x60;INLINE_DATA_TOO_LARGE&#x60;). Upload the file and load it by &#x60;upload_id&#x60;. |  -  |
**503** | The catalog is busy (&#x60;CATALOG_BUSY&#x60;). The load may already have written its data, so check the table or use an idempotency key before you retry after the &#x60;Retry-After&#x60; delay. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_managed_table_constant_per_key**
> ManagedTableConstantPerKeyResponse set_managed_table_constant_per_key(connection_id, var_schema, table, update_managed_table_request)

Declare which columns are constant per key

Set which columns never change for a given key. Keyed loads (`delete`, `update`, `upsert`) use this to search fewer files. You can change it at any time; it applies from the next load. Send an empty array to clear it.

Only declare columns that really are constant per key. If they are not, a keyed load can leave duplicate rows.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.managed_table_constant_per_key_response import ManagedTableConstantPerKeyResponse
from hotdata.models.update_managed_table_request import UpdateManagedTableRequest
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
    api_instance = hotdata.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | Connection ID
    var_schema = 'var_schema_example' # str | Schema name
    table = 'table_example' # str | Table name
    update_managed_table_request = hotdata.UpdateManagedTableRequest() # UpdateManagedTableRequest | 

    try:
        # Declare which columns are constant per key
        api_response = api_instance.set_managed_table_constant_per_key(connection_id, var_schema, table, update_managed_table_request)
        print("The response of ConnectionsApi->set_managed_table_constant_per_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->set_managed_table_constant_per_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 
 **var_schema** | **str**| Schema name | 
 **table** | **str**| Table name | 
 **update_managed_table_request** | [**UpdateManagedTableRequest**](UpdateManagedTableRequest.md)|  | 

### Return type

[**ManagedTableConstantPerKeyResponse**](ManagedTableConstantPerKeyResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The table&#39;s declaration as it now stands |  -  |
**400** | The connection is not &#x60;managed&#x60;, a column name is invalid, or the table has no key |  -  |
**404** | Connection, schema or table not found |  -  |
**409** | The setting changed at the same time. Retry. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

