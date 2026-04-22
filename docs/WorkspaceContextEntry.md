# WorkspaceContextEntry

One context entry returned by the API.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** |  | 
**name** | **str** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from hotdata.models.workspace_context_entry import WorkspaceContextEntry

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceContextEntry from a JSON string
workspace_context_entry_instance = WorkspaceContextEntry.from_json(json)
# print the JSON string representation of the object
print(WorkspaceContextEntry.to_json())

# convert the object into a dict
workspace_context_entry_dict = workspace_context_entry_instance.to_dict()
# create an instance of WorkspaceContextEntry from a dict
workspace_context_entry_from_dict = WorkspaceContextEntry.from_dict(workspace_context_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


