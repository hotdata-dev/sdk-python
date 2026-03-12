# WorkspaceListItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**public_id** | **str** |  | 
**name** | **str** |  | 
**active** | **bool** |  | 
**favorite** | **bool** |  | 
**provision_status** | **str** |  | 
**namespace** | **str** |  | 

## Example

```python
from hotdata.models.workspace_list_item import WorkspaceListItem

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceListItem from a JSON string
workspace_list_item_instance = WorkspaceListItem.from_json(json)
# print the JSON string representation of the object
print(WorkspaceListItem.to_json())

# convert the object into a dict
workspace_list_item_dict = workspace_list_item_instance.to_dict()
# create an instance of WorkspaceListItem from a dict
workspace_list_item_from_dict = WorkspaceListItem.from_dict(workspace_list_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


