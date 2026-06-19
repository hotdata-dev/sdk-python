# IndexEntryResponse

One index in a cross-table listing: the per-table [`IndexInfoResponse`] plus the identity needed to know which table it belongs to.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **List[str]** |  | 
**created_at** | **datetime** |  | 
**index_name** | **str** |  | 
**index_type** | **str** |  | 
**metric** | **str** | Distance metric this index was built with. Only present for vector indexes. | [optional] 
**source_column** | **str** | Source text column for an embedding-backed vector index. A query searches it via &#x60;vector_distance(&lt;source_column&gt;, …)&#x60;; the indexed &#x60;columns&#x60; hold the generated embedding column instead. Absent for BM25, sorted, and direct (existing-column) vector indexes. | [optional] 
**status** | [**IndexStatus**](IndexStatus.md) |  | 
**updated_at** | **datetime** |  | 
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


