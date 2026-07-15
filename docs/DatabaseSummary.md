# DatabaseSummary

Summary item in GET /databases

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | When the database was created. | [optional] 
**default_catalog** | **str** | Name the database&#39;s default catalog answers to inside its query scope. | 
**default_schema** | **str** | Schema that unqualified table names resolve to inside this database&#39;s query scope. &#x60;main&#x60; unless the database declares a single schema or a &#x60;default_schema&#x60; was set at create time. | 
**expires_at** | **datetime** |  | [optional] 
**id** | **str** |  | 
**name** | **str** |  | [optional] 

## Example

```python
from hotdata.models.database_summary import DatabaseSummary

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseSummary from a JSON string
database_summary_instance = DatabaseSummary.from_json(json)
# print the JSON string representation of the object
print(DatabaseSummary.to_json())

# convert the object into a dict
database_summary_dict = database_summary_instance.to_dict()
# create an instance of DatabaseSummary from a dict
database_summary_from_dict = DatabaseSummary.from_dict(database_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


