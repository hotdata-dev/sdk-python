# CreateIndexRequest

Request body for POST .../indexes

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_async** | **bool** | When true, create the index as a background job and return a job ID for polling. | [optional] 
**columns** | **List[str]** | Columns to index. Required for all index types. | 
**description** | **str** | User-facing description of the embedding (e.g., \&quot;product descriptions\&quot;). | [optional] 
**dimensions** | **int** | Output vector dimensions. Some models support multiple dimension sizes (e.g., OpenAI text-embedding-3-small supports 512 or 1536). If omitted, the model&#39;s default dimensions are used. | [optional] 
**embedding_provider_id** | **str** | Embedding provider ID. When set for a vector index, the source column is treated as text and embeddings are generated automatically. The vector index is then built on the generated embedding column (&#x60;{column}_embedding&#x60; by default). | [optional] 
**index_name** | **str** |  | 
**index_type** | **str** | Index type: \&quot;sorted\&quot; (default), \&quot;bm25\&quot; (full text search), or \&quot;vector\&quot; | [optional] 
**metric** | **str** | Distance metric for vector indexes: \&quot;l2\&quot;, \&quot;cosine\&quot;, or \&quot;dot\&quot;. When omitted, defaults to \&quot;l2\&quot; for float array columns or the provider&#39;s preferred metric for text columns with auto-embedding. | [optional] 
**output_column** | **str** | Custom name for the generated embedding column. Defaults to &#x60;{column}_embedding&#x60;. | [optional] 

## Example

```python
from hotdata.models.create_index_request import CreateIndexRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateIndexRequest from a JSON string
create_index_request_instance = CreateIndexRequest.from_json(json)
# print the JSON string representation of the object
print(CreateIndexRequest.to_json())

# convert the object into a dict
create_index_request_dict = create_index_request_instance.to_dict()
# create an instance of CreateIndexRequest from a dict
create_index_request_from_dict = CreateIndexRequest.from_dict(create_index_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


