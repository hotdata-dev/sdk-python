# hotdata.InformationSchemaApi

All URIs are relative to *https://api.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**information_schema**](InformationSchemaApi.md#information_schema) | **GET** /v1/information_schema | List tables


# **information_schema**
> InformationSchemaResponse information_schema(connection_id=connection_id, var_schema=var_schema, table=table, include_columns=include_columns, limit=limit, cursor=cursor)

List tables

List tables, with optional filters and pagination. `schema` and `table` accept SQL `%` wildcards. Set `include_columns=true` to include each table's columns.

Each table reports its `partition_by` and `sorted_by` layout, which is fixed when the table is created. An empty array means none was set. An API key limited to one database must pass that database's `connection_id`.

### Example

* Api Key Authentication (WorkspaceId):
* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.information_schema_response import InformationSchemaResponse
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
    api_instance = hotdata.InformationSchemaApi(api_client)
    connection_id = 'connection_id_example' # str | Filter by connection ID (optional)
    var_schema = 'var_schema_example' # str | Filter by schema name (supports % wildcards) (optional)
    table = 'table_example' # str | Filter by table name (supports % wildcards) (optional)
    include_columns = True # bool | Include each table's columns. Default: false. (optional)
    limit = 56 # int | Tables per page. Default 100, maximum 1000. (optional)
    cursor = 'cursor_example' # str | The `next_cursor` from the previous page (optional)

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
 **include_columns** | **bool**| Include each table&#39;s columns. Default: false. | [optional] 
 **limit** | **int**| Tables per page. Default 100, maximum 1000. | [optional] 
 **cursor** | **str**| The &#x60;next_cursor&#x60; from the previous page | [optional] 

### Return type

[**InformationSchemaResponse**](InformationSchemaResponse.md)

### Authorization

[WorkspaceId](../README.md#WorkspaceId), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Table metadata |  -  |
**403** | The API key is limited to one database, and &#x60;connection_id&#x60; does not name that database&#39;s connection |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

