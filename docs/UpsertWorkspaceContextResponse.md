# UpsertWorkspaceContextResponse

Response body for POST `/v1/context`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**context** | [**WorkspaceContextEntry**](WorkspaceContextEntry.md) |  | 

## Example

```python
from hotdata.models.upsert_workspace_context_response import UpsertWorkspaceContextResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpsertWorkspaceContextResponse from a JSON string
upsert_workspace_context_response_instance = UpsertWorkspaceContextResponse.from_json(json)
# print the JSON string representation of the object
print(UpsertWorkspaceContextResponse.to_json())

# convert the object into a dict
upsert_workspace_context_response_dict = upsert_workspace_context_response_instance.to_dict()
# create an instance of UpsertWorkspaceContextResponse from a dict
upsert_workspace_context_response_from_dict = UpsertWorkspaceContextResponse.from_dict(upsert_workspace_context_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


