# GetSecretResponse

Response body for GET /secrets/{name}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**name** | **str** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from hotdata.models.get_secret_response import GetSecretResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetSecretResponse from a JSON string
get_secret_response_instance = GetSecretResponse.from_json(json)
# print the JSON string representation of the object
print(GetSecretResponse.to_json())

# convert the object into a dict
get_secret_response_dict = get_secret_response_instance.to_dict()
# create an instance of GetSecretResponse from a dict
get_secret_response_from_dict = GetSecretResponse.from_dict(get_secret_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


