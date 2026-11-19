# IndexInfoResponse

An index on a table.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**algorithm** | **str** | Vector index algorithm: &#x60;hnsw&#x60; or &#x60;ivf&#x60;. Absent for other index types. | [optional] 
**columns** | **List[str]** | Indexed columns. | 
**created_at** | **datetime** | When the index was created. | 
**index_name** | **str** | Index name. | 
**index_type** | **str** | Index type: &#x60;sorted&#x60;, &#x60;bm25&#x60; or &#x60;vector&#x60;. | 
**metric** | **str** | Distance metric of a vector index. Absent for other index types. | [optional] 
**nlist** | **int** | Number of clusters an &#x60;ivf&#x60; index was built with. Can be lower than the requested &#x60;nlist&#x60;, because it is capped by the number of vectors the clusters were fitted to. | [optional] 
**probe_fraction** | **float** | Share of an &#x60;ivf&#x60; index each search reads, from 0 (exclusive) to 1, when set at creation. When absent, Hotdata picks the share for each search. | [optional] 
**source_column** | **str** | Text column an embedding-based vector index was built from; search it with &#x60;vector_distance(&lt;source_column&gt;, …)&#x60;. &#x60;columns&#x60; then holds the generated embedding column. Absent for other indexes. | [optional] 
**status** | [**IndexStatus**](IndexStatus.md) |  | 
**updated_at** | **datetime** | When the index was last updated. | 
**vector_precision** | **str** | Precision a vector index stores each number at, such as &#x60;int8&#x60;. Always set for &#x60;ivf&#x60; (default &#x60;int8&#x60;); for &#x60;hnsw&#x60;, set only when chosen at creation, and otherwise it matches the column. | [optional] 

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


