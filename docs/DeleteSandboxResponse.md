# DeleteSandboxResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ok** | **bool** |  | 
**deleted** | **bool** |  | 

## Example

```python
from hotdata.models.delete_sandbox_response import DeleteSandboxResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteSandboxResponse from a JSON string
delete_sandbox_response_instance = DeleteSandboxResponse.from_json(json)
# print the JSON string representation of the object
print(DeleteSandboxResponse.to_json())

# convert the object into a dict
delete_sandbox_response_dict = delete_sandbox_response_instance.to_dict()
# create an instance of DeleteSandboxResponse from a dict
delete_sandbox_response_from_dict = DeleteSandboxResponse.from_dict(delete_sandbox_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


