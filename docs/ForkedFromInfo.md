# ForkedFromInfo

Where a forked database came from, and which state of the source it copied.  Present only on a database that was created by forking another one. It is a record of how this database came to exist, not a live link: the fork and its source are independent from the moment the fork is created, and either can change or be deleted without affecting the other.  Forks created before lineage was recorded carry no `forked_from`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**database_id** | **str** | ID of the database that was forked. The database may since have been deleted — the record outlives it — so this is not guaranteed to resolve. | 
**forked_at** | **datetime** | When the fork was taken. | [optional] 
**name** | **str** | Display label the source carried when the fork was taken, kept so a deleted source still reads as more than an ID. | [optional] 
**snapshot_id** | **int** | Marks the version of the source that this fork copied — its table set and their contents as of that moment. It is a point in time rather than a per-database revision count, so two forks of a source that did not change still report different values, and the numbers are not a way to tell whether a source has changed. Absent only on forks taken before the version was recorded. | [optional] 

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


