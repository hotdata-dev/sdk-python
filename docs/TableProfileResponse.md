# TableProfileResponse

Column-level statistics for a synced table. Profiles are computed at sync time and include per-column cardinality, null counts, and type-specific details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[ColumnProfileInfo]**](ColumnProfileInfo.md) | Per-column profile statistics | 
**connection** | **str** | Connection name | 
**row_count** | **int** | Total number of rows in the table | 
**var_schema** | **str** | Schema name | 
**synced_at** | **object** | When the table was last synced | [optional] 
**table** | **str** | Table name | 

## Example

```python
from hotdata.models.table_profile_response import TableProfileResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TableProfileResponse from a JSON string
table_profile_response_instance = TableProfileResponse.from_json(json)
# print the JSON string representation of the object
print(TableProfileResponse.to_json())

# convert the object into a dict
table_profile_response_dict = table_profile_response_instance.to_dict()
# create an instance of TableProfileResponse from a dict
table_profile_response_from_dict = TableProfileResponse.from_dict(table_profile_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


