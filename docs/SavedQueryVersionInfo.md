# SavedQueryVersionInfo

Single saved query version

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **str** |  | [optional] 
**created_at** | **datetime** |  | 
**has_aggregation** | **bool** |  | [optional] 
**has_group_by** | **bool** |  | [optional] 
**has_join** | **bool** |  | [optional] 
**has_limit** | **bool** |  | [optional] 
**has_order_by** | **bool** |  | [optional] 
**has_predicate** | **bool** |  | [optional] 
**num_tables** | **int** |  | [optional] 
**sql** | **str** |  | 
**sql_hash** | **str** |  | 
**table_size** | **str** |  | [optional] 
**version** | **int** |  | 

## Example

```python
from hotdata.models.saved_query_version_info import SavedQueryVersionInfo

# TODO update the JSON string below
json = "{}"
# create an instance of SavedQueryVersionInfo from a JSON string
saved_query_version_info_instance = SavedQueryVersionInfo.from_json(json)
# print the JSON string representation of the object
print(SavedQueryVersionInfo.to_json())

# convert the object into a dict
saved_query_version_info_dict = saved_query_version_info_instance.to_dict()
# create an instance of SavedQueryVersionInfo from a dict
saved_query_version_info_from_dict = SavedQueryVersionInfo.from_dict(saved_query_version_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


