# hotdata.ConnectionsApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_managed_schema**](ConnectionsApi.md#add_managed_schema) | **POST** /v1/connections/{connection_id}/schemas | Add managed schema
[**add_managed_table**](ConnectionsApi.md#add_managed_table) | **POST** /v1/connections/{connection_id}/schemas/{schema}/tables | Add managed table
[**check_connection_health**](ConnectionsApi.md#check_connection_health) | **GET** /v1/connections/{connection_id}/health | Check connection health
[**create_connection**](ConnectionsApi.md#create_connection) | **POST** /v1/connections | Create connection
[**delete_connection**](ConnectionsApi.md#delete_connection) | **DELETE** /v1/connections/{connection_id} | Delete connection
[**delete_managed_table**](ConnectionsApi.md#delete_managed_table) | **DELETE** /v1/connections/{connection_id}/schemas/{schema}/tables/{table} | Delete managed table
[**get_connection**](ConnectionsApi.md#get_connection) | **GET** /v1/connections/{connection_id} | Get connection
[**get_table_profile**](ConnectionsApi.md#get_table_profile) | **GET** /v1/connections/{connection_id}/tables/{schema}/{table}/profile | Get table profile
[**list_connections**](ConnectionsApi.md#list_connections) | **GET** /v1/connections | List connections
[**load_managed_table**](ConnectionsApi.md#load_managed_table) | **POST** /v1/connections/{connection_id}/schemas/{schema}/tables/{table}/loads | Load managed table from upload
[**purge_connection_cache**](ConnectionsApi.md#purge_connection_cache) | **DELETE** /v1/connections/{connection_id}/cache | Purge connection cache
[**purge_table_cache**](ConnectionsApi.md#purge_table_cache) | **DELETE** /v1/connections/{connection_id}/tables/{schema}/{table}/cache | Purge table cache


# **add_managed_schema**
> ManagedSchemaResponse add_managed_schema(connection_id, add_managed_schema_request)

Add managed schema

Declare a new schema (and optionally its tables) on an existing managed catalog after creation. The schema is added to the connection's declaration; declared tables can then be populated via the managed-table load endpoint. Only valid against connections whose source type is `managed`. Identifiers are normalized to lowercase.

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
**400** | Connection is not a managed catalog or identifier is invalid |  -  |
**404** | Connection not found |  -  |
**409** | Schema already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_managed_table**
> ManagedTableResponse add_managed_table(connection_id, var_schema, add_managed_table_request)

Add managed table

Declare a new table on an existing schema of a managed catalog after creation. The table is added empty (declared-but-unloaded) and can be populated via the managed-table load endpoint. Only valid against connections whose source type is `managed`. Identifiers are normalized to lowercase.

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
**400** | Connection is not a managed catalog or identifier is invalid |  -  |
**404** | Connection or schema not found |  -  |
**409** | Table already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **check_connection_health**
> ConnectionHealthResponse check_connection_health(connection_id)

Check connection health

Test connectivity to the remote database. Returns health status and latency.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.connection_health_response import ConnectionHealthResponse
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
        # Check connection health
        api_response = api_instance.check_connection_health(connection_id)
        print("The response of ConnectionsApi->check_connection_health:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->check_connection_health: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 

### Return type

[**ConnectionHealthResponse**](ConnectionHealthResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Connection health status |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_connection**
> CreateConnectionResponse create_connection(create_connection_request)

Create connection

Register a new database connection. Provide the source type and connection config (host, port, database, etc.). Credentials can be supplied inline (password/token fields are auto-converted to secrets) or by referencing an existing secret by name or ID. Schema discovery runs automatically after registration.

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
**409** | Connection already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_connection**
> delete_connection(connection_id)

Delete connection

Delete a connection and its cached data.

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
**409** | Connection backs a database&#39;s default catalog, or is attached to one or more databases as a non-default catalog; detach via DELETE /v1/databases/{database_id}/catalogs/{connection_id} first |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_managed_table**
> delete_managed_table(connection_id, var_schema, table)

Delete managed table

Delete a single managed-catalog table. The table and its data are removed. Only valid against connections whose source type is `managed`.

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
**400** | Connection is not a managed catalog |  -  |
**404** | Connection or table not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connection**
> GetConnectionResponse get_connection(connection_id)

Get connection

Get details for a specific connection, including table and sync counts.

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

Get column-level statistics for a synced table. Returns per-column profiles including cardinality, null counts, and type-specific details (distinct values for categorical columns, min/max for temporal/numeric, length stats for text). Profiles are computed at sync time.

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
**404** | Table or profile not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_connections**
> ListConnectionsResponse list_connections()

List connections

List all registered database connections.

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

Load managed table from upload

Publish a previously-uploaded file as the new contents of a managed table. CSV, JSON, and Parquet uploads are supported; the format is auto-detected from the upload's `Content-Type` and file contents, or set explicitly via the `format` field. If the target table (or its schema) has not been declared yet, it is created automatically as part of the load — declaring tables up front is optional. `mode` selects how the upload is applied: `replace` overwrites the table's contents, `append` inserts the uploaded rows on top of the existing data. Concurrent loads against the same upload return 409. Set `async` to run the load in the background and get back a job ID to poll; add `async_after_ms` to wait briefly for it to finish before falling back to a job ID.

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
    load_managed_table_request = hotdata.LoadManagedTableRequest() # LoadManagedTableRequest | 

    try:
        # Load managed table from upload
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
**202** | Load accepted and running in the background; poll the returned job for status and result |  -  |
**400** | Invalid request (bad mode, non-managed connection, invalid identifier, bad parquet) |  -  |
**404** | Connection or upload not found, or the table was deleted |  -  |
**409** | Upload already consumed or in flight, or the uploaded data changes a column&#39;s type incompatibly (only widening to a larger compatible type can be applied automatically); the existing data is unchanged and remains queryable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **purge_connection_cache**
> purge_connection_cache(connection_id)

Purge connection cache

Purge all cached data for a connection. The next query against these tables will trigger a fresh sync from the remote source.

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
        # Purge connection cache
        api_instance.purge_connection_cache(connection_id)
    except Exception as e:
        print("Exception when calling ConnectionsApi->purge_connection_cache: %s\n" % e)
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
**204** | Cache purged |  -  |
**400** | Managed catalogs own their data and cannot be cache-purged |  -  |
**404** | Connection not found |  -  |
**409** | Connection backs a database&#39;s default catalog and cannot be purged directly |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **purge_table_cache**
> purge_table_cache(connection_id, var_schema, table)

Purge table cache

Purge the cached data for a single table. The next query will trigger a fresh sync.

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
        # Purge table cache
        api_instance.purge_table_cache(connection_id, var_schema, table)
    except Exception as e:
        print("Exception when calling ConnectionsApi->purge_table_cache: %s\n" % e)
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
**204** | Table cache purged |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

