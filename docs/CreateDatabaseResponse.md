# CreateDatabaseResponse

Response body for POST /databases

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created** | **bool** | &#x60;true&#x60; if this call created the database; &#x60;false&#x60; if &#x60;if_not_exists&#x60; returned an existing one. | [optional] 
**default_catalog** | **str** | Name of the database&#39;s own catalog in SQL. | 
**default_connection_id** | **str** | ID of the connection behind the database&#39;s own catalog. Use it to load tables through the connection endpoints, or to attach this catalog to another database. | 
**default_schema** | **str** | Schema that unqualified table names resolve to. | 
**expires_at** | **datetime** | When the database expires. | [optional] 
**forked_from** | [**ForkedFromInfo**](ForkedFromInfo.md) | Present on a fork: the database it was copied from. | [optional] 
**id** | **str** |  | 
**name** | **str** |  | [optional] 

## Example

```python
from hotdata.models.create_database_response import CreateDatabaseResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDatabaseResponse from a JSON string
create_database_response_instance = CreateDatabaseResponse.from_json(json)
# print the JSON string representation of the object
print(CreateDatabaseResponse.to_json())

# convert the object into a dict
create_database_response_dict = create_database_response_instance.to_dict()
# create an instance of CreateDatabaseResponse from a dict
create_database_response_from_dict = CreateDatabaseResponse.from_dict(create_database_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


