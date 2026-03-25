# ListConnectionTypesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_types** | [**List[ConnectionTypeSummary]**](ConnectionTypeSummary.md) |  | 

## Example

```python
from hotdata.models.list_connection_types_response import ListConnectionTypesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListConnectionTypesResponse from a JSON string
list_connection_types_response_instance = ListConnectionTypesResponse.from_json(json)
# print the JSON string representation of the object
print(ListConnectionTypesResponse.to_json())

# convert the object into a dict
list_connection_types_response_dict = list_connection_types_response_instance.to_dict()
# create an instance of ListConnectionTypesResponse from a dict
list_connection_types_response_from_dict = ListConnectionTypesResponse.from_dict(list_connection_types_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


