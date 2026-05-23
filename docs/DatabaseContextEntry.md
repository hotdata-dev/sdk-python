# DatabaseContextEntry

One context entry returned by the API.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** |  | 
**name** | **str** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from hotdata.models.database_context_entry import DatabaseContextEntry

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseContextEntry from a JSON string
database_context_entry_instance = DatabaseContextEntry.from_json(json)
# print the JSON string representation of the object
print(DatabaseContextEntry.to_json())

# convert the object into a dict
database_context_entry_dict = database_context_entry_instance.to_dict()
# create an instance of DatabaseContextEntry from a dict
database_context_entry_from_dict = DatabaseContextEntry.from_dict(database_context_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


