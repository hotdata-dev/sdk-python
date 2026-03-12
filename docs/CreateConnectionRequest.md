# CreateConnectionRequest

Request body for POST /connections

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | **object** |  | 
**name** | **str** |  | 
**secret_id** | **object** | Optional reference to a secret by ID (e.g., \&quot;secr_abc123\&quot;). If provided, this secret will be used for authentication. Mutually exclusive with &#x60;secret_name&#x60;. | [optional] 
**secret_name** | **object** | Optional reference to a secret by name. If provided, this secret will be used for authentication. Mutually exclusive with &#x60;secret_id&#x60;. | [optional] 
**source_type** | **str** |  | 

## Example

```python
from hotdata.models.create_connection_request import CreateConnectionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConnectionRequest from a JSON string
create_connection_request_instance = CreateConnectionRequest.from_json(json)
# print the JSON string representation of the object
print(CreateConnectionRequest.to_json())

# convert the object into a dict
create_connection_request_dict = create_connection_request_instance.to_dict()
# create an instance of CreateConnectionRequest from a dict
create_connection_request_from_dict = CreateConnectionRequest.from_dict(create_connection_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


