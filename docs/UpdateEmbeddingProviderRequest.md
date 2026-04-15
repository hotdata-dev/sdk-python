# UpdateEmbeddingProviderRequest

Request body for PUT /embedding-providers/{id}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_key** | **str** | Inline API key. If provided, updates (or creates) the auto-managed secret. | [optional] 
**config** | **object** |  | [optional] 
**name** | **str** |  | [optional] 
**secret_name** | **str** | Secret name containing the API key. Pass null to clear. | [optional] 

## Example

```python
from hotdata.models.update_embedding_provider_request import UpdateEmbeddingProviderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateEmbeddingProviderRequest from a JSON string
update_embedding_provider_request_instance = UpdateEmbeddingProviderRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateEmbeddingProviderRequest.to_json())

# convert the object into a dict
update_embedding_provider_request_dict = update_embedding_provider_request_instance.to_dict()
# create an instance of UpdateEmbeddingProviderRequest from a dict
update_embedding_provider_request_from_dict = UpdateEmbeddingProviderRequest.from_dict(update_embedding_provider_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


