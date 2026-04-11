# hotdata.ConnectionTypesApi

All URIs are relative to *https://app.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_connection_type**](ConnectionTypesApi.md#get_connection_type) | **GET** /v1/connection-types/{name} | Get connection type details
[**list_connection_types**](ConnectionTypesApi.md#list_connection_types) | **GET** /v1/connection-types | List connection types


# **get_connection_type**
> ConnectionTypeDetail get_connection_type(name)

Get connection type details

Get configuration schema and authentication requirements for a specific connection type.

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.connection_type_detail import ConnectionTypeDetail
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
    api_instance = hotdata.ConnectionTypesApi(api_client)
    name = 'name_example' # str | Connection type name (e.g. postgres, mysql, snowflake)

    try:
        # Get connection type details
        api_response = api_instance.get_connection_type(name)
        print("The response of ConnectionTypesApi->get_connection_type:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionTypesApi->get_connection_type: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Connection type name (e.g. postgres, mysql, snowflake) | 

### Return type

[**ConnectionTypeDetail**](ConnectionTypeDetail.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Connection type details |  -  |
**404** | Unknown connection type |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_connection_types**
> ListConnectionTypesResponse list_connection_types()

List connection types

List all available connection types, including native sources and FlightDLT services.

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_connection_types_response import ListConnectionTypesResponse
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
    api_instance = hotdata.ConnectionTypesApi(api_client)

    try:
        # List connection types
        api_response = api_instance.list_connection_types()
        print("The response of ConnectionTypesApi->list_connection_types:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionTypesApi->list_connection_types: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListConnectionTypesResponse**](ListConnectionTypesResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Available connection types |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

