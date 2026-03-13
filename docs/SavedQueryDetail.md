# SavedQueryDetail

Saved query detail (includes latest version's SQL)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **str** |  | [optional] 
**created_at** | **datetime** |  | 
**description** | **str** |  | 
**has_aggregation** | **bool** |  | [optional] 
**has_group_by** | **bool** |  | [optional] 
**has_join** | **bool** |  | [optional] 
**has_limit** | **bool** |  | [optional] 
**has_order_by** | **bool** |  | [optional] 
**has_predicate** | **bool** |  | [optional] 
**id** | **str** |  | 
**latest_version** | **int** |  | 
**name** | **str** |  | 
**num_tables** | **int** |  | [optional] 
**sql** | **str** |  | 
**sql_hash** | **str** |  | 
**table_size** | **str** |  | [optional] 
**tags** | **List[str]** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from hotdata.models.saved_query_detail import SavedQueryDetail

# TODO update the JSON string below
json = "{}"
# create an instance of SavedQueryDetail from a JSON string
saved_query_detail_instance = SavedQueryDetail.from_json(json)
# print the JSON string representation of the object
print(SavedQueryDetail.to_json())

# convert the object into a dict
saved_query_detail_dict = saved_query_detail_instance.to_dict()
# create an instance of SavedQueryDetail from a dict
saved_query_detail_from_dict = SavedQueryDetail.from_dict(saved_query_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


