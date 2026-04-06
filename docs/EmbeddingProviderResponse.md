# EmbeddingProviderResponse

Single embedding provider for API responses

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | **object** |  | 
**created_at** | **datetime** |  | 
**has_secret** | **bool** |  | 
**id** | **str** |  | 
**name** | **str** |  | 
**provider_type** | **str** |  | 
**source** | **str** | Provider source: \&quot;system\&quot; (from config) or \&quot;user\&quot; (created via API). | 
**updated_at** | **datetime** |  | 

## Example

```python
from hotdata.models.embedding_provider_response import EmbeddingProviderResponse

# TODO update the JSON string below
json = "{}"
# create an instance of EmbeddingProviderResponse from a JSON string
embedding_provider_response_instance = EmbeddingProviderResponse.from_json(json)
# print the JSON string representation of the object
print(EmbeddingProviderResponse.to_json())

# convert the object into a dict
embedding_provider_response_dict = embedding_provider_response_instance.to_dict()
# create an instance of EmbeddingProviderResponse from a dict
embedding_provider_response_from_dict = EmbeddingProviderResponse.from_dict(embedding_provider_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


