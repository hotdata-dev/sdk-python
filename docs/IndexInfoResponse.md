# IndexInfoResponse

Result payload for a `create_index` job, and response for index endpoints.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**algorithm** | **str** | How this vector index organises the vectors it searches: &#x60;hnsw&#x60; or &#x60;ivf&#x60;. Absent for BM25 and sorted indexes. | [optional] 
**columns** | **List[str]** |  | 
**created_at** | **datetime** |  | 
**index_name** | **str** |  | 
**index_type** | **str** |  | 
**metric** | **str** | Distance metric this index was built with. Only present for vector indexes. | [optional] 
**nlist** | **int** | Number of clusters an &#x60;ivf&#x60; index was built with. This can be smaller than the &#x60;nlist&#x60; requested when the index was created, because the number is capped by how many vectors the clusters were fitted to. Absent for every other kind of index. | [optional] 
**probe_fraction** | **float** | How much of an &#x60;ivf&#x60; index a search reads, as a fraction greater than 0 and at most 1, when the index was created with one. When absent, the server chooses how much each search reads: a width measured on this index&#39;s own data when it was built, scaled to the number of results a search asks for, or a server default when no measurement could be made. Absent for every other kind of index. | [optional] 
**source_column** | **str** | Source text column for an embedding-backed vector index. A query searches it via &#x60;vector_distance(&lt;source_column&gt;, …)&#x60;; the indexed &#x60;columns&#x60; hold the generated embedding column instead. Absent for BM25, sorted, and direct (existing-column) vector indexes. | [optional] 
**status** | [**IndexStatus**](IndexStatus.md) |  | 
**updated_at** | **datetime** |  | 
**vector_precision** | **str** | How precisely this vector index stores each number of a vector. Always present for an &#x60;ivf&#x60; index, which stores &#x60;int8&#x60; unless it was created with another precision. For an &#x60;hnsw&#x60; index it is present only when the index was created with an explicit precision; absent means it stores at the same precision as the column. Absent for BM25 and sorted indexes. | [optional] 

## Example

```python
from hotdata.models.index_info_response import IndexInfoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of IndexInfoResponse from a JSON string
index_info_response_instance = IndexInfoResponse.from_json(json)
# print the JSON string representation of the object
print(IndexInfoResponse.to_json())

# convert the object into a dict
index_info_response_dict = index_info_response_instance.to_dict()
# create an instance of IndexInfoResponse from a dict
index_info_response_from_dict = IndexInfoResponse.from_dict(index_info_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


