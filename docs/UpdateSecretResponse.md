# UpdateSecretResponse

Response body for PUT /secrets/{name}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from hotdata.models.update_secret_response import UpdateSecretResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateSecretResponse from a JSON string
update_secret_response_instance = UpdateSecretResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateSecretResponse.to_json())

# convert the object into a dict
update_secret_response_dict = update_secret_response_instance.to_dict()
# create an instance of UpdateSecretResponse from a dict
update_secret_response_from_dict = UpdateSecretResponse.from_dict(update_secret_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


