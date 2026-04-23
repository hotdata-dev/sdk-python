# hotdata.UploadsApi

All URIs are relative to *https://app.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_uploads**](UploadsApi.md#list_uploads) | **GET** /v1/files | List uploads
[**upload_file**](UploadsApi.md#upload_file) | **POST** /v1/files | Upload file


# **list_uploads**
> ListUploadsResponse list_uploads(status=status)

List uploads

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_uploads_response import ListUploadsResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

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

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of uploads |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_file**
> UploadResponse upload_file(request_body, streaming=streaming)

Upload file

Upload a file to be used as a dataset source. Send the raw file bytes as the request body with an appropriate Content-Type header (e.g., `text/csv`, `application/json`, `application/parquet`). The returned upload ID can be passed to POST /v1/datasets to create a queryable table. Add `?streaming=true` for large files (up to 20GB) — streams to disk instead of loading into memory.

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.upload_response import UploadResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.UploadsApi(api_client)
    request_body = [56] # List[int] | 
    streaming = True # bool | Stream upload to disk for large files (up to 20GB) (optional)

    try:
        # Upload file
        api_response = api_instance.upload_file(request_body, streaming=streaming)
        print("The response of UploadsApi->upload_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UploadsApi->upload_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**List[int]**](int.md)|  | 
 **streaming** | **bool**| Stream upload to disk for large files (up to 20GB) | [optional] 

### Return type

[**UploadResponse**](UploadResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | File uploaded |  -  |
**400** | Invalid request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

