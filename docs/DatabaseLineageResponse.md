# DatabaseLineageResponse

Response body for GET /databases/{database_id}/lineage.  Answers where a database came from and what came from it. Everything here is a historical record: forks are independent databases, and lineage does not make one depend on another.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ancestors** | [**List[LineageAncestorInfo]**](LineageAncestorInfo.md) | Fork ancestry, nearest parent first, ending at the database named by &#x60;root_id&#x60; unless &#x60;ancestors_truncated&#x60; says otherwise. A deleted generation does not cut the chain short — it is listed with &#x60;exists&#x60; false and the ancestry continues past it. Empty when this database is not a fork. | 
**ancestors_truncated** | **bool** | True when the ancestry is longer than one response carries, so &#x60;ancestors&#x60; stops before reaching &#x60;root_id&#x60;. | 
**database_id** | **str** | The database this lineage describes. | 
**fork_count** | **int** | How many databases were forked directly from this one in total — so you can tell whether &#x60;forks&#x60; is the whole set or only the newest of it. | 
**forks** | [**List[LineageForkInfo]**](LineageForkInfo.md) | The databases forked directly from this one, most recently forked first, including any that have since been deleted. A fork of a fork appears in its own parent&#39;s lineage, not here. | 
**root_id** | **str** | Top of the family tree: the database the whole chain of forks descends from. Equal to &#x60;database_id&#x60; when this database is not a fork. | 

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


