# ConnectionHealthResponse

Response body for GET /connections/{connection_id}/health

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_id** | **str** |  | 
**error** | **str** |  | [optional] 
**healthy** | **bool** |  | 
**latency_ms** | **int** |  | 

## Example

```python
from hotdata.models.connection_health_response import ConnectionHealthResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectionHealthResponse from a JSON string
connection_health_response_instance = ConnectionHealthResponse.from_json(json)
# print the JSON string representation of the object
print(ConnectionHealthResponse.to_json())

# convert the object into a dict
connection_health_response_dict = connection_health_response_instance.to_dict()
# create an instance of ConnectionHealthResponse from a dict
connection_health_response_from_dict = ConnectionHealthResponse.from_dict(connection_health_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


