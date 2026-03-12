# ListSecretsResponse

Response body for GET /secrets

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**secrets** | [**List[SecretMetadataResponse]**](SecretMetadataResponse.md) |  | 

## Example

```python
from hotdata.models.list_secrets_response import ListSecretsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListSecretsResponse from a JSON string
list_secrets_response_instance = ListSecretsResponse.from_json(json)
# print the JSON string representation of the object
print(ListSecretsResponse.to_json())

# convert the object into a dict
list_secrets_response_dict = list_secrets_response_instance.to_dict()
# create an instance of ListSecretsResponse from a dict
list_secrets_response_from_dict = ListSecretsResponse.from_dict(list_secrets_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


