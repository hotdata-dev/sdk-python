# UpdateEmbeddingProviderResponse

Response body for PUT /embedding-providers/{id}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from hotdata.models.update_embedding_provider_response import UpdateEmbeddingProviderResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateEmbeddingProviderResponse from a JSON string
update_embedding_provider_response_instance = UpdateEmbeddingProviderResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateEmbeddingProviderResponse.to_json())

# convert the object into a dict
update_embedding_provider_response_dict = update_embedding_provider_response_instance.to_dict()
# create an instance of UpdateEmbeddingProviderResponse from a dict
update_embedding_provider_response_from_dict = UpdateEmbeddingProviderResponse.from_dict(update_embedding_provider_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


