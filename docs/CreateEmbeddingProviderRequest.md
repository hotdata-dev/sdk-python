# CreateEmbeddingProviderRequest

Request body for POST /embedding-providers

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_key** | **str** | Inline API key. If provided, a secret is auto-created and referenced. Cannot be used together with &#x60;secret_name&#x60;. | [optional] 
**config** | **Dict[str, object]** | Provider-specific configuration (model name, base URL, dimensions, etc.) | [optional] 
**name** | **str** |  | 
**provider_type** | **str** | Provider type: \&quot;local\&quot; or \&quot;service\&quot; | 
**secret_name** | **str** | Reference an existing stored secret by name (for service providers).  A stored secret is only sent to an approved provider origin — by default OpenAI&#39;s public API. To use a different endpoint, supply the key inline with &#x60;api_key&#x60; instead, or ask your operator to approve the origin. | [optional] 

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


