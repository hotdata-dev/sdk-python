# BulkCreateDatabasesResult

Result of a bulk database creation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**batch_id** | **str** | ID of the batch. | 
**cancelled** | **bool** | Whether the batch was stopped before it finished. | 
**created** | **int** | Number of databases created. | 
**requested** | **int** | Number of databases requested. | 

## Example

```python
from hotdata.models.bulk_create_databases_result import BulkCreateDatabasesResult

# TODO update the JSON string below
json = "{}"
# create an instance of BulkCreateDatabasesResult from a JSON string
bulk_create_databases_result_instance = BulkCreateDatabasesResult.from_json(json)
# print the JSON string representation of the object
print(BulkCreateDatabasesResult.to_json())

# convert the object into a dict
bulk_create_databases_result_dict = bulk_create_databases_result_instance.to_dict()
# create an instance of BulkCreateDatabasesResult from a dict
bulk_create_databases_result_from_dict = BulkCreateDatabasesResult.from_dict(bulk_create_databases_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


