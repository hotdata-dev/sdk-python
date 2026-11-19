# hotdata.RollupsApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**declare_rollup**](RollupsApi.md#declare_rollup) | **POST** /v1/databases/{database_id}/rollups | Declare a rollup on a table
[**drop_rollup**](RollupsApi.md#drop_rollup) | **DELETE** /v1/databases/{database_id}/rollups/{rollup_id} | Drop a rollup
[**get_rollup**](RollupsApi.md#get_rollup) | **GET** /v1/databases/{database_id}/rollups/{rollup_id} | Get a rollup
[**list_rollups**](RollupsApi.md#list_rollups) | **GET** /v1/databases/{database_id}/rollups | List a database&#39;s rollups
[**rebuild_rollup**](RollupsApi.md#rebuild_rollup) | **POST** /v1/databases/{database_id}/rollups/{rollup_id}/rebuild | Rebuild a rollup
[**set_rollup_window**](RollupsApi.md#set_rollup_window) | **PUT** /v1/databases/{database_id}/rollups/{rollup_id}/window | Set a rollup&#39;s window


# **declare_rollup**
> RollupBuildResponse declare_rollup(database_id, declare_rollup_request)

Declare a rollup on a table

Declare a rollup: pre-aggregated rows of one table, one per time bucket and set of dimension values, which answer matching aggregate queries without reading the whole table. Answers are the same as reading the table. The table must hold data, and its time column must be a timestamp with no time zone or in UTC.

The rollup starts as `building` and becomes `ready` when its build catches up with the table; poll the returned job or the rollup. When `job_id` is null the build could not be started: rebuild the rollup to start it.

A query uses a ready rollup when it aggregates with `count`, `sum`, `avg`, `min`, `max`, or `approx_percentile_cont` / `approx_median` at the declared `centroids` (approximate answers only); groups by the time column in buckets that are a multiple of `bucket_width_secs`, and by dimensions; filters only on dimensions and the time column; and, when the rollup has a `filter`, contains each of its `AND`-joined parts written the same way. `min` and `max` of a floating-point column are always read from the table. The query's response says whether a rollup was used.

Declaring a rollup changes how the table can be written. Rows whose time is older than `window_secs` can no longer be changed or deleted, and SQL `DELETE` and `UPDATE` on the table are refused: change rows with a keyed load whose key includes the time column. Appends are always allowed, and so is replacing the table, after which its rollups need a rebuild and queries read the table until then. A fork of the database does not carry rollups, and dropping the table drops them. A rollup cannot be changed: drop it and declare a new one, which builds from the start.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.declare_rollup_request import DeclareRollupRequest
from hotdata.models.rollup_build_response import RollupBuildResponse
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
    api_instance = hotdata.RollupsApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    declare_rollup_request = hotdata.DeclareRollupRequest() # DeclareRollupRequest | 

    try:
        # Declare a rollup on a table
        api_response = api_instance.declare_rollup(database_id, declare_rollup_request)
        print("The response of RollupsApi->declare_rollup:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RollupsApi->declare_rollup: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
 **declare_rollup_request** | [**DeclareRollupRequest**](DeclareRollupRequest.md)|  | 

### Return type

[**RollupBuildResponse**](RollupBuildResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The rollup was declared |  -  |
**400** | The declaration does not fit the table |  -  |
**404** | No such database or table |  -  |
**409** | An identical rollup already exists, or the table&#39;s window differs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **drop_rollup**
> drop_rollup(database_id, rollup_id)

Drop a rollup

Drop a rollup and its rows. The table does not change. Returns once the rollup is gone, which can take up to two minutes when a build step is running on it. When the last rollup on a table is dropped, the table's write window no longer applies.

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
    api_instance = hotdata.RollupsApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    rollup_id = 'rollup_id_example' # str | Rollup ID

    try:
        # Drop a rollup
        api_instance.drop_rollup(database_id, rollup_id)
    except Exception as e:
        print("Exception when calling RollupsApi->drop_rollup: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
 **rollup_id** | **str**| Rollup ID | 

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
**204** | The rollup was dropped |  -  |
**404** | No such database or rollup |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_rollup**
> Rollup get_rollup(database_id, rollup_id)

Get a rollup

Get a rollup: its definition, its status, and how far its build has come.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.rollup import Rollup
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
    api_instance = hotdata.RollupsApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    rollup_id = 'rollup_id_example' # str | Rollup ID

    try:
        # Get a rollup
        api_response = api_instance.get_rollup(database_id, rollup_id)
        print("The response of RollupsApi->get_rollup:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RollupsApi->get_rollup: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
 **rollup_id** | **str**| Rollup ID | 

### Return type

[**Rollup**](Rollup.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The rollup |  -  |
**404** | No such database or rollup |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_rollups**
> ListRollupsResponse list_rollups(database_id, schema_name=schema_name, table_name=table_name)

List a database's rollups

List the rollups on a database's tables. Filter by schema, or by schema and table.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_rollups_response import ListRollupsResponse
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
    api_instance = hotdata.RollupsApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    schema_name = 'schema_name_example' # str | Only rollups on tables of this schema (optional)
    table_name = 'table_name_example' # str | Only rollups on this table; requires `schema_name` (optional)

    try:
        # List a database's rollups
        api_response = api_instance.list_rollups(database_id, schema_name=schema_name, table_name=table_name)
        print("The response of RollupsApi->list_rollups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RollupsApi->list_rollups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
 **schema_name** | **str**| Only rollups on tables of this schema | [optional] 
 **table_name** | **str**| Only rollups on this table; requires &#x60;schema_name&#x60; | [optional] 

### Return type

[**ListRollupsResponse**](ListRollupsResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The rollups |  -  |
**400** | &#x60;table_name&#x60; without &#x60;schema_name&#x60; |  -  |
**404** | No such database |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **rebuild_rollup**
> RollupBuildResponse rebuild_rollup(database_id, rollup_id)

Rebuild a rollup

Start building a rollup again, in the background, and return the build job. A `needs_rebuild` rollup (left that way when its table is replaced) is emptied and rebuilt; queries read the table until the build finishes. A `build_failed` rollup, or a `building` one whose build is not running, resumes where it stopped.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.rollup_build_response import RollupBuildResponse
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
    api_instance = hotdata.RollupsApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    rollup_id = 'rollup_id_example' # str | Rollup ID

    try:
        # Rebuild a rollup
        api_response = api_instance.rebuild_rollup(database_id, rollup_id)
        print("The response of RollupsApi->rebuild_rollup:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RollupsApi->rebuild_rollup: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
 **rollup_id** | **str**| Rollup ID | 

### Return type

[**RollupBuildResponse**](RollupBuildResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | The build was started |  -  |
**404** | No such database or rollup |  -  |
**409** | The rollup is ready, is being dropped, or is already being built |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_rollup_window**
> Rollup set_rollup_window(database_id, rollup_id, set_rollup_window_request)

Set a rollup's window

Set how long after a row's time it can still be changed or deleted. This applies to every rollup on the same table. Appends are always allowed. Nothing is rebuilt: a wider window applies as time passes, and a narrower one at the next refresh.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.rollup import Rollup
from hotdata.models.set_rollup_window_request import SetRollupWindowRequest
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
    api_instance = hotdata.RollupsApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    rollup_id = 'rollup_id_example' # str | Rollup ID
    set_rollup_window_request = hotdata.SetRollupWindowRequest() # SetRollupWindowRequest | 

    try:
        # Set a rollup's window
        api_response = api_instance.set_rollup_window(database_id, rollup_id, set_rollup_window_request)
        print("The response of RollupsApi->set_rollup_window:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RollupsApi->set_rollup_window: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
 **rollup_id** | **str**| Rollup ID | 
 **set_rollup_window_request** | [**SetRollupWindowRequest**](SetRollupWindowRequest.md)|  | 

### Return type

[**Rollup**](Rollup.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The rollup, with its new window |  -  |
**400** | The window is zero or too large |  -  |
**404** | No such database or rollup |  -  |
**409** | The rollup is being dropped, or its table was replaced |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

