# ListWorkspaceContextsResponse

Response body for GET `/v1/context`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contexts** | [**List[WorkspaceContextEntry]**](WorkspaceContextEntry.md) |  | 

## Example

```python
from hotdata.models.list_workspace_contexts_response import ListWorkspaceContextsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListWorkspaceContextsResponse from a JSON string
list_workspace_contexts_response_instance = ListWorkspaceContextsResponse.from_json(json)
# print the JSON string representation of the object
print(ListWorkspaceContextsResponse.to_json())

# convert the object into a dict
list_workspace_contexts_response_dict = list_workspace_contexts_response_instance.to_dict()
# create an instance of ListWorkspaceContextsResponse from a dict
list_workspace_contexts_response_from_dict = ListWorkspaceContextsResponse.from_dict(list_workspace_contexts_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


