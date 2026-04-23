# GetWorkspaceContextResponse

Response body for GET `/v1/context/{name}`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**context** | [**WorkspaceContextEntry**](WorkspaceContextEntry.md) |  | 

## Example

```python
from hotdata.models.get_workspace_context_response import GetWorkspaceContextResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetWorkspaceContextResponse from a JSON string
get_workspace_context_response_instance = GetWorkspaceContextResponse.from_json(json)
# print the JSON string representation of the object
print(GetWorkspaceContextResponse.to_json())

# convert the object into a dict
get_workspace_context_response_dict = get_workspace_context_response_instance.to_dict()
# create an instance of GetWorkspaceContextResponse from a dict
get_workspace_context_response_from_dict = GetWorkspaceContextResponse.from_dict(get_workspace_context_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


