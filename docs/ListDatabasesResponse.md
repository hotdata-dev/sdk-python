# ListDatabasesResponse

Response body for GET /databases

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**databases** | [**List[DatabaseSummary]**](DatabaseSummary.md) |  | 

## Example

```python
from hotdata.models.list_databases_response import ListDatabasesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListDatabasesResponse from a JSON string
list_databases_response_instance = ListDatabasesResponse.from_json(json)
# print the JSON string representation of the object
print(ListDatabasesResponse.to_json())

# convert the object into a dict
list_databases_response_dict = list_databases_response_instance.to_dict()
# create an instance of ListDatabasesResponse from a dict
list_databases_response_from_dict = ListDatabasesResponse.from_dict(list_databases_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


