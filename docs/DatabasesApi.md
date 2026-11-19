# hotdata.DatabasesApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_database_schema**](DatabasesApi.md#add_database_schema) | **POST** /v1/databases/{database_id}/schemas | Add schema to database default catalog
[**add_database_table**](DatabasesApi.md#add_database_table) | **POST** /v1/databases/{database_id}/schemas/{schema}/tables | Add table to database default catalog
[**attach_database_catalog**](DatabasesApi.md#attach_database_catalog) | **POST** /v1/databases/{database_id}/catalogs | Attach catalog to database
[**bulk_create_databases**](DatabasesApi.md#bulk_create_databases) | **POST** /v1/databases/bulk | Create many databases at once
[**count_databases**](DatabasesApi.md#count_databases) | **GET** /v1/databases/count | Count databases
[**create_database**](DatabasesApi.md#create_database) | **POST** /v1/databases | Create database
[**delete_database**](DatabasesApi.md#delete_database) | **DELETE** /v1/databases/{database_id} | Delete database
[**delete_database_batch**](DatabasesApi.md#delete_database_batch) | **DELETE** /v1/databases/bulk/{batch_id} | Delete a database batch
[**detach_database_catalog**](DatabasesApi.md#detach_database_catalog) | **DELETE** /v1/databases/{database_id}/catalogs/{connection_id} | Detach catalog from database
[**fork_database**](DatabasesApi.md#fork_database) | **POST** /v1/databases/{database_id}/fork | Fork database
[**get_database**](DatabasesApi.md#get_database) | **GET** /v1/databases/{database_id} | Get database
[**get_database_batch**](DatabasesApi.md#get_database_batch) | **GET** /v1/databases/bulk/{batch_id} | Get a database batch
[**get_database_lineage**](DatabasesApi.md#get_database_lineage) | **GET** /v1/databases/{database_id}/lineage | Get database lineage
[**list_databases**](DatabasesApi.md#list_databases) | **GET** /v1/databases | List databases
[**load_database_table**](DatabasesApi.md#load_database_table) | **POST** /v1/databases/{database_id}/schemas/{schema}/tables/{table}/loads | Load database table from inline data, upload, or query result
[**lookup_database_by_name**](DatabasesApi.md#lookup_database_by_name) | **GET** /v1/databases/by-name | Look up a database by name
[**set_database_table_constant_per_key**](DatabasesApi.md#set_database_table_constant_per_key) | **PUT** /v1/databases/{database_id}/schemas/{schema}/tables/{table}/constant-per-key | Declare which columns are constant per key


# **add_database_schema**
> ManagedSchemaResponse add_database_schema(database_id, add_managed_schema_request)

Add schema to database default catalog

Add a schema, and optionally its tables, to the database's `default` catalog. Names are stored in lowercase.

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

Add an empty table to a schema in the database's `default` catalog. Names are stored in lowercase. You do not have to declare tables first: a load creates the table if it is missing.

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

Attach a catalog so its tables can be queried in this database. To query across two databases, pass the other database's `default_connection_id` as `connection_id`.

The catalog is read-only here and nothing is copied. It answers to `alias`, or to its own name if you omit it. That name cannot be `default` or a reserved name, so attaching another database's `default` catalog needs an `alias`. Attaching is not transitive: you do not see the attached catalog's own attachments.

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
**409** | The catalog is already attached, or the alias is already in use |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **bulk_create_databases**
> DatabaseBatchResponse bulk_create_databases(bulk_create_databases_request)

Create many databases at once

Create many databases from one template, in the background. The response returns at once with a `batch_id` and a job to poll.

Pass `schemas` to declare the same tables in every database. List the databases a batch created with `GET /v1/databases?batch=<batch_id>`.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.bulk_create_databases_request import BulkCreateDatabasesRequest
from hotdata.models.database_batch_response import DatabaseBatchResponse
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
    bulk_create_databases_request = hotdata.BulkCreateDatabasesRequest() # BulkCreateDatabasesRequest | 

    try:
        # Create many databases at once
        api_response = api_instance.bulk_create_databases(bulk_create_databases_request)
        print("The response of DatabasesApi->bulk_create_databases:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->bulk_create_databases: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bulk_create_databases_request** | [**BulkCreateDatabasesRequest**](BulkCreateDatabasesRequest.md)|  | 

### Return type

[**DatabaseBatchResponse**](DatabaseBatchResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Batch accepted. Databases are created in the background. |  -  |
**400** | Invalid count, template, or expiry |  -  |
**409** | A batch with this idempotency key is already running |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **count_databases**
> DatabaseCountResponse count_databases(search=search, batch=batch)

Count databases

Count the databases in the workspace. `search` and `batch` filter the same way as on `GET /v1/databases`.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.database_count_response import DatabaseCountResponse
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
    search = 'search_example' # str | Count only databases whose name contains this text, ignoring case. (optional)
    batch = 'batch_example' # str | Count only databases from this bulk-create batch. (optional)

    try:
        # Count databases
        api_response = api_instance.count_databases(search=search, batch=batch)
        print("The response of DatabasesApi->count_databases:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->count_databases: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search** | **str**| Count only databases whose name contains this text, ignoring case. | [optional] 
 **batch** | **str**| Count only databases from this bulk-create batch. | [optional] 

### Return type

[**DatabaseCountResponse**](DatabaseCountResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Number of matching databases |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_database**
> CreateDatabaseResponse create_database(create_database_request)

Create database

Create a database. Each database gets its own `default` catalog with a `main` schema, so `default.main.<table>` works right away. You can declare more schemas and tables in `schemas`.

`name` is a label and does not have to be unique. Set `if_not_exists` to get back the database that already has this `name` (status 200) instead of creating a new one; the rest of the request is then ignored. Set `expires_at` to have the database deleted after that time. Deletion never happens earlier, but can happen later.

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
**200** | &#x60;if_not_exists&#x60; was set and a database with this &#x60;name&#x60; already exists. It is returned unchanged. |  -  |
**201** | Database created |  -  |
**400** | Invalid request |  -  |
**409** | &#x60;if_not_exists&#x60; was set and more than one database has this &#x60;name&#x60;. |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_database**
> delete_database(database_id)

Delete database

Delete a database and its `default` catalog. Catalogs attached to it are detached, not deleted.

Returns 409 while another database has this database's catalog attached; detach it there first. After `expires_at` the database is deleted anyway, and the other database loses access.

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
**409** | Another database has this database&#39;s catalog attached |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_database_batch**
> DeleteDatabaseBatchResponse delete_database_batch(batch_id)

Delete a database batch

Stop a batch and delete the databases it created, then the batch.

This works only while no database in the batch holds loaded data. Declared but unloaded tables are fine. If any database has data, the request returns 409; delete those databases one at a time.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.delete_database_batch_response import DeleteDatabaseBatchResponse
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
    batch_id = 'batch_id_example' # str | Batch ID

    try:
        # Delete a database batch
        api_response = api_instance.delete_database_batch(batch_id)
        print("The response of DatabasesApi->delete_database_batch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->delete_database_batch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **batch_id** | **str**| Batch ID | 

### Return type

[**DeleteDatabaseBatchResponse**](DeleteDatabaseBatchResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Batch deleted |  -  |
**404** | Batch not found |  -  |
**409** | Some databases in the batch hold loaded data |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **detach_database_catalog**
> detach_database_catalog(database_id, connection_id)

Detach catalog from database

Detach a catalog from a database. The catalog and its data are not deleted.

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

Create a new database that starts as a copy of an existing one: same schemas, tables, data and attached catalogs. The two are independent after that; the source does not change.

Indexes come across and work at once, except vector indexes that use the `ivf` algorithm and indexes not up to date with the table's latest load. Create those again on the fork. A fork shares the source's storage at first, so it adds no stored bytes until it is written to or maintenance rewrites a table.

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
**400** | The source database cannot be forked |  -  |
**404** | Source database not found |  -  |
**409** | The source database changed during the fork. Retry the request. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_database**
> DatabaseDetailResponse get_database(database_id)

Get database

Get a database by ID. To find one by name, use `GET /v1/databases/by-name`.

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

# **get_database_batch**
> DatabaseBatchResponse get_database_batch(batch_id)

Get a database batch

Get a batch: how many databases were requested and how many exist so far. Poll this to follow progress.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.database_batch_response import DatabaseBatchResponse
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
    batch_id = 'batch_id_example' # str | Batch ID

    try:
        # Get a database batch
        api_response = api_instance.get_database_batch(batch_id)
        print("The response of DatabasesApi->get_database_batch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->get_database_batch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **batch_id** | **str**| Batch ID | 

### Return type

[**DatabaseBatchResponse**](DatabaseBatchResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The batch |  -  |
**404** | Batch not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_database_lineage**
> DatabaseLineageResponse get_database_lineage(database_id, forks_limit=forks_limit)

Get database lineage

Show where a database was forked from and what was forked from it.

`ancestors` lists the fork chain up to the original, nearest first. `forks` lists databases forked directly from this one, newest first; `fork_count` is the full total when the list is cut short. Deleted databases stay in the record with `exists` set to false. A database with no forks returns empty lists and itself as `root_id`.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.database_lineage_response import DatabaseLineageResponse
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
    forks_limit = 56 # int | Number of direct forks to list, 1 to 100. Defaults to 25. (optional)

    try:
        # Get database lineage
        api_response = api_instance.get_database_lineage(database_id, forks_limit=forks_limit)
        print("The response of DatabasesApi->get_database_lineage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->get_database_lineage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
 **forks_limit** | **int**| Number of direct forks to list, 1 to 100. Defaults to 25. | [optional] 

### Return type

[**DatabaseLineageResponse**](DatabaseLineageResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Database lineage |  -  |
**404** | Database not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_databases**
> ListDatabasesResponse list_databases(limit=limit, cursor=cursor, search=search, batch=batch)

List databases

List databases, newest first, one page at a time. If `has_more` is true, pass `next_cursor` as `cursor` to get the next page.

`search` matches names that contain the text. To get the one database with an exact name, use `GET /v1/databases/by-name`. `batch` lists only the databases a bulk create made.

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
    limit = 56 # int | Databases per page, 1 to 100. Defaults to 100. (optional)
    cursor = 'cursor_example' # str | `next_cursor` from the previous page. (optional)
    search = 'search_example' # str | Return only databases whose name contains this text, ignoring case. (optional)
    batch = 'batch_example' # str | Return only databases from this bulk-create batch, ordered by ID. (optional)

    try:
        # List databases
        api_response = api_instance.list_databases(limit=limit, cursor=cursor, search=search, batch=batch)
        print("The response of DatabasesApi->list_databases:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->list_databases: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Databases per page, 1 to 100. Defaults to 100. | [optional] 
 **cursor** | **str**| &#x60;next_cursor&#x60; from the previous page. | [optional] 
 **search** | **str**| Return only databases whose name contains this text, ignoring case. | [optional] 
 **batch** | **str**| Return only databases from this bulk-create batch, ordered by ID. | [optional] 

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

Load database table from inline data, upload, or query result

Load data into a table in the database's `default` catalog. Give exactly one source: `data` (inline CSV, up to 2 MiB), `upload_id` (a CSV, JSON or Parquet file from `POST /v1/uploads`) or `result_id` (a saved query result). The table and its schema are created if they do not exist. `mode` sets how the rows apply.

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
    api_instance = hotdata.DatabasesApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    var_schema = 'var_schema_example' # str | Schema name
    table = 'table_example' # str | Table name
    load_managed_table_request = {mode=replace, data=order_id,customer_id,amount
1001,42,1999
1002,7,4550
, format=csv, columns={order_id=BIGINT, customer_id=BIGINT, amount={type=DECIMAL, precision=10, scale=2}}} # LoadManagedTableRequest | 

    try:
        # Load database table from inline data, upload, or query result
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
**202** | The load is running in the background. Poll the returned job. |  -  |
**400** | Invalid request, such as a bad &#x60;mode&#x60;, not exactly one data source, data that cannot be parsed, or a result that failed to compute |  -  |
**404** | Database, upload, or result not found, or the table was deleted |  -  |
**409** | Conflict: the upload was already used or is in use, the result is not ready, or the data changes a column&#39;s type in a way that cannot be widened. The table is unchanged. With &#x60;RESOURCE_LOCKED&#x60;, another write holds the table; retry after the &#x60;Retry-After&#x60; delay. |  -  |
**413** | Inline &#x60;data&#x60; is over 2 MiB (&#x60;INLINE_DATA_TOO_LARGE&#x60;). Upload the file and load it by &#x60;upload_id&#x60;. |  -  |
**503** | The catalog is busy (&#x60;CATALOG_BUSY&#x60;). The load may already have written its data, so check the table or use an idempotency key before you retry after the &#x60;Retry-After&#x60; delay. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **lookup_database_by_name**
> DatabaseDetailResponse lookup_database_by_name(name)

Look up a database by name

Get the database with this exact name. Matching ignores case only for unaccented Latin letters; all other characters must match exactly.

Returns 409 if more than one database has the name. Use the database ID for those.

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
    name = 'name_example' # str | Full name of the database. Case is ignored for ASCII letters only.

    try:
        # Look up a database by name
        api_response = api_instance.lookup_database_by_name(name)
        print("The response of DatabasesApi->lookup_database_by_name:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->lookup_database_by_name: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Full name of the database. Case is ignored for ASCII letters only. | 

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
**400** | The &#x60;name&#x60; parameter is empty or too long |  -  |
**404** | No database has that name |  -  |
**409** | More than one database has that name |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_database_table_constant_per_key**
> ManagedTableConstantPerKeyResponse set_database_table_constant_per_key(database_id, var_schema, table, update_managed_table_request)

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
    api_instance = hotdata.DatabasesApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    var_schema = 'var_schema_example' # str | Schema name
    table = 'table_example' # str | Table name
    update_managed_table_request = hotdata.UpdateManagedTableRequest() # UpdateManagedTableRequest | 

    try:
        # Declare which columns are constant per key
        api_response = api_instance.set_database_table_constant_per_key(database_id, var_schema, table, update_managed_table_request)
        print("The response of DatabasesApi->set_database_table_constant_per_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatabasesApi->set_database_table_constant_per_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
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
**400** | An invalid column name, or a table with no key |  -  |
**404** | Database, schema or table not found |  -  |
**409** | The setting changed at the same time. Retry. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

