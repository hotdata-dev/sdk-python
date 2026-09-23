# LineageForkInfo

One database forked directly from the one being asked about.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**database_id** | **str** |  | 
**description** | **str** | Why the fork was taken, as given when it was created. Absent when none was given. | [optional] 
**exists** | **bool** | False once the fork has been deleted. The record of it is kept either way, so a source can still account for everything taken from it. | 
**forked_at** | **datetime** | When the fork was taken. | [optional] 
**name** | **str** | Absent once the fork has been deleted — only the record of it remains. | [optional] 
**snapshot_id** | **int** | Version of this database&#39;s data that the fork copied. See &#x60;forked_from.snapshot_id&#x60;. | [optional] 

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


