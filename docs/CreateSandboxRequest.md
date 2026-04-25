# CreateSandboxRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Human-readable name for the sandbox. | [optional] 
**markdown** | **str** | Optional markdown notes. | [optional] 

## Example

```python
from hotdata.models.create_sandbox_request import CreateSandboxRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSandboxRequest from a JSON string
create_sandbox_request_instance = CreateSandboxRequest.from_json(json)
# print the JSON string representation of the object
print(CreateSandboxRequest.to_json())

# convert the object into a dict
create_sandbox_request_dict = create_sandbox_request_instance.to_dict()
# create an instance of CreateSandboxRequest from a dict
create_sandbox_request_from_dict = CreateSandboxRequest.from_dict(create_sandbox_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


