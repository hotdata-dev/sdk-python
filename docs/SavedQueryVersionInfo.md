# SavedQueryVersionInfo

Single saved query version

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **object** |  | [optional] 
**created_at** | **datetime** |  | 
**has_aggregation** | **object** |  | [optional] 
**has_group_by** | **object** |  | [optional] 
**has_join** | **object** |  | [optional] 
**has_limit** | **object** |  | [optional] 
**has_order_by** | **object** |  | [optional] 
**has_predicate** | **object** |  | [optional] 
**num_tables** | **object** |  | [optional] 
**sql** | **str** |  | 
**sql_hash** | **str** |  | 
**table_size** | **object** |  | [optional] 
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


