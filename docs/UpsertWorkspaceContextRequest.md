# UpsertWorkspaceContextRequest

Request body for POST `/v1/context`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** |  | 
**name** | **str** | Unique name in the catalog (upsert key). Same field as in list/get responses. | 

## Example

```python
from hotdata.models.upsert_workspace_context_request import UpsertWorkspaceContextRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpsertWorkspaceContextRequest from a JSON string
upsert_workspace_context_request_instance = UpsertWorkspaceContextRequest.from_json(json)
# print the JSON string representation of the object
print(UpsertWorkspaceContextRequest.to_json())

# convert the object into a dict
upsert_workspace_context_request_dict = upsert_workspace_context_request_instance.to_dict()
# create an instance of UpsertWorkspaceContextRequest from a dict
upsert_workspace_context_request_from_dict = UpsertWorkspaceContextRequest.from_dict(upsert_workspace_context_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


