# DatabaseLineageResponse

Where a database was forked from, and which databases were forked from it.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ancestors** | [**List[LineageAncestorInfo]**](LineageAncestorInfo.md) | Databases this one descends from, nearest parent first. Deleted ones stay in the list with &#x60;exists: false&#x60;. Empty when this is not a fork. | 
**ancestors_truncated** | **bool** | True when &#x60;ancestors&#x60; stops before reaching &#x60;root_id&#x60;. | 
**database_id** | **str** | The database this lineage describes. | 
**fork_count** | **int** | Total number of databases forked directly from this one. | 
**forks** | [**List[LineageForkInfo]**](LineageForkInfo.md) | Databases forked directly from this one, newest first, including deleted ones. Limited by &#x60;forks_limit&#x60;. | 
**root_id** | **str** | The original database at the top of the fork chain. Equal to &#x60;database_id&#x60; when this database is not a fork. | 

## Example

```python
from hotdata.models.database_lineage_response import DatabaseLineageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseLineageResponse from a JSON string
database_lineage_response_instance = DatabaseLineageResponse.from_json(json)
# print the JSON string representation of the object
print(DatabaseLineageResponse.to_json())

# convert the object into a dict
database_lineage_response_dict = database_lineage_response_instance.to_dict()
# create an instance of DatabaseLineageResponse from a dict
database_lineage_response_from_dict = DatabaseLineageResponse.from_dict(database_lineage_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


