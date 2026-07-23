# hotdata.DatabasesApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_database_schema**](DatabasesApi.md#add_database_schema) | **POST** /v1/databases/{database_id}/schemas | Add schema to database default catalog
[**add_database_table**](DatabasesApi.md#add_database_table) | **POST** /v1/databases/{database_id}/schemas/{schema}/tables | Add table to database default catalog
[**attach_database_catalog**](DatabasesApi.md#attach_database_catalog) | **POST** /v1/databases/{database_id}/catalogs | Attach catalog to database
[**create_database**](DatabasesApi.md#create_database) | **POST** /v1/databases | Create database
[**delete_database**](DatabasesApi.md#delete_database) | **DELETE** /v1/databases/{database_id} | Delete database
[**detach_database_catalog**](DatabasesApi.md#detach_database_catalog) | **DELETE** /v1/databases/{database_id}/catalogs/{connection_id} | Detach catalog from database
[**fork_database**](DatabasesApi.md#fork_database) | **POST** /v1/databases/{database_id}/fork | Fork database
[**get_database**](DatabasesApi.md#get_database) | **GET** /v1/databases/{database_id} | Get database
[**list_databases**](DatabasesApi.md#list_databases) | **GET** /v1/databases | List databases
[**load_database_table**](DatabasesApi.md#load_database_table) | **POST** /v1/databases/{database_id}/schemas/{schema}/tables/{table}/loads | Load database table from upload or query result


# **add_database_schema**
> ManagedSchemaResponse add_database_schema(database_id, add_managed_schema_request)

Add schema to database default catalog

Declare a new schema (and optionally its tables) on the database's auto-created default catalog after creation. The schema becomes reachable inside the database scope (e.g. `default.<schema>.<table>` and `information_schema.schemata`) without the caller addressing the internal default connection directly. Identifiers are normalized to lowercase.

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
    api_instance = hotdata.DatabasesApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    add_managed_schema_request = hotdata.AddManagedSchemaRequest() # AddManagedSchemaRequest | 

    try:
        # Add schema to database default catalog
        api_response = api_instance.add_database_schema(database_id, add_managed_schema_request)
        print("The response of DatabasesApi->add_database_schema:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->add_database_schema: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
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
**400** | Invalid identifier |  -  |
**404** | Database not found |  -  |
**409** | Schema already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_database_table**
> ManagedTableResponse add_database_table(database_id, var_schema, add_managed_table_request)

Add table to database default catalog

Declare a new table on an existing schema of the database's default catalog after creation. The table is added empty (declared-but-unloaded) and can be populated via the managed-table load endpoint targeting the default connection. Identifiers are normalized to lowercase.

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
    api_instance = hotdata.DatabasesApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    var_schema = 'var_schema_example' # str | Schema name
    add_managed_table_request = hotdata.AddManagedTableRequest() # AddManagedTableRequest | 

    try:
        # Add table to database default catalog
        api_response = api_instance.add_database_table(database_id, var_schema, add_managed_table_request)
        print("The response of DatabasesApi->add_database_table:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->add_database_table: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
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
**400** | Invalid identifier |  -  |
**404** | Database or schema not found |  -  |
**409** | Table already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **attach_database_catalog**
> attach_database_catalog(database_id, attach_database_catalog_request)

Attach catalog to database

Attach an existing connection (catalog) to a database with an optional alias. Inside the database the catalog is reachable as the alias (when set) or its original name.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.attach_database_catalog_request import AttachDatabaseCatalogRequest
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
    api_instance = hotdata.DatabasesApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    attach_database_catalog_request = hotdata.AttachDatabaseCatalogRequest() # AttachDatabaseCatalogRequest | 

    try:
        # Attach catalog to database
        api_instance.attach_database_catalog(database_id, attach_database_catalog_request)
    except Exception as e:
        print("Exception when calling DatabasesApi->attach_database_catalog: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
 **attach_database_catalog_request** | [**AttachDatabaseCatalogRequest**](AttachDatabaseCatalogRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Catalog attached |  -  |
**400** | Invalid request |  -  |
**404** | Database or connection not found |  -  |
**409** | Catalog already attached or alias collides with an existing attachment |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_database**
> CreateDatabaseResponse create_database(create_database_request)

Create database

Create a new database (a metadata-only grouping). A managed default catalog is auto-created and addressable inside the database as `default` (or the optional `default_catalog` name), with a `main` schema pre-declared so `default.main.<table>` works out of the box. The optional `name` is a free-form display label and is not required to be unique. Optional `default_catalog` overrides the name the default catalog answers to; it must be a valid SQL identifier and may not collide with the reserved catalog names `hotdata` or `information_schema`. Optional `schemas` declares additional schemas/tables on the default catalog at create time; declared tables can be loaded via the standard managed-tables-load endpoint targeting `default_connection_id`. Optional `expires_at` sets when the database expires — accepts either an RFC 3339 timestamp or a relative duration suffixed with `h` (hours), `m` (minutes), or `d` (days), e.g. `24h`, `48h`, `90m`, `7d`. When omitted, the database never expires. Expiry is best-effort: the database will not be deleted before `expires_at`, but cleanup may run later than the exact timestamp.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.create_database_request import CreateDatabaseRequest
from hotdata.models.create_database_response import CreateDatabaseResponse
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
    api_instance = hotdata.DatabasesApi(api_client)
    create_database_request = hotdata.CreateDatabaseRequest() # CreateDatabaseRequest | 

    try:
        # Create database
        api_response = api_instance.create_database(create_database_request)
        print("The response of DatabasesApi->create_database:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->create_database: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_database_request** | [**CreateDatabaseRequest**](CreateDatabaseRequest.md)|  | 

### Return type

[**CreateDatabaseResponse**](CreateDatabaseResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Database created |  -  |
**400** | Invalid request |  -  |
**500** | Internal server error (e.g., managed-connection create succeeded but database row insert + rollback both failed) |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_database**
> delete_database(database_id)

Delete database

Delete a database and its auto-created default catalog. Attached catalogs are detached (their underlying connections are not deleted).

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
    api_instance = hotdata.DatabasesApi(api_client)
    database_id = 'database_id_example' # str | Database ID

    try:
        # Delete database
        api_instance.delete_database(database_id)
    except Exception as e:
        print("Exception when calling DatabasesApi->delete_database: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 

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
**204** | Database deleted |  -  |
**404** | Database not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **detach_database_catalog**
> detach_database_catalog(database_id, connection_id)

Detach catalog from database

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
    api_instance = hotdata.DatabasesApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    connection_id = 'connection_id_example' # str | Connection ID

    try:
        # Detach catalog from database
        api_instance.detach_database_catalog(database_id, connection_id)
    except Exception as e:
        print("Exception when calling DatabasesApi->detach_database_catalog: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
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
**204** | Catalog detached |  -  |
**400** | Cannot detach a database&#39;s own default catalog |  -  |
**404** | Database or attachment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fork_database**
> CreateDatabaseResponse fork_database(database_id, fork_database_request)

Fork database

Create a new database that is an independent fork of an existing one. The fork has its own default catalog and contains the same schemas, tables, and data as the source; the source is left unchanged. External catalogs attached to the source are re-attached to the fork. Optional `name` sets the fork's display label (defaults to the source's). Optional `expires_at` sets when the fork expires — accepts an RFC 3339 timestamp or a relative duration suffixed with `h` (hours), `m` (minutes), or `d` (days), e.g. `24h`, `90m`, `7d`. When omitted, a still-future expiry on the source is carried over; otherwise the fork never expires. Any indexes on the source's tables are not carried over.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.create_database_response import CreateDatabaseResponse
from hotdata.models.fork_database_request import ForkDatabaseRequest
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
    api_instance = hotdata.DatabasesApi(api_client)
    database_id = 'database_id_example' # str | Source database ID
    fork_database_request = hotdata.ForkDatabaseRequest() # ForkDatabaseRequest | 

    try:
        # Fork database
        api_response = api_instance.fork_database(database_id, fork_database_request)
        print("The response of DatabasesApi->fork_database:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->fork_database: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Source database ID | 
 **fork_database_request** | [**ForkDatabaseRequest**](ForkDatabaseRequest.md)|  | 

### Return type

[**CreateDatabaseResponse**](CreateDatabaseResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Database forked |  -  |
**400** | The source database can&#39;t be forked as-is (for example, it uses a storage backend that does not support forking, or one of its tables has rows that were individually deleted or updated) |  -  |
**404** | Source database not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_database**
> DatabaseDetailResponse get_database(database_id)

Get database

Fetch a database by id. The `name` field is a display label only; it is not accepted as an identifier here.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.database_detail_response import DatabaseDetailResponse
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
    api_instance = hotdata.DatabasesApi(api_client)
    database_id = 'database_id_example' # str | Database ID

    try:
        # Get database
        api_response = api_instance.get_database(database_id)
        print("The response of DatabasesApi->get_database:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->get_database: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 

### Return type

[**DatabaseDetailResponse**](DatabaseDetailResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Database details |  -  |
**404** | Database not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_databases**
> ListDatabasesResponse list_databases(limit=limit, cursor=cursor)

List databases

List databases in the workspace, newest first, one page at a time. When no `limit` is given a default page size is applied, so a single call returns at most one page rather than every database. If the response's `has_more` is true, pass its `next_cursor` value back as the `cursor` query parameter to fetch the next page.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_databases_response import ListDatabasesResponse
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
    api_instance = hotdata.DatabasesApi(api_client)
    limit = 56 # int | Maximum number of databases to return in this page (1–100). Values outside the range are clamped. (optional)
    cursor = 'cursor_example' # str | Opaque pagination cursor from a previous response's `next_cursor`. (optional)

    try:
        # List databases
        api_response = api_instance.list_databases(limit=limit, cursor=cursor)
        print("The response of DatabasesApi->list_databases:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->list_databases: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of databases to return in this page (1–100). Values outside the range are clamped. | [optional] 
 **cursor** | **str**| Opaque pagination cursor from a previous response&#39;s &#x60;next_cursor&#x60;. | [optional] 

### Return type

[**ListDatabasesResponse**](ListDatabasesResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | One page of databases |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **load_database_table**
> LoadManagedTableResponse load_database_table(database_id, var_schema, table, load_managed_table_request)

Load database table from upload or query result

Publish data as the new contents of a table on the database's default catalog, from one of two sources — provide exactly one. The database-scoped equivalent of the connection-scoped managed-table load — addressed by `database_id`, so no `default_connection_id` is needed. With `upload_id`, a previously-uploaded file is published: CSV, JSON, and Parquet are supported; the format is auto-detected or set via `format`. With `result_id`, a persisted query result is copied into the table, so the table keeps its data even after the result expires. If the target table (or its schema) has not been declared yet, it is created automatically as part of the load — declaring tables up front is optional. `mode` selects how the data is applied: `replace` overwrites the table's contents, `append` inserts the new rows on top of the existing data. Concurrent loads against the same upload return 409. For an upload, set `async` to run the load in the background and get back a job ID to poll; add `async_after_ms` to wait briefly for it to finish before falling back to a job ID. A `result_id` load runs synchronously.

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
    api_instance = hotdata.DatabasesApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    var_schema = 'var_schema_example' # str | Schema name
    table = 'table_example' # str | Table name
    load_managed_table_request = hotdata.LoadManagedTableRequest() # LoadManagedTableRequest | 

    try:
        # Load database table from upload or query result
        api_response = api_instance.load_database_table(database_id, var_schema, table, load_managed_table_request)
        print("The response of DatabasesApi->load_database_table:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->load_database_table: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
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
**200** | Table loaded |  -  |
**202** | Upload load accepted and running in the background; poll the returned job for status and result |  -  |
**400** | Invalid request (bad mode, both or neither of &#x60;upload_id&#x60;/&#x60;result_id&#x60;, &#x60;format&#x60; combined with &#x60;result_id&#x60;, invalid identifier, bad parquet, or the result failed to compute) |  -  |
**404** | Database, upload, or result not found, or the table was deleted |  -  |
**409** | Upload already consumed or in flight, the result is still being computed, or the incoming data changes a column&#39;s type incompatibly (only widening to a larger compatible type can be applied automatically); the existing data is unchanged and remains queryable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

