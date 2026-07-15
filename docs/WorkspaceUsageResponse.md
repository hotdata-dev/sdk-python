# WorkspaceUsageResponse

Response for GET /v1/usage

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bytes_scanned** | **int** | Sum of &#x60;bytes_scanned&#x60; across all completed/failed query runs since &#x60;since&#x60;. Null bytes (queries that touched no row data) contribute 0. | 
**query_count** | **int** | Number of query runs (succeeded + failed) since &#x60;since&#x60;. | 
**since** | **datetime** | The period start used for this response (echoed back for the caller to verify). | 
**storage_bytes** | **int** | The workspace&#39;s current stored-data footprint in bytes, measured at request time: managed-database data, plus un-consumed uploads, connection caches, and search-index artifacts. | 
**storage_captured_at** | **datetime** | When &#x60;storage_bytes&#x60; was measured (the time this response was produced). | [optional] 

## Example

```python
from hotdata.models.workspace_usage_response import WorkspaceUsageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceUsageResponse from a JSON string
workspace_usage_response_instance = WorkspaceUsageResponse.from_json(json)
# print the JSON string representation of the object
print(WorkspaceUsageResponse.to_json())

# convert the object into a dict
workspace_usage_response_dict = workspace_usage_response_instance.to_dict()
# create an instance of WorkspaceUsageResponse from a dict
workspace_usage_response_from_dict = WorkspaceUsageResponse.from_dict(workspace_usage_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


