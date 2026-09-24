# LineageAncestorInfo

One database up a fork chain.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**database_id** | **str** |  | 
**description** | **str** | Why the next database down the chain was forked from it, as given at the time. Absent when none was given. | [optional] 
**exists** | **bool** | False once the ancestor has been deleted. Its place in the chain is kept either way, and the ancestry continues past it. | 
**forked_at** | **datetime** | When the next database down the chain was forked from it. | [optional] 
**name** | **str** | The ancestor&#39;s current label, or the one captured at fork time when it no longer exists. | [optional] 
**snapshot_id** | **int** | Version of this ancestor&#39;s data that the next database down the chain copied. See &#x60;forked_from.snapshot_id&#x60;. | [optional] 

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


