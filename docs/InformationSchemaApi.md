# hotdata.InformationSchemaApi

All URIs are relative to *https://app.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**information_schema**](InformationSchemaApi.md#information_schema) | **GET** /v1/information_schema | List tables


# **information_schema**
> InformationSchemaResponse information_schema(connection_id=connection_id, var_schema=var_schema, table=table, include_columns=include_columns, limit=limit, cursor=cursor)

List tables

List discovered tables with optional filtering and pagination. Supports wildcard patterns (SQL %) for schema and table name filters. Set include_columns=true to include column definitions (omitted by default).

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.information_schema_response import InformationSchemaResponse
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
    api_instance = hotdata.InformationSchemaApi(api_client)
    connection_id = 'connection_id_example' # str | Filter by connection ID (optional)
    var_schema = 'var_schema_example' # str | Filter by schema name (supports % wildcards) (optional)
    table = 'table_example' # str | Filter by table name (supports % wildcards) (optional)
    include_columns = True # bool | Include column definitions (default: false) (optional)
    limit = 56 # int | Maximum number of tables per page (optional)
    cursor = 'cursor_example' # str | Pagination cursor from a previous response (optional)

    try:
        # List tables
        api_response = api_instance.information_schema(connection_id=connection_id, var_schema=var_schema, table=table, include_columns=include_columns, limit=limit, cursor=cursor)
        print("The response of InformationSchemaApi->information_schema:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InformationSchemaApi->information_schema: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| Filter by connection ID | [optional] 
 **var_schema** | **str**| Filter by schema name (supports % wildcards) | [optional] 
 **table** | **str**| Filter by table name (supports % wildcards) | [optional] 
 **include_columns** | **bool**| Include column definitions (default: false) | [optional] 
 **limit** | **int**| Maximum number of tables per page | [optional] 
 **cursor** | **str**| Pagination cursor from a previous response | [optional] 

### Return type

[**InformationSchemaResponse**](InformationSchemaResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Table metadata |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

