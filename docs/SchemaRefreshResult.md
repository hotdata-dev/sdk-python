# SchemaRefreshResult

Response for schema refresh operations

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connections_failed** | **int** |  | 
**connections_refreshed** | **int** |  | 
**errors** | [**List[ConnectionSchemaError]**](ConnectionSchemaError.md) |  | [optional] 
**tables_added** | **int** |  | 
**tables_discovered** | **int** |  | 
**tables_modified** | **int** |  | 

## Example

```python
from hotdata.models.schema_refresh_result import SchemaRefreshResult

# TODO update the JSON string below
json = "{}"
# create an instance of SchemaRefreshResult from a JSON string
schema_refresh_result_instance = SchemaRefreshResult.from_json(json)
# print the JSON string representation of the object
print(SchemaRefreshResult.to_json())

# convert the object into a dict
schema_refresh_result_dict = schema_refresh_result_instance.to_dict()
# create an instance of SchemaRefreshResult from a dict
schema_refresh_result_from_dict = SchemaRefreshResult.from_dict(schema_refresh_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


