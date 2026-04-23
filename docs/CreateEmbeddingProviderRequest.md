# CreateEmbeddingProviderRequest

Request body for POST /embedding-providers

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_key** | **str** | Inline API key. If provided, a secret is auto-created and referenced. Cannot be used together with &#x60;secret_name&#x60;. | [optional] 
**config** | **object** |  | [optional] 
**name** | **str** |  | 
**provider_type** | **str** | Provider type: \&quot;local\&quot; or \&quot;service\&quot; | 
**secret_name** | **str** | Reference an existing secret by name (for service providers). | [optional] 

## Example

```python
from hotdata.models.create_embedding_provider_request import CreateEmbeddingProviderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateEmbeddingProviderRequest from a JSON string
create_embedding_provider_request_instance = CreateEmbeddingProviderRequest.from_json(json)
# print the JSON string representation of the object
print(CreateEmbeddingProviderRequest.to_json())

# convert the object into a dict
create_embedding_provider_request_dict = create_embedding_provider_request_instance.to_dict()
# create an instance of CreateEmbeddingProviderRequest from a dict
create_embedding_provider_request_from_dict = CreateEmbeddingProviderRequest.from_dict(create_embedding_provider_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


