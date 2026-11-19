# WorkspaceUsageResponse

Query and storage usage for a workspace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bytes_scanned** | **int** | Total &#x60;bytes_scanned&#x60; of succeeded and failed query runs since &#x60;since&#x60;. Reads served from cache are not counted. | 
**query_count** | **int** | Number of succeeded and failed query runs since &#x60;since&#x60;. | 
**since** | **datetime** | Start of the period these totals cover. | 
**storage_bytes** | **int** | Bytes the workspace stores now: table data, uploads not yet loaded, and caches and indexes. | 
**storage_captured_at** | **datetime** | When &#x60;storage_bytes&#x60; was measured. | [optional] 

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


