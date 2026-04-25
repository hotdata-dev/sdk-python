# SandboxResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ok** | **bool** |  | 
**sandbox** | [**Sandbox**](Sandbox.md) |  | 

## Example

```python
from hotdata.models.sandbox_response import SandboxResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SandboxResponse from a JSON string
sandbox_response_instance = SandboxResponse.from_json(json)
# print the JSON string representation of the object
print(SandboxResponse.to_json())

# convert the object into a dict
sandbox_response_dict = sandbox_response_instance.to_dict()
# create an instance of SandboxResponse from a dict
sandbox_response_from_dict = SandboxResponse.from_dict(sandbox_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


