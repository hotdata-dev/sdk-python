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

Start an upload. You `PUT` the file straight to the URLs in the response, not through this API. The response has a one-time `finalize_token` and one of three shapes:

- `mode: single`: `PUT` the whole file to `url`.
- `mode: multipart` with `part_urls`: split the file into `part_size`-byte parts (the last one is smaller) and `PUT` part *i* to `part_urls[i - 1]`. Keep each part's `ETag`.
- `mode: multipart` with no `part_urls`, when you omit `declared_size_bytes`: get part URLs as you go from `POST /v1/uploads/{upload_id}/parts`.

Then call `POST /v1/uploads/{upload_id}/finalize`, and load the upload into a table by its ID.

An upload can be at most 16 GiB by default. With `declared_size_bytes`, a larger file is refused here; without it, at finalize. To load more into one table, split the data and load each upload with `mode: append`. A 501 `PRESIGN_UNSUPPORTED` means upload URLs are not available; send the data inline on the load endpoint.

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
**400** | Invalid request, such as a file that is too large or an unsupported checksum algorithm |  -  |
**501** | This deployment cannot issue upload URLs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_upload_sessions_batch_handler**
> BatchCreateUploadResponse create_upload_sessions_batch_handler(batch_create_upload_request)

Create upload sessions in bulk

Create upload sessions for up to 100 files in one request. Sessions come back in the order of the request. Upload and finalize each one on its own.

The 16 GiB size limit applies to each file. If any file is refused, no sessions are created; retry the whole request. A 501 `PRESIGN_UNSUPPORTED` means upload URLs are not available.

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
**400** | Invalid request, such as a file that is too large or an unsupported checksum algorithm |  -  |
**501** | This deployment cannot issue upload URLs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **finalize_upload_handler**
> FinalizeUploadResponse finalize_upload_handler(upload_id, x_upload_finalize_token, finalize_upload_request=finalize_upload_request)

Finalize upload

Confirm that a file is uploaded, so it can be loaded into a table. Send the `finalize_token` in the `X-Upload-Finalize-Token` header. For a multipart upload, send the `{part_number, e_tag}` list.

If you declared a size, the file must match it. An upload without a declared size must not be empty and must be at most 16 GiB by default. You can finalize an upload only once. Load it within 7 days (by default), or it is deleted.

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
    upload_id = 'upload_id_example' # str | Upload ID
    x_upload_finalize_token = 'x_upload_finalize_token_example' # str | The `finalize_token` from the create response
    finalize_upload_request = hotdata.FinalizeUploadRequest() # FinalizeUploadRequest | Send `parts` for a multipart upload. A single-`PUT` upload needs no body. (optional)

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
 **upload_id** | **str**| Upload ID | 
 **x_upload_finalize_token** | **str**| The &#x60;finalize_token&#x60; from the create response | 
 **finalize_upload_request** | [**FinalizeUploadRequest**](FinalizeUploadRequest.md)| Send &#x60;parts&#x60; for a multipart upload. A single-&#x60;PUT&#x60; upload needs no body. | [optional] 

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
**400** | Missing token header, a size that does not match, no uploaded file, or an upload that cannot be finalized (for example, already finalized) |  -  |
**404** | Upload not found, or the token does not match it |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mint_upload_parts_handler**
> MintUploadPartsResponse mint_upload_parts_handler(upload_id, x_upload_finalize_token, mint_upload_parts_request)

Mint upload part URLs

Get upload URLs for parts of a multipart upload. You need this for an upload created without `declared_size_bytes`. You can also use it to get a new URL for a part whose URL expired.

Send the `finalize_token` in the `X-Upload-Finalize-Token` header and the part numbers (starting at 1), up to 100 per request. `PUT` each part to its URL, keep its `ETag`, and pass the list to finalize.

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
    upload_id = 'upload_id_example' # str | Upload ID
    x_upload_finalize_token = 'x_upload_finalize_token_example' # str | The `finalize_token` from the create response
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
 **upload_id** | **str**| Upload ID | 
 **x_upload_finalize_token** | **str**| The &#x60;finalize_token&#x60; from the create response | 
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
**400** | Missing token header, invalid part numbers, more than 100 parts, or not a multipart upload |  -  |
**404** | Upload not found, or the token does not match it |  -  |
**501** | This deployment cannot issue upload URLs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

