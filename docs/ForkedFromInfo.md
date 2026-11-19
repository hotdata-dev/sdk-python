# ForkedFromInfo

The database a fork was copied from. A fork is independent of its source: changing or deleting either does not affect the other.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**database_id** | **str** | ID of the source database. It may have been deleted since. | 
**description** | **str** | Why the fork was taken, if given. | [optional] 
**forked_at** | **datetime** | When the fork was taken. | [optional] 
**name** | **str** | Name of the source when the fork was taken. | [optional] 
**snapshot_id** | **int** | Point in time of the source data that the fork copied. Not a revision count: two forks of an unchanged source get different values. | [optional] 

## Example

```python
from hotdata.models.forked_from_info import ForkedFromInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ForkedFromInfo from a JSON string
forked_from_info_instance = ForkedFromInfo.from_json(json)
# print the JSON string representation of the object
print(ForkedFromInfo.to_json())

# convert the object into a dict
forked_from_info_dict = forked_from_info_instance.to_dict()
# create an instance of ForkedFromInfo from a dict
forked_from_info_from_dict = ForkedFromInfo.from_dict(forked_from_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


