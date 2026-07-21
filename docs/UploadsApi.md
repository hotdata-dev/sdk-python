# hotdata.UploadsApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_upload_session_handler**](UploadsApi.md#create_upload_session_handler) | **POST** /v1/uploads | Create upload session
[**create_upload_sessions_batch_handler**](UploadsApi.md#create_upload_sessions_batch_handler) | **POST** /v1/uploads/batch | Create upload sessions in bulk
[**finalize_upload_handler**](UploadsApi.md#finalize_upload_handler) | **POST** /v1/uploads/{upload_id}/finalize | Finalize upload
[**mint_upload_parts_handler**](UploadsApi.md#mint_upload_parts_handler) | **POST** /v1/uploads/{upload_id}/parts | Mint upload part URLs


# **create_upload_session_handler**
> UploadSessionResponse create_upload_session_handler(create_upload_request)

Create upload session

Create an upload session for a file you will send directly to storage. The response is one of three shapes. For a small file (`mode: single`) it contains a short-lived `url` to `PUT` the whole file to. For a large file with a known size (`mode: multipart`) it contains `part_urls` and `part_size`: split the file into `part_size`-byte chunks (the last is the remainder) and `PUT` chunk *i* (1-based) to `part_urls[i - 1]`, keeping each response's `ETag`. Slice by `part_size`, not by an even division across `part_urls.len()` (which can make a non-final part too small). For a file whose size you do not know up front, omit `declared_size_bytes`: the response is `mode: multipart` with a `part_size` but NO `part_urls`. As you stream, call `POST /v1/uploads/{upload_id}/parts` with a batch of `part_numbers` to mint per-part `PUT` URLs, `PUT` each part and keep its `ETag`, then finalize as for any multipart upload. In all cases the response also includes a one-time `finalize_token`. After uploading, call the finalize endpoint with the token (and, for multipart, the `{part_number, e_tag}` list) to make the upload usable as managed-table contents. The returned upload ID can then be passed to the managed-table load endpoint.

You may hint a preferred part size with `part_size`; the service clamps it to the allowed range and ignores it for single-`PUT` uploads.

If the response status is `501` with error code `PRESIGN_UNSUPPORTED`, the configured storage backend cannot issue upload URLs (for example a local-filesystem development backend).

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
**501** | Storage backend cannot issue upload URLs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_upload_sessions_batch_handler**
> BatchCreateUploadResponse create_upload_sessions_batch_handler(batch_create_upload_request)

Create upload sessions in bulk

Create upload sessions for several files in one request. Each file is planned independently and the response returns one session per requested file, in the same order. Each session is finalized separately via the finalize endpoint, so you can upload and finalize files at your own pace.

If the response status is `501` with error code `PRESIGN_UNSUPPORTED`, the configured storage backend cannot issue upload URLs (for example a local-filesystem development backend).

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
**501** | Storage backend cannot issue upload URLs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **finalize_upload_handler**
> FinalizeUploadResponse finalize_upload_handler(upload_id, x_upload_finalize_token, finalize_upload_request=finalize_upload_request)

Finalize upload

Confirm that a file has been uploaded to storage and make it usable as managed-table contents. Supply the `finalize_token` returned when the session was created, in the `X-Upload-Finalize-Token` header. When you declared a size at create time, the uploaded file's size is validated against it and a mismatch is rejected. An upload created without a declared size is finalized from its uploaded parts; it must be non-empty and is rejected if it exceeds the server's maximum upload size. Finalize is exactly-once: a second finalize of the same upload is rejected.

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

# **mint_upload_parts_handler**
> MintUploadPartsResponse mint_upload_parts_handler(upload_id, x_upload_finalize_token, mint_upload_parts_request)

Mint upload part URLs

Mint short-lived presigned URLs for specific parts of a multi-part upload. This is required for a streaming (unknown-size) upload — created by omitting the declared size — which mints no part URLs up front. It also works for a known-size multi-part upload: use it to re-mint a part whose URL expired before you uploaded that part. Supply the `finalize_token` returned when the session was created, in the `X-Upload-Finalize-Token` header, and the 1-based `part_numbers` you want URLs for. `PUT` each part's bytes to its URL, keep each response's `ETag`, then pass the `{part_number, e_tag}` list to finalize. You may mint parts in batches as you upload, and re-mint a part number whose URL expired before you finished uploading it.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.mint_upload_parts_request import MintUploadPartsRequest
from hotdata.models.mint_upload_parts_response import MintUploadPartsResponse
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
    mint_upload_parts_request = hotdata.MintUploadPartsRequest() # MintUploadPartsRequest | 

    try:
        # Mint upload part URLs
        api_response = api_instance.mint_upload_parts_handler(upload_id, x_upload_finalize_token, mint_upload_parts_request)
        print("The response of UploadsApi->mint_upload_parts_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UploadsApi->mint_upload_parts_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **upload_id** | **str**| Upload session ID returned at create time | 
 **x_upload_finalize_token** | **str**| One-time finalize token returned when the session was created | 
 **mint_upload_parts_request** | [**MintUploadPartsRequest**](MintUploadPartsRequest.md)|  | 

### Return type

[**MintUploadPartsResponse**](MintUploadPartsResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Minted part URLs |  -  |
**400** | Invalid finalize token, invalid part numbers, batch too large, or the upload is not a multi-part upload |  -  |
**404** | Upload session not found |  -  |
**501** | Storage backend cannot issue upload URLs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

