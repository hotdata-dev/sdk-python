# WorkspaceDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**public_id** | **str** |  | 
**name** | **str** |  | 
**provision_status** | **str** |  | 
**namespace** | **str** |  | 

## Example

```python
from hotdata.models.workspace_detail import WorkspaceDetail

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceDetail from a JSON string
workspace_detail_instance = WorkspaceDetail.from_json(json)
# print the JSON string representation of the object
print(WorkspaceDetail.to_json())

# convert the object into a dict
workspace_detail_dict = workspace_detail_instance.to_dict()
# create an instance of WorkspaceDetail from a dict
workspace_detail_from_dict = WorkspaceDetail.from_dict(workspace_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


