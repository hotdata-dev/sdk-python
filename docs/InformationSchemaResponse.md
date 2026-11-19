# InformationSchemaResponse

A page of tables.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of tables on this page, not the total. An empty &#x60;tables&#x60; array does not mean the listing is finished: check &#x60;has_more&#x60;. | 
**has_more** | **bool** | Whether more tables follow. Fetch them with &#x60;next_cursor&#x60;. | 
**limit** | **int** | Page size used: the &#x60;limit&#x60; you sent, capped at the maximum, or the default when omitted. | 
**next_cursor** | **str** | Cursor for the next page, present only when &#x60;has_more&#x60; is true. Pass it as the &#x60;cursor&#x60; query parameter. | [optional] 
**tables** | [**List[TableInfo]**](TableInfo.md) | Tables on this page. | 

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


