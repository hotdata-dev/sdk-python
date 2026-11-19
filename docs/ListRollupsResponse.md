# ListRollupsResponse

The rollups of one database.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rollups** | [**List[Rollup]**](Rollup.md) |  | 

## Example

```python
from hotdata.models.list_rollups_response import ListRollupsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListRollupsResponse from a JSON string
list_rollups_response_instance = ListRollupsResponse.from_json(json)
# print the JSON string representation of the object
print(ListRollupsResponse.to_json())

# convert the object into a dict
list_rollups_response_dict = list_rollups_response_instance.to_dict()
# create an instance of ListRollupsResponse from a dict
list_rollups_response_from_dict = ListRollupsResponse.from_dict(list_rollups_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


