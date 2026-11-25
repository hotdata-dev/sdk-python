# hotdata.StreamsApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_stream_handler**](StreamsApi.md#create_stream_handler) | **POST** /v1/databases/{database_id}/streams | Create a stream
[**delete_stream_handler**](StreamsApi.md#delete_stream_handler) | **DELETE** /v1/streams/{stream_id} | Delete a stream
[**get_stream_handler**](StreamsApi.md#get_stream_handler) | **GET** /v1/streams/{stream_id} | Get a stream
[**ingest_stream_handler**](StreamsApi.md#ingest_stream_handler) | **POST** /v1/streams/{stream_id}/spans/ingest/sync | Append rows to a stream


# **create_stream_handler**
> StreamResponse create_stream_handler(database_id, create_stream_request)

Create a stream

Create a stream: a table you post span or log rows to without declaring its columns. The first request sets the columns from its rows. Each key becomes a column typed from its values, and each key inside an object field also gets its own `field.key` column. Use `columns` to set a column's type or role in advance.

The table is partitioned by day of its time column. With no `time_column`, Hotdata adds `_ingested_at` and sets it to the time each request arrives. The stream's status is `waiting_for_data` until the first request. Streams are available only where they are enabled.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.create_stream_request import CreateStreamRequest
from hotdata.models.stream_response import StreamResponse
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
    api_instance = hotdata.StreamsApi(api_client)
    database_id = 'database_id_example' # str | Database ID
    create_stream_request = hotdata.CreateStreamRequest() # CreateStreamRequest | 

    try:
        # Create a stream
        api_response = api_instance.create_stream_handler(database_id, create_stream_request)
        print("The response of StreamsApi->create_stream_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StreamsApi->create_stream_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **database_id** | **str**| Database ID | 
 **create_stream_request** | [**CreateStreamRequest**](CreateStreamRequest.md)|  | 

### Return type

[**StreamResponse**](StreamResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Stream created |  -  |
**400** | Invalid table name, time column, time unit or column hint |  -  |
**404** | Database not found, or streams are not enabled |  -  |
**409** | A table of that name already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_stream_handler**
> delete_stream_handler(stream_id)

Delete a stream

Delete a stream, its table and all its rows, including rows not stored yet. Requests to the stream return 404 as soon as the delete starts. When it finishes, the table name can be used again. If the delete fails, retry it.

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
    api_instance = hotdata.StreamsApi(api_client)
    stream_id = 'stream_id_example' # str | Stream ID

    try:
        # Delete a stream
        api_instance.delete_stream_handler(stream_id)
    except Exception as e:
        print("Exception when calling StreamsApi->delete_stream_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **stream_id** | **str**| Stream ID | 

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
**204** | Stream deleted |  -  |
**403** | The API key is limited to another database |  -  |
**404** | Stream not found, or streams are not enabled |  -  |
**409** | The stream&#39;s table is busy. Retry shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_stream_handler**
> StreamResponse get_stream_handler(stream_id)

Get a stream

Get a stream: its table, status, time column and column hints. After the first request, it also lists each column with its type and role: `time`, `large_text`, `normal`, `map_key` or `extra`.

A `map_key` column holds one key of an object field; `from` names the field and key. The `_extra` column keeps, as JSON text, any field that has no column and any value of the wrong type for its column. `pending_bytes` and `oldest_pending_age_ms` describe accepted rows that the answering server has not stored yet; both are null when it holds none. `id_index_up_to_date` says whether every stored row is indexed for each ID column the server indexes; it is omitted when the server does not index IDs.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.stream_response import StreamResponse
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
    api_instance = hotdata.StreamsApi(api_client)
    stream_id = 'stream_id_example' # str | Stream ID

    try:
        # Get a stream
        api_response = api_instance.get_stream_handler(stream_id)
        print("The response of StreamsApi->get_stream_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StreamsApi->get_stream_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **stream_id** | **str**| Stream ID | 

### Return type

[**StreamResponse**](StreamResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The stream |  -  |
**403** | The API key is limited to another database |  -  |
**404** | Stream not found, or streams are not enabled |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ingest_stream_handler**
> IngestStreamResponse ingest_stream_handler(stream_id, ingest_stream_request)

Append rows to a stream

Append rows to a stream. The body is a JSON object with a `spans` array of rows, up to 64 MiB. The first request sets the stream's columns and returns them.

After that, fields match columns by name. A missing field is null. A field with no column, or a value of the wrong type, goes to the `_extra` column. Every row must carry the time column, unless Hotdata sets `_ingested_at`. The call returns once the rows are accepted; they can be queried within seconds.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.ingest_stream_request import IngestStreamRequest
from hotdata.models.ingest_stream_response import IngestStreamResponse
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
    api_instance = hotdata.StreamsApi(api_client)
    stream_id = 'stream_id_example' # str | Stream ID
    ingest_stream_request = hotdata.IngestStreamRequest() # IngestStreamRequest | 

    try:
        # Append rows to a stream
        api_response = api_instance.ingest_stream_handler(stream_id, ingest_stream_request)
        print("The response of StreamsApi->ingest_stream_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StreamsApi->ingest_stream_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **stream_id** | **str**| Stream ID | 
 **ingest_stream_request** | [**IngestStreamRequest**](IngestStreamRequest.md)|  | 

### Return type

[**IngestStreamResponse**](IngestStreamResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Rows appended |  -  |
**400** | The body has no &#x60;spans&#x60; array, a row lacks the time column, or a value does not fit its column |  -  |
**403** | The API key is limited to another database |  -  |
**404** | Stream not found, or streams are not enabled |  -  |
**409** | The stream&#39;s table was changed by another writer |  -  |
**429** | Too many rows are waiting to be stored. Retry shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

