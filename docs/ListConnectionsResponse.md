# ListConnectionsResponse

Response body for GET /connections

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connections** | [**List[ConnectionInfo]**](ConnectionInfo.md) |  | 

## Example

```python
from hotdata.models.list_connections_response import ListConnectionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListConnectionsResponse from a JSON string
list_connections_response_instance = ListConnectionsResponse.from_json(json)
# print the JSON string representation of the object
print(ListConnectionsResponse.to_json())

# convert the object into a dict
list_connections_response_dict = list_connections_response_instance.to_dict()
# create an instance of ListConnectionsResponse from a dict
list_connections_response_from_dict = ListConnectionsResponse.from_dict(list_connections_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


