# TableRefreshResult

Result payload for a `data_refresh_table` job.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_id** | **str** |  | 
**duration_ms** | **int** |  | 
**rows_synced** | **int** |  | 
**schema_name** | **str** |  | 
**table_name** | **str** |  | 
**warnings** | [**List[RefreshWarning]**](RefreshWarning.md) |  | [optional] 

## Example

```python
from hotdata.models.table_refresh_result import TableRefreshResult

# TODO update the JSON string below
json = "{}"
# create an instance of TableRefreshResult from a JSON string
table_refresh_result_instance = TableRefreshResult.from_json(json)
# print the JSON string representation of the object
print(TableRefreshResult.to_json())

# convert the object into a dict
table_refresh_result_dict = table_refresh_result_instance.to_dict()
# create an instance of TableRefreshResult from a dict
table_refresh_result_from_dict = TableRefreshResult.from_dict(table_refresh_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


