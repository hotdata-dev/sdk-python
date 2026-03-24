# hotdata.DatasetsApi

All URIs are relative to *https://app.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_dataset**](DatasetsApi.md#create_dataset) | **POST** /v1/datasets | Create dataset
[**delete_dataset**](DatasetsApi.md#delete_dataset) | **DELETE** /v1/datasets/{id} | Delete dataset
[**get_dataset**](DatasetsApi.md#get_dataset) | **GET** /v1/datasets/{id} | Get dataset
[**list_dataset_versions**](DatasetsApi.md#list_dataset_versions) | **GET** /v1/datasets/{id}/versions | List dataset versions
[**list_datasets**](DatasetsApi.md#list_datasets) | **GET** /v1/datasets | List datasets
[**update_dataset**](DatasetsApi.md#update_dataset) | **PUT** /v1/datasets/{id} | Update dataset


# **create_dataset**
> CreateDatasetResponse create_dataset(create_dataset_request)

Create dataset

Create a new dataset from an uploaded file or inline data. The dataset becomes a queryable table under the `datasets` schema (e.g., `SELECT * FROM datasets.my_table`). Supports CSV, JSON, and Parquet formats. Optionally specify explicit column types.

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.create_dataset_request import CreateDatasetRequest
from hotdata.models.create_dataset_response import CreateDatasetResponse
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
    api_instance = hotdata.DatasetsApi(api_client)
    create_dataset_request = hotdata.CreateDatasetRequest() # CreateDatasetRequest | 

    try:
        # Create dataset
        api_response = api_instance.create_dataset(create_dataset_request)
        print("The response of DatasetsApi->create_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetsApi->create_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_dataset_request** | [**CreateDatasetRequest**](CreateDatasetRequest.md)|  | 

### Return type

[**CreateDatasetResponse**](CreateDatasetResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Dataset created |  -  |
**400** | Invalid request |  -  |
**409** | Dataset already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_dataset**
> delete_dataset(id)

Delete dataset

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
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
    api_instance = hotdata.DatasetsApi(api_client)
    id = 'id_example' # str | Dataset ID

    try:
        # Delete dataset
        api_instance.delete_dataset(id)
    except Exception as e:
        print("Exception when calling DatasetsApi->delete_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Dataset ID | 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Dataset deleted |  -  |
**404** | Dataset not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dataset**
> GetDatasetResponse get_dataset(id)

Get dataset

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.get_dataset_response import GetDatasetResponse
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
    api_instance = hotdata.DatasetsApi(api_client)
    id = 'id_example' # str | Dataset ID

    try:
        # Get dataset
        api_response = api_instance.get_dataset(id)
        print("The response of DatasetsApi->get_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetsApi->get_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Dataset ID | 

### Return type

[**GetDatasetResponse**](GetDatasetResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Dataset details |  -  |
**404** | Dataset not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_dataset_versions**
> ListDatasetVersionsResponse list_dataset_versions(id, limit=limit, offset=offset)

List dataset versions

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_dataset_versions_response import ListDatasetVersionsResponse
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
    api_instance = hotdata.DatasetsApi(api_client)
    id = 'id_example' # str | Dataset ID
    limit = 56 # int | Maximum number of versions (default: 100, max: 1000) (optional)
    offset = 56 # int | Pagination offset (default: 0) (optional)

    try:
        # List dataset versions
        api_response = api_instance.list_dataset_versions(id, limit=limit, offset=offset)
        print("The response of DatasetsApi->list_dataset_versions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetsApi->list_dataset_versions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Dataset ID | 
 **limit** | **int**| Maximum number of versions (default: 100, max: 1000) | [optional] 
 **offset** | **int**| Pagination offset (default: 0) | [optional] 

### Return type

[**ListDatasetVersionsResponse**](ListDatasetVersionsResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of dataset versions |  -  |
**404** | Dataset not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_datasets**
> ListDatasetsResponse list_datasets(limit=limit, offset=offset)

List datasets

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_datasets_response import ListDatasetsResponse
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
    api_instance = hotdata.DatasetsApi(api_client)
    limit = 56 # int | Maximum number of datasets (default: 100, max: 1000) (optional)
    offset = 56 # int | Pagination offset (default: 0) (optional)

    try:
        # List datasets
        api_response = api_instance.list_datasets(limit=limit, offset=offset)
        print("The response of DatasetsApi->list_datasets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetsApi->list_datasets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of datasets (default: 100, max: 1000) | [optional] 
 **offset** | **int**| Pagination offset (default: 0) | [optional] 

### Return type

[**ListDatasetsResponse**](ListDatasetsResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of datasets |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_dataset**
> UpdateDatasetResponse update_dataset(id, update_dataset_request)

Update dataset

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.update_dataset_request import UpdateDatasetRequest
from hotdata.models.update_dataset_response import UpdateDatasetResponse
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
    api_instance = hotdata.DatasetsApi(api_client)
    id = 'id_example' # str | Dataset ID
    update_dataset_request = hotdata.UpdateDatasetRequest() # UpdateDatasetRequest | 

    try:
        # Update dataset
        api_response = api_instance.update_dataset(id, update_dataset_request)
        print("The response of DatasetsApi->update_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetsApi->update_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Dataset ID | 
 **update_dataset_request** | [**UpdateDatasetRequest**](UpdateDatasetRequest.md)|  | 

### Return type

[**UpdateDatasetResponse**](UpdateDatasetResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Dataset updated |  -  |
**404** | Dataset not found |  -  |
**409** | Conflict |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

