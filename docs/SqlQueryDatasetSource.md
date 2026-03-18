# SqlQueryDatasetSource

Create dataset from a SQL query (auto-creates a saved query)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Optional description for the auto-created saved query. | [optional] 
**name** | **str** | Optional name for the auto-created saved query. Defaults to the dataset label. | [optional] 
**sql** | **str** |  | 

## Example

```python
from hotdata.models.sql_query_dataset_source import SqlQueryDatasetSource

# TODO update the JSON string below
json = "{}"
# create an instance of SqlQueryDatasetSource from a JSON string
sql_query_dataset_source_instance = SqlQueryDatasetSource.from_json(json)
# print the JSON string representation of the object
print(SqlQueryDatasetSource.to_json())

# convert the object into a dict
sql_query_dataset_source_dict = sql_query_dataset_source_instance.to_dict()
# create an instance of SqlQueryDatasetSource from a dict
sql_query_dataset_source_from_dict = SqlQueryDatasetSource.from_dict(sql_query_dataset_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


