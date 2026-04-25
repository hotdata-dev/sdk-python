# hotdata.EmbeddingProvidersApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_embedding_provider**](EmbeddingProvidersApi.md#create_embedding_provider) | **POST** /v1/embedding-providers | Create embedding provider
[**delete_embedding_provider**](EmbeddingProvidersApi.md#delete_embedding_provider) | **DELETE** /v1/embedding-providers/{id} | Delete embedding provider
[**get_embedding_provider**](EmbeddingProvidersApi.md#get_embedding_provider) | **GET** /v1/embedding-providers/{id} | Get embedding provider
[**list_embedding_providers**](EmbeddingProvidersApi.md#list_embedding_providers) | **GET** /v1/embedding-providers | List embedding providers
[**update_embedding_provider**](EmbeddingProvidersApi.md#update_embedding_provider) | **PUT** /v1/embedding-providers/{id} | Update embedding provider


# **create_embedding_provider**
> CreateEmbeddingProviderResponse create_embedding_provider(create_embedding_provider_request)

Create embedding provider

Register a new embedding provider that can be used to generate vector embeddings for text columns. Providers can be service-based (e.g., OpenAI) or local.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.create_embedding_provider_request import CreateEmbeddingProviderRequest
from hotdata.models.create_embedding_provider_response import CreateEmbeddingProviderResponse
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
    api_instance = hotdata.EmbeddingProvidersApi(api_client)
    create_embedding_provider_request = hotdata.CreateEmbeddingProviderRequest() # CreateEmbeddingProviderRequest | 

    try:
        # Create embedding provider
        api_response = api_instance.create_embedding_provider(create_embedding_provider_request)
        print("The response of EmbeddingProvidersApi->create_embedding_provider:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EmbeddingProvidersApi->create_embedding_provider: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_embedding_provider_request** | [**CreateEmbeddingProviderRequest**](CreateEmbeddingProviderRequest.md)|  | 

### Return type

[**CreateEmbeddingProviderResponse**](CreateEmbeddingProviderResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Embedding provider created |  -  |
**400** | Invalid request |  -  |
**409** | Provider with this name already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_embedding_provider**
> delete_embedding_provider(id)

Delete embedding provider

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
    api_instance = hotdata.EmbeddingProvidersApi(api_client)
    id = 'id_example' # str | Embedding provider ID

    try:
        # Delete embedding provider
        api_instance.delete_embedding_provider(id)
    except Exception as e:
        print("Exception when calling EmbeddingProvidersApi->delete_embedding_provider: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Embedding provider ID | 

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
**204** | Embedding provider deleted |  -  |
**404** | Provider not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_embedding_provider**
> EmbeddingProviderResponse get_embedding_provider(id)

Get embedding provider

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.embedding_provider_response import EmbeddingProviderResponse
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
    api_instance = hotdata.EmbeddingProvidersApi(api_client)
    id = 'id_example' # str | Embedding provider ID

    try:
        # Get embedding provider
        api_response = api_instance.get_embedding_provider(id)
        print("The response of EmbeddingProvidersApi->get_embedding_provider:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EmbeddingProvidersApi->get_embedding_provider: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Embedding provider ID | 

### Return type

[**EmbeddingProviderResponse**](EmbeddingProviderResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Embedding provider details |  -  |
**404** | Provider not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_embedding_providers**
> ListEmbeddingProvidersResponse list_embedding_providers()

List embedding providers

List all registered embedding providers.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_embedding_providers_response import ListEmbeddingProvidersResponse
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
    api_instance = hotdata.EmbeddingProvidersApi(api_client)

    try:
        # List embedding providers
        api_response = api_instance.list_embedding_providers()
        print("The response of EmbeddingProvidersApi->list_embedding_providers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EmbeddingProvidersApi->list_embedding_providers: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListEmbeddingProvidersResponse**](ListEmbeddingProvidersResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of embedding providers |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_embedding_provider**
> UpdateEmbeddingProviderResponse update_embedding_provider(id, update_embedding_provider_request)

Update embedding provider

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.update_embedding_provider_request import UpdateEmbeddingProviderRequest
from hotdata.models.update_embedding_provider_response import UpdateEmbeddingProviderResponse
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
    api_instance = hotdata.EmbeddingProvidersApi(api_client)
    id = 'id_example' # str | Embedding provider ID
    update_embedding_provider_request = hotdata.UpdateEmbeddingProviderRequest() # UpdateEmbeddingProviderRequest | 

    try:
        # Update embedding provider
        api_response = api_instance.update_embedding_provider(id, update_embedding_provider_request)
        print("The response of EmbeddingProvidersApi->update_embedding_provider:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EmbeddingProvidersApi->update_embedding_provider: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Embedding provider ID | 
 **update_embedding_provider_request** | [**UpdateEmbeddingProviderRequest**](UpdateEmbeddingProviderRequest.md)|  | 

### Return type

[**UpdateEmbeddingProviderResponse**](UpdateEmbeddingProviderResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Embedding provider updated |  -  |
**404** | Provider not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

