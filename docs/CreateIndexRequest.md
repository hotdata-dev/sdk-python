# CreateIndexRequest

An index to create on a table.  Limits: a table can have only one vector index. A vector index with `embedding_provider_id` must be the only index on its table and cannot be created on a partitioned table. No index can be created on a table with `sorted_by`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**algorithm** | **str** | How a vector index is built. Defaults to &#x60;hnsw&#x60;.  &#x60;hnsw&#x60;: a graph kept in memory. Very fast searches, but memory grows with the table, so very large tables cannot be served.  &#x60;ivf&#x60;: vectors grouped into clusters; a search reads only the nearest clusters. Slower than &#x60;hnsw&#x60;, but memory follows how much of the index a search reads, so it works for much larger tables. It stores a copy of the table&#39;s rows, which uses extra storage. Supports the &#x60;l2&#x60; and &#x60;cosine&#x60; metrics. Search it with &#x60;ORDER BY vector_distance(column, &#39;&lt;query&gt;&#39;) LIMIT &lt;k&gt;&#x60; and name the columns to return instead of &#x60;*&#x60;; &#x60;vector_search&#x60; works only with &#x60;hnsw&#x60;. Generating embeddings for tens of millions of rows is not supported yet. | [optional] 
**var_async** | **bool** | Build the index in the background and return a job ID to poll. | [optional] [default to False]
**async_after_ms** | **int** | With &#x60;async: true&#x60;, wait up to this many milliseconds for the build before falling back to a job ID. Must be between 1000 and 30000. | [optional] 
**columns** | **List[str]** | Columns to index. | 
**description** | **str** | Description of what the embeddings represent, such as \&quot;product descriptions\&quot;. | [optional] 
**dimensions** | **int** | Vector size to request from the embedding model, for models that support more than one. Defaults to the model&#39;s own size. | [optional] 
**embedding_provider_id** | **str** | Embedding provider that turns the text column into vectors. The vectors are stored in a new column, and later loads and searches use the same provider. With &#x60;ivf&#x60;, the metric must be &#x60;l2&#x60; or &#x60;cosine&#x60;. | [optional] 
**index_name** | **str** |  | 
**index_type** | **str** | Index type. &#x60;sorted&#x60; supports range queries, &#x60;bm25&#x60; full-text search, and &#x60;vector&#x60; similarity search. | [optional] [default to 'sorted']
**metric** | **str** | Distance metric for a vector index: &#x60;l2&#x60;, &#x60;cosine&#x60; or &#x60;dot&#x60;. Defaults to &#x60;l2&#x60;, or to the embedding provider&#39;s metric when &#x60;embedding_provider_id&#x60; is set. | [optional] 
**nlist** | **int** | For &#x60;ivf&#x60;: number of clusters to group the vectors into. More clusters means each search reads less data. Defaults to a value based on the table size. | [optional] 
**output_column** | **str** | Name of the generated vector column. Defaults to &#x60;{column}_embedding&#x60;. | [optional] 
**probe_fraction** | **float** | For &#x60;ivf&#x60;: share of the index each search reads, above 0 and up to 1. Higher is more accurate and slower. | [optional] 
**vector_precision** | **str** | How precisely a vector index stores each number. Lower precision makes the index smaller, so it needs less memory, and for &#x60;ivf&#x60; makes each search read less. Defaults to the column&#39;s own precision for &#x60;hnsw&#x60;, and &#x60;int8&#x60; for &#x60;ivf&#x60;. To change it, drop and recreate the index; the table&#39;s data is never changed.  &#x60;ivf&#x60; accepts &#x60;int8&#x60; and &#x60;float32&#x60; only. &#x60;hnsw&#x60; accepts every value except &#x60;int8&#x60;.  Accuracy figures below come from benchmarks; test on your own data.  &#x60;float64&#x60;: only for columns that already hold 64-bit values.  &#x60;float32&#x60;: half the size of &#x60;float64&#x60;, with no loss for the usual 32-bit embeddings.  &#x60;float16&#x60;: half the size of &#x60;float32&#x60;; results within 0.1 percentage points of &#x60;float32&#x60; on 1536-dimension text embeddings with cosine distance.  &#x60;float8&#x60;: a quarter of the size of &#x60;float32&#x60;; about 4 percentage points less accurate on the same test, which a wider search does not recover.  &#x60;int8&#x60;: a quarter of the size of &#x60;float32&#x60;. A search of every cluster finds about 99.5% of the true neighbours; the default search finds fewer (see &#x60;probe_fraction&#x60;). With &#x60;l2&#x60;, accuracy drops when vector lengths vary widely (about 93% when the longest is 16 times the shortest); use &#x60;float32&#x60; if that matters. | [optional] 

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


