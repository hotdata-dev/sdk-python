# ListEmbeddingProvidersResponse

Response body for GET /embedding-providers

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**embedding_providers** | [**List[EmbeddingProviderResponse]**](EmbeddingProviderResponse.md) |  | 

## Example

```python
from hotdata.models.list_embedding_providers_response import ListEmbeddingProvidersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListEmbeddingProvidersResponse from a JSON string
list_embedding_providers_response_instance = ListEmbeddingProvidersResponse.from_json(json)
# print the JSON string representation of the object
print(ListEmbeddingProvidersResponse.to_json())

# convert the object into a dict
list_embedding_providers_response_dict = list_embedding_providers_response_instance.to_dict()
# create an instance of ListEmbeddingProvidersResponse from a dict
list_embedding_providers_response_from_dict = ListEmbeddingProvidersResponse.from_dict(list_embedding_providers_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


