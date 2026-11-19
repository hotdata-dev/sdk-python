# CreateEmbeddingProviderRequest

Request body for POST /embedding-providers

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_key** | **str** | API key. Hotdata stores it as a secret for you. Cannot be combined with &#x60;secret_name&#x60;. | [optional] 
**config** | **Dict[str, object]** | Provider settings, such as &#x60;model&#x60;, &#x60;base_url&#x60; and &#x60;dimensions&#x60;. | [optional] 
**name** | **str** |  | 
**provider_type** | **str** | Provider type. Only &#x60;service&#x60; (a hosted embedding API) is supported. | 
**secret_name** | **str** | Name of a stored secret that holds the API key. It is only sent to approved endpoints (by default, OpenAI&#39;s API); for other endpoints use &#x60;api_key&#x60;. | [optional] 

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


