# IndexEntryResponse

One index in a cross-table listing: the index itself plus the connection, schema, and table it belongs to.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**algorithm** | **str** | How this vector index organises the vectors it searches: &#x60;hnsw&#x60; or &#x60;ivf&#x60;. Absent for BM25 and sorted indexes. | [optional] 
**columns** | **List[str]** |  | 
**created_at** | **datetime** |  | 
**index_name** | **str** |  | 
**index_type** | **str** |  | 
**metric** | **str** | Distance metric this index was built with. Only present for vector indexes. | [optional] 
**probe_fraction** | **float** | How much of an &#x60;ivf&#x60; index a search reads, as a fraction greater than 0 and at most 1, when it was created with an explicit one. Absent means the server&#39;s default. Also absent for every other kind of index. | [optional] 
**source_column** | **str** | Source text column for an embedding-backed vector index. A query searches it via &#x60;vector_distance(&lt;source_column&gt;, …)&#x60;; the indexed &#x60;columns&#x60; hold the generated embedding column instead. Absent for BM25, sorted, and direct (existing-column) vector indexes. | [optional] 
**status** | [**IndexStatus**](IndexStatus.md) |  | 
**updated_at** | **datetime** |  | 
**vector_precision** | **str** | How precisely this vector index stores each number of a vector, when it was created with an explicit precision. Absent means it stores at the same precision as the column, which is the default. Also absent for BM25 and sorted indexes. | [optional] 
**connection_id** | **str** |  | [optional] 
**schema_name** | **str** |  | 
**table_name** | **str** |  | 

## Example

```python
from hotdata.models.index_entry_response import IndexEntryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of IndexEntryResponse from a JSON string
index_entry_response_instance = IndexEntryResponse.from_json(json)
# print the JSON string representation of the object
print(IndexEntryResponse.to_json())

# convert the object into a dict
index_entry_response_dict = index_entry_response_instance.to_dict()
# create an instance of IndexEntryResponse from a dict
index_entry_response_from_dict = IndexEntryResponse.from_dict(index_entry_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


