# RefreshResponse

Unified response type for refresh operations

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connections_failed** | **int** |  | 
**connections_refreshed** | **int** |  | 
**errors** | [**List[TableRefreshError]**](TableRefreshError.md) |  | 
**tables_added** | **int** |  | 
**tables_discovered** | **int** |  | 
**tables_modified** | **int** |  | 
**connection_id** | **str** |  | 
**duration_ms** | **int** |  | 
**rows_synced** | **int** |  | 
**schema_name** | **str** |  | 
**table_name** | **str** |  | 
**warnings** | [**List[RefreshWarning]**](RefreshWarning.md) |  | [optional] 
**tables_failed** | **int** |  | 
**tables_refreshed** | **int** |  | 
**total_rows** | **int** |  | 
**created_at** | **datetime** |  | 
**id** | **str** | Job ID for status polling. | 
**status** | **str** | Current status: \&quot;pending\&quot; or \&quot;running\&quot;. | 
**version** | **int** |  | 
**status_url** | **str** | URL to poll for job status. | 

## Example

```python
from hotdata.models.refresh_response import RefreshResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RefreshResponse from a JSON string
refresh_response_instance = RefreshResponse.from_json(json)
# print the JSON string representation of the object
print(RefreshResponse.to_json())

# convert the object into a dict
refresh_response_dict = refresh_response_instance.to_dict()
# create an instance of RefreshResponse from a dict
refresh_response_from_dict = RefreshResponse.from_dict(refresh_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


