# InformationSchemaResponse

Response body for GET /information_schema

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of tables in this response, the same meaning &#x60;count&#x60; carries on the results and databases listings.  This is a page size, not a total for the whole filter. Page with &#x60;has_more&#x60; and &#x60;next_cursor&#x60;: an empty &#x60;tables&#x60; array on its own does not mean the listing is finished. | 
**has_more** | **bool** | True when more tables follow this page. Pass &#x60;next_cursor&#x60; to fetch them. | 
**limit** | **int** | The page size in effect for this response — the &#x60;limit&#x60; you asked for, clamped to the server&#39;s maximum, or the server default when you sent none. | 
**next_cursor** | **str** | Cursor for the next page, present only when &#x60;has_more&#x60; is &#x60;true&#x60;. Send it back as the &#x60;cursor&#x60; query parameter. | [optional] 
**tables** | [**List[TableInfo]**](TableInfo.md) | The tables on this page. | 

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


