# CreateIndexRequest

Request body for POST .../indexes  One constraint spans the whole table rather than this request alone: a vector index that generates its own embeddings — that is, one created with `embedding_provider_id` — has to be the only index on its table. So a table that already carries any index (sorted, full-text, or vector) will not accept an embedding-backed vector index, and a table that already carries an embedding-backed vector index will not accept any further index of any type. To move between the two arrangements, drop what is there first. Plan for it when designing a table: combining full-text search with generated embeddings on one table is not possible, so use a separate table for the second index, or supply the embeddings yourself.  A vector index over a column that already holds vectors — no `embedding_provider_id` — is not affected and coexists with other indexes normally.  Embedding generation also rewrites the table to add its generated column, and that rewrite cannot preserve a declared partition or sort order. An embedding-backed vector index is therefore refused on a table declaring either.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_async** | **bool** | When true, create the index as a background job and return a job ID for polling. | [optional] [default to False]
**async_after_ms** | **int** | If set (requires &#x60;async&#x60; &#x3D; true), wait up to this many milliseconds for the index build to finish: if it completes in time the index is returned (201), otherwise a 202 with a job ID to poll. Must be between 1000 and the server maximum; a value out of that range, or set without &#x60;async&#x60; &#x3D; true, is rejected with 400. | [optional] 
**columns** | **List[str]** | Columns to index. Required for all index types. | 
**description** | **str** | User-facing description of the embedding (e.g., \&quot;product descriptions\&quot;). | [optional] 
**dimensions** | **int** | Output vector dimensions. Some models support multiple dimension sizes (e.g., OpenAI text-embedding-3-small supports 512 or 1536). If omitted, the model&#39;s default dimensions are used | [optional] 
**embedding_provider_id** | **str** | Embedding provider ID. When set for a vector index, the source column is treated as text and embeddings are generated automatically. The vector index is then built on the generated embedding column (&#x60;{column}_embedding&#x60; by default). | [optional] 
**index_name** | **str** |  | 
**index_type** | **str** | Index type. &#x60;sorted&#x60; supports range queries, &#x60;bm25&#x60; full-text search, and &#x60;vector&#x60; similarity search. | [optional] [default to 'sorted']
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


