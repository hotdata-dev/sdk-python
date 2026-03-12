# ConnectionRefreshResult

Response for connection-wide data refresh

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_id** | **str** |  | 
**duration_ms** | **int** |  | 
**errors** | [**List[TableRefreshError]**](TableRefreshError.md) |  | 
**tables_failed** | **int** |  | 
**tables_refreshed** | **int** |  | 
**total_rows** | **int** |  | 
**warnings** | [**List[RefreshWarning]**](RefreshWarning.md) |  | [optional] 

## Example

```python
from hotdata.models.connection_refresh_result import ConnectionRefreshResult

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectionRefreshResult from a JSON string
connection_refresh_result_instance = ConnectionRefreshResult.from_json(json)
# print the JSON string representation of the object
print(ConnectionRefreshResult.to_json())

# convert the object into a dict
connection_refresh_result_dict = connection_refresh_result_instance.to_dict()
# create an instance of ConnectionRefreshResult from a dict
connection_refresh_result_from_dict = ConnectionRefreshResult.from_dict(connection_refresh_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


