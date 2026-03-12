# SecretMetadataResponse

Single secret metadata for API responses

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**name** | **str** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from hotdata.models.secret_metadata_response import SecretMetadataResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SecretMetadataResponse from a JSON string
secret_metadata_response_instance = SecretMetadataResponse.from_json(json)
# print the JSON string representation of the object
print(SecretMetadataResponse.to_json())

# convert the object into a dict
secret_metadata_response_dict = secret_metadata_response_instance.to_dict()
# create an instance of SecretMetadataResponse from a dict
secret_metadata_response_from_dict = SecretMetadataResponse.from_dict(secret_metadata_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


