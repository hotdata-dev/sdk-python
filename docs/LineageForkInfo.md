# LineageForkInfo

A database forked directly from this one.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**database_id** | **str** |  | 
**description** | **str** | Why the fork was taken, if given. | [optional] 
**exists** | **bool** | False if the fork has been deleted. | 
**forked_at** | **datetime** | When the fork was taken. | [optional] 
**name** | **str** | The fork&#39;s name. Absent once the fork is deleted. | [optional] 
**snapshot_id** | **int** | Point in time of this database&#39;s data that the fork copied. | [optional] 

## Example

```python
from hotdata.models.lineage_fork_info import LineageForkInfo

# TODO update the JSON string below
json = "{}"
# create an instance of LineageForkInfo from a JSON string
lineage_fork_info_instance = LineageForkInfo.from_json(json)
# print the JSON string representation of the object
print(LineageForkInfo.to_json())

# convert the object into a dict
lineage_fork_info_dict = lineage_fork_info_instance.to_dict()
# create an instance of LineageForkInfo from a dict
lineage_fork_info_from_dict = LineageForkInfo.from_dict(lineage_fork_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


