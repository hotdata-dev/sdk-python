# InformationSchemaResponse

Response body for GET /information_schema

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | 
**has_more** | **bool** |  | 
**limit** | **int** |  | 
**next_cursor** | **str** |  | [optional] 
**tables** | [**List[TableInfo]**](TableInfo.md) |  | 

## Example

```python
from hotdata.models.information_schema_response import InformationSchemaResponse

# TODO update the JSON string below
json = "{}"
# create an instance of InformationSchemaResponse from a JSON string
information_schema_response_instance = InformationSchemaResponse.from_json(json)
# print the JSON string representation of the object
print(InformationSchemaResponse.to_json())

# convert the object into a dict
information_schema_response_dict = information_schema_response_instance.to_dict()
# create an instance of InformationSchemaResponse from a dict
information_schema_response_from_dict = InformationSchemaResponse.from_dict(information_schema_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


