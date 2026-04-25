# UpdateSandboxRequest

Partial update — only the provided fields are changed.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**markdown** | **str** |  | [optional] 

## Example

```python
from hotdata.models.update_sandbox_request import UpdateSandboxRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateSandboxRequest from a JSON string
update_sandbox_request_instance = UpdateSandboxRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateSandboxRequest.to_json())

# convert the object into a dict
update_sandbox_request_dict = update_sandbox_request_instance.to_dict()
# create an instance of UpdateSandboxRequest from a dict
update_sandbox_request_from_dict = UpdateSandboxRequest.from_dict(update_sandbox_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


