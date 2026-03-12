# ConnectionSchemaError

Error details for a failed connection schema refresh

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_id** | **str** |  | 
**error** | **str** |  | 

## Example

```python
from hotdata.models.connection_schema_error import ConnectionSchemaError

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectionSchemaError from a JSON string
connection_schema_error_instance = ConnectionSchemaError.from_json(json)
# print the JSON string representation of the object
print(ConnectionSchemaError.to_json())

# convert the object into a dict
connection_schema_error_dict = connection_schema_error_instance.to_dict()
# create an instance of ConnectionSchemaError from a dict
connection_schema_error_from_dict = ConnectionSchemaError.from_dict(connection_schema_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


