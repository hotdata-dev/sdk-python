# hotdata.ConnectionsApi

All URIs are relative to *https://app.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**check_connection_health_handler**](ConnectionsApi.md#check_connection_health_handler) | **GET** /v1/connections/{connection_id}/health | Check connection health
[**create_connection_handler**](ConnectionsApi.md#create_connection_handler) | **POST** /v1/connections | Create connection
[**delete_connection_handler**](ConnectionsApi.md#delete_connection_handler) | **DELETE** /v1/connections/{connection_id} | Delete connection
[**get_connection_handler**](ConnectionsApi.md#get_connection_handler) | **GET** /v1/connections/{connection_id} | Get connection
[**get_table_profile_handler**](ConnectionsApi.md#get_table_profile_handler) | **GET** /v1/connections/{connection_id}/tables/{schema}/{table}/profile | Get table profile
[**list_connections_handler**](ConnectionsApi.md#list_connections_handler) | **GET** /v1/connections | List connections
[**purge_connection_cache_handler**](ConnectionsApi.md#purge_connection_cache_handler) | **DELETE** /v1/connections/{connection_id}/cache | Purge connection cache
[**purge_table_cache_handler**](ConnectionsApi.md#purge_table_cache_handler) | **DELETE** /v1/connections/{connection_id}/tables/{schema}/{table}/cache | Purge table cache


# **check_connection_health_handler**
> ConnectionHealthResponse check_connection_health_handler(connection_id)

Check connection health

Test connectivity to the remote database. Returns health status and latency.

### Example


```python
import hotdata
from hotdata.models.connection_health_response import ConnectionHealthResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | Connection ID

    try:
        # Check connection health
        api_response = api_instance.check_connection_health_handler(connection_id)
        print("The response of ConnectionsApi->check_connection_health_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->check_connection_health_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 

### Return type

[**ConnectionHealthResponse**](ConnectionHealthResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Connection health status |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_connection_handler**
> CreateConnectionResponse create_connection_handler(create_connection_request)

Create connection

Register a new database connection. Provide the source type and connection config (host, port, database, etc.). Credentials can be supplied inline (password/token fields are auto-converted to secrets) or by referencing an existing secret by name or ID. Schema discovery runs automatically after registration.

### Example


```python
import hotdata
from hotdata.models.create_connection_request import CreateConnectionRequest
from hotdata.models.create_connection_response import CreateConnectionResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.ConnectionsApi(api_client)
    create_connection_request = hotdata.CreateConnectionRequest() # CreateConnectionRequest | 

    try:
        # Create connection
        api_response = api_instance.create_connection_handler(create_connection_request)
        print("The response of ConnectionsApi->create_connection_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->create_connection_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_connection_request** | [**CreateConnectionRequest**](CreateConnectionRequest.md)|  | 

### Return type

[**CreateConnectionResponse**](CreateConnectionResponse.md)

### Authorization

No authorization required

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

# **delete_connection_handler**
> delete_connection_handler(connection_id)

Delete connection

Delete a connection and its cached data.

### Example


```python
import hotdata
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | Connection ID

    try:
        # Delete connection
        api_instance.delete_connection_handler(connection_id)
    except Exception as e:
        print("Exception when calling ConnectionsApi->delete_connection_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Connection deleted |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connection_handler**
> GetConnectionResponse get_connection_handler(connection_id)

Get connection

Get details for a specific connection, including table and sync counts.

### Example


```python
import hotdata
from hotdata.models.get_connection_response import GetConnectionResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | Connection ID

    try:
        # Get connection
        api_response = api_instance.get_connection_handler(connection_id)
        print("The response of ConnectionsApi->get_connection_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->get_connection_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 

### Return type

[**GetConnectionResponse**](GetConnectionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Connection details |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_table_profile_handler**
> TableProfileResponse get_table_profile_handler(connection_id, var_schema, table)

Get table profile

Get column-level statistics for a synced table. Returns per-column profiles including cardinality, null counts, and type-specific details (distinct values for categorical columns, min/max for temporal/numeric, length stats for text). Profiles are computed at sync time.

### Example


```python
import hotdata
from hotdata.models.table_profile_response import TableProfileResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
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
        api_response = api_instance.get_table_profile_handler(connection_id, var_schema, table)
        print("The response of ConnectionsApi->get_table_profile_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->get_table_profile_handler: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Column profile statistics |  -  |
**404** | Table or profile not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_connections_handler**
> ListConnectionsResponse list_connections_handler()

List connections

List all registered database connections.

### Example


```python
import hotdata
from hotdata.models.list_connections_response import ListConnectionsResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.ConnectionsApi(api_client)

    try:
        # List connections
        api_response = api_instance.list_connections_handler()
        print("The response of ConnectionsApi->list_connections_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->list_connections_handler: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListConnectionsResponse**](ListConnectionsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of connections |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **purge_connection_cache_handler**
> purge_connection_cache_handler(connection_id)

Purge connection cache

Purge all cached data for a connection. The next query against these tables will trigger a fresh sync from the remote source.

### Example


```python
import hotdata
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | Connection ID

    try:
        # Purge connection cache
        api_instance.purge_connection_cache_handler(connection_id)
    except Exception as e:
        print("Exception when calling ConnectionsApi->purge_connection_cache_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Connection ID | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Cache purged |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **purge_table_cache_handler**
> purge_table_cache_handler(connection_id, var_schema, table)

Purge table cache

Purge the cached data for a single table. The next query will trigger a fresh sync.

### Example


```python
import hotdata
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
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
        api_instance.purge_table_cache_handler(connection_id, var_schema, table)
    except Exception as e:
        print("Exception when calling ConnectionsApi->purge_table_cache_handler: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Table cache purged |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

