# hotdata.SecretsApi

All URIs are relative to *https://app.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_secret_handler**](SecretsApi.md#create_secret_handler) | **POST** /v1/secrets | Create secret
[**delete_secret_handler**](SecretsApi.md#delete_secret_handler) | **DELETE** /v1/secrets/{name} | Delete secret
[**get_secret_handler**](SecretsApi.md#get_secret_handler) | **GET** /v1/secrets/{name} | Get secret
[**list_secrets_handler**](SecretsApi.md#list_secrets_handler) | **GET** /v1/secrets | List secrets
[**update_secret_handler**](SecretsApi.md#update_secret_handler) | **PUT** /v1/secrets/{name} | Update secret


# **create_secret_handler**
> CreateSecretResponse create_secret_handler(create_secret_request)

Create secret

Store a new named secret. The value is encrypted at rest and can be referenced by connections for authentication. Secret names must be unique.

### Example


```python
import hotdata
from hotdata.models.create_secret_request import CreateSecretRequest
from hotdata.models.create_secret_response import CreateSecretResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.SecretsApi(api_client)
    create_secret_request = hotdata.CreateSecretRequest() # CreateSecretRequest | 

    try:
        # Create secret
        api_response = api_instance.create_secret_handler(create_secret_request)
        print("The response of SecretsApi->create_secret_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->create_secret_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_secret_request** | [**CreateSecretRequest**](CreateSecretRequest.md)|  | 

### Return type

[**CreateSecretResponse**](CreateSecretResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Secret created |  -  |
**409** | Secret already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_secret_handler**
> delete_secret_handler(name)

Delete secret

### Example


```python
import hotdata
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.SecretsApi(api_client)
    name = 'name_example' # str | Secret name

    try:
        # Delete secret
        api_instance.delete_secret_handler(name)
    except Exception as e:
        print("Exception when calling SecretsApi->delete_secret_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Secret name | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Secret deleted |  -  |
**404** | Secret not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_secret_handler**
> GetSecretResponse get_secret_handler(name)

Get secret

Get metadata for a secret. The secret value is never returned.

### Example


```python
import hotdata
from hotdata.models.get_secret_response import GetSecretResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.SecretsApi(api_client)
    name = 'name_example' # str | Secret name

    try:
        # Get secret
        api_response = api_instance.get_secret_handler(name)
        print("The response of SecretsApi->get_secret_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->get_secret_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Secret name | 

### Return type

[**GetSecretResponse**](GetSecretResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Secret metadata |  -  |
**404** | Secret not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_secrets_handler**
> ListSecretsResponse list_secrets_handler()

List secrets

List all stored secrets. Only metadata (name, timestamps) is returned — secret values are never exposed.

### Example


```python
import hotdata
from hotdata.models.list_secrets_response import ListSecretsResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.SecretsApi(api_client)

    try:
        # List secrets
        api_response = api_instance.list_secrets_handler()
        print("The response of SecretsApi->list_secrets_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->list_secrets_handler: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListSecretsResponse**](ListSecretsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of secrets |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_secret_handler**
> UpdateSecretResponse update_secret_handler(name, update_secret_request)

Update secret

### Example


```python
import hotdata
from hotdata.models.update_secret_request import UpdateSecretRequest
from hotdata.models.update_secret_response import UpdateSecretResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)


# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.SecretsApi(api_client)
    name = 'name_example' # str | Secret name
    update_secret_request = hotdata.UpdateSecretRequest() # UpdateSecretRequest | 

    try:
        # Update secret
        api_response = api_instance.update_secret_handler(name, update_secret_request)
        print("The response of SecretsApi->update_secret_handler:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->update_secret_handler: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Secret name | 
 **update_secret_request** | [**UpdateSecretRequest**](UpdateSecretRequest.md)|  | 

### Return type

[**UpdateSecretResponse**](UpdateSecretResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Secret updated |  -  |
**404** | Secret not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

