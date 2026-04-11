# CreateEmbeddingProviderResponse

Response body for POST /embedding-providers

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | **object** |  | 
**created_at** | **datetime** |  | 
**id** | **str** |  | 
**name** | **str** |  | 
**provider_type** | **str** |  | 

## Example

```python
from hotdata.models.create_embedding_provider_response import CreateEmbeddingProviderResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateEmbeddingProviderResponse from a JSON string
create_embedding_provider_response_instance = CreateEmbeddingProviderResponse.from_json(json)
# print the JSON string representation of the object
print(CreateEmbeddingProviderResponse.to_json())

# convert the object into a dict
create_embedding_provider_response_dict = create_embedding_provider_response_instance.to_dict()
# create an instance of CreateEmbeddingProviderResponse from a dict
create_embedding_provider_response_from_dict = CreateEmbeddingProviderResponse.from_dict(create_embedding_provider_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


