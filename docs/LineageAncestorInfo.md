# LineageAncestorInfo

A database up the fork chain.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**database_id** | **str** |  | 
**description** | **str** | Why that fork was taken, if given. | [optional] 
**exists** | **bool** | False if the database has been deleted. | 
**forked_at** | **datetime** | When the next database down the chain was forked from this one. | [optional] 
**name** | **str** | The database&#39;s current name, or its name at fork time if deleted. | [optional] 
**snapshot_id** | **int** | Point in time of this database&#39;s data that the next database down the chain copied. | [optional] 

## Example

```python
from hotdata.models.lineage_ancestor_info import LineageAncestorInfo

# TODO update the JSON string below
json = "{}"
# create an instance of LineageAncestorInfo from a JSON string
lineage_ancestor_info_instance = LineageAncestorInfo.from_json(json)
# print the JSON string representation of the object
print(LineageAncestorInfo.to_json())

# convert the object into a dict
lineage_ancestor_info_dict = lineage_ancestor_info_instance.to_dict()
# create an instance of LineageAncestorInfo from a dict
lineage_ancestor_info_from_dict = LineageAncestorInfo.from_dict(lineage_ancestor_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


