# hotdata.UploadsApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_upload_session_handler**](UploadsApi.md#create_upload_session_handler) | **POST** /v1/uploads | Create upload session
[**create_upload_sessions_batch_handler**](UploadsApi.md#create_upload_sessions_batch_handler) | **POST** /v1/uploads/batch | Create upload sessions in bulk
[**finalize_upload_handler**](UploadsApi.md#finalize_upload_handler) | **POST** /v1/uploads/{upload_id}/finalize | Finalize upload
[**list_uploads**](UploadsApi.md#list_uploads) | **GET** /v1/files | List uploads
[**upload_file**](UploadsApi.md#upload_file) | **POST** /v1/files | Upload file


# **create_upload_session_handler**
> UploadSessionResponse create_upload_session_handler(create_upload_request)

Create upload session

Create an upload session for a file you will send directly to storage. Based on the declared size, the response is one of two shapes. For a small file (`mode: single`) it contains a short-lived `url` to `PUT` the whole file to. For a large file (`mode: multipart`) it contains `part_urls` and `part_size`: split the file into `part_size`-byte chunks (the last is the remainder) and `PUT` chunk *i* (1-based) to `part_urls[i - 1]`, keeping each response's `ETag`. Slice by `part_size`, not by an even division across `part_urls.len()` (which can make a non-final part too small). In both cases the response also includes a one-time `finalize_token`. After uploading, call the finalize endpoint with the token (and, for multipart, the `{part_number, e_tag}` list) to make the upload usable as managed-table contents. The returned upload ID can then be passed to the managed-table load endpoint.

You may hint a preferred part size with `part_size`; the service clamps it to the allowed range and ignores it for single-`PUT` uploads.

If the response status is `501` with error code `PRESIGN_UNSUPPORTED`, the configured storage backend cannot issue upload URLs; send the file to the `POST /v1/files` endpoint instead.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.create_upload_request import CreateUploadRequest
from hotdata.models.upload_session_response import UploadSessionResponse
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
    api_instance = hotdata.UploadsApi(api_client)
    create_upload_request = hotdata.CreateUploadRequest() # CreateUploadRequest | 

    try:
        # Create upload session
        api_response = api_instance.create_upload_session_handler(create_upload_request)
        print("The response of UploadsApi->create_upload_session_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UploadsApi->create_upload_session_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_upload_request** | [**CreateUploadRequest**](CreateUploadRequest.md)|  | 

### Return type

[**UploadSessionResponse**](UploadSessionResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Upload session created |  -  |
**400** | Invalid request (e.g. file too large, unsupported checksum algorithm) |  -  |
**501** | Storage backend cannot issue upload URLs; use POST /v1/files instead |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_upload_sessions_batch_handler**
> BatchCreateUploadResponse create_upload_sessions_batch_handler(batch_create_upload_request)

Create upload sessions in bulk

Create upload sessions for several files in one request. Each file is planned independently and the response returns one session per requested file, in the same order. Each session is finalized separately via the finalize endpoint, so you can upload and finalize files at your own pace.

If the response status is `501` with error code `PRESIGN_UNSUPPORTED`, the configured storage backend cannot issue upload URLs; send each file to the `POST /v1/files` endpoint instead.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.batch_create_upload_request import BatchCreateUploadRequest
from hotdata.models.batch_create_upload_response import BatchCreateUploadResponse
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
    api_instance = hotdata.UploadsApi(api_client)
    batch_create_upload_request = hotdata.BatchCreateUploadRequest() # BatchCreateUploadRequest | 

    try:
        # Create upload sessions in bulk
        api_response = api_instance.create_upload_sessions_batch_handler(batch_create_upload_request)
        print("The response of UploadsApi->create_upload_sessions_batch_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UploadsApi->create_upload_sessions_batch_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **batch_create_upload_request** | [**BatchCreateUploadRequest**](BatchCreateUploadRequest.md)|  | 

### Return type

[**BatchCreateUploadResponse**](BatchCreateUploadResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Upload sessions created |  -  |
**400** | Invalid request (e.g. a file too large, unsupported checksum algorithm) |  -  |
**501** | Storage backend cannot issue upload URLs; use POST /v1/files instead |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **finalize_upload_handler**
> FinalizeUploadResponse finalize_upload_handler(upload_id, x_upload_finalize_token, finalize_upload_request=finalize_upload_request)

Finalize upload

Confirm that a file has been uploaded to storage and make it usable as managed-table contents. Supply the `finalize_token` returned when the session was created, in the `X-Upload-Finalize-Token` header. The uploaded file's size is validated against the size declared at create time; a mismatch is rejected. Finalize is exactly-once: a second finalize of the same upload is rejected.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.finalize_upload_request import FinalizeUploadRequest
from hotdata.models.finalize_upload_response import FinalizeUploadResponse
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
    api_instance = hotdata.UploadsApi(api_client)
    upload_id = 'upload_id_example' # str | Upload session ID returned at create time
    x_upload_finalize_token = 'x_upload_finalize_token_example' # str | One-time finalize token returned when the session was created
    finalize_upload_request = hotdata.FinalizeUploadRequest() # FinalizeUploadRequest | Optional; send `parts` only for a multi-part upload. Single-`PUT` uploads finalize with no body. (optional)

    try:
        # Finalize upload
        api_response = api_instance.finalize_upload_handler(upload_id, x_upload_finalize_token, finalize_upload_request=finalize_upload_request)
        print("The response of UploadsApi->finalize_upload_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UploadsApi->finalize_upload_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **upload_id** | **str**| Upload session ID returned at create time | 
 **x_upload_finalize_token** | **str**| One-time finalize token returned when the session was created | 
 **finalize_upload_request** | [**FinalizeUploadRequest**](FinalizeUploadRequest.md)| Optional; send &#x60;parts&#x60; only for a multi-part upload. Single-&#x60;PUT&#x60; uploads finalize with no body. | [optional] 

### Return type

[**FinalizeUploadResponse**](FinalizeUploadResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Upload finalized |  -  |
**400** | Invalid finalize token, uploaded size mismatch, missing object, or upload not finalizable |  -  |
**404** | Upload session not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_uploads**
> ListUploadsResponse list_uploads(status=status)

List uploads

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_uploads_response import ListUploadsResponse
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
    api_instance = hotdata.UploadsApi(api_client)
    status = 'status_example' # str | Filter by upload status (optional)

    try:
        # List uploads
        api_response = api_instance.list_uploads(status=status)
        print("The response of UploadsApi->list_uploads:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UploadsApi->list_uploads: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | **str**| Filter by upload status | [optional] 

### Return type

[**ListUploadsResponse**](ListUploadsResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of uploads |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_file**
> UploadResponse upload_file(body)

Upload file

Upload a Parquet file to publish as the contents of a managed table. Send the raw file bytes as the request body with an appropriate Content-Type header (e.g., `application/parquet`). The body is streamed to disk, so files up to 20GB are supported. The returned upload ID can be passed to the managed-table load endpoint.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.upload_response import UploadResponse
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
    api_instance = hotdata.UploadsApi(api_client)
    body = None # bytearray | 

    try:
        # Upload file
        api_response = api_instance.upload_file(body)
        print("The response of UploadsApi->upload_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UploadsApi->upload_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **bytearray**|  | 

### Return type

[**UploadResponse**](UploadResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | File uploaded |  -  |
**400** | Invalid request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

