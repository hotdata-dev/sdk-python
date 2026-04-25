# ListSandboxesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ok** | **bool** |  | 
**sandboxes** | [**List[Sandbox]**](Sandbox.md) |  | 

## Example

```python
from hotdata.models.list_sandboxes_response import ListSandboxesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListSandboxesResponse from a JSON string
list_sandboxes_response_instance = ListSandboxesResponse.from_json(json)
# print the JSON string representation of the object
print(ListSandboxesResponse.to_json())

# convert the object into a dict
list_sandboxes_response_dict = list_sandboxes_response_instance.to_dict()
# create an instance of ListSandboxesResponse from a dict
list_sandboxes_response_from_dict = ListSandboxesResponse.from_dict(list_sandboxes_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


