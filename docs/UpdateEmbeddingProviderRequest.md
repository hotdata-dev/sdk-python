# UpdateEmbeddingProviderRequest

Request body for PUT /embedding-providers/{id}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_key** | **str** | New API key. Hotdata stores it as a secret for you. | [optional] 
**config** | **object** |  | [optional] 
**name** | **str** |  | [optional] 
**secret_name** | **str** | Name of a stored secret that holds the API key. Send &#x60;null&#x60; to remove the key from the provider. | [optional] 

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


