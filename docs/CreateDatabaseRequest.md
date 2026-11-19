# CreateDatabaseRequest

Request body for POST /databases

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_catalog** | **str** | Name of the database&#39;s own catalog in SQL. Defaults to &#x60;default&#x60;. Lowercase letters, digits and &#x60;_&#x60;, not starting with a digit. Some names are reserved, such as &#x60;hotdata&#x60; and &#x60;information_schema&#x60;. | [optional] 
**default_schema** | **str** | Schema that unqualified table names resolve to. Defaults to the only schema in &#x60;schemas&#x60; if there is exactly one, otherwise &#x60;main&#x60;. | [optional] 
**expires_at** | **str** | When the database expires: a future RFC 3339 timestamp, or a duration such as &#x60;90m&#x60;, &#x60;24h&#x60; or &#x60;7d&#x60;. Omit for no expiry. | [optional] 
**if_not_exists** | **bool** | If a database with this &#x60;name&#x60; exists, return it with 200 instead of creating another. Requires &#x60;name&#x60;; the rest of the request is ignored on a match. | [optional] 
**name** | **str** | Display name. Need not be unique. Defaults to a name based on the database ID. | [optional] 
**schemas** | [**List[DatabaseDefaultSchemaDecl]**](DatabaseDefaultSchemaDecl.md) | Schemas and tables to create with the database. | [optional] 

## Example

```python
from hotdata.models.create_database_request import CreateDatabaseRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDatabaseRequest from a JSON string
create_database_request_instance = CreateDatabaseRequest.from_json(json)
# print the JSON string representation of the object
print(CreateDatabaseRequest.to_json())

# convert the object into a dict
create_database_request_dict = create_database_request_instance.to_dict()
# create an instance of CreateDatabaseRequest from a dict
create_database_request_from_dict = CreateDatabaseRequest.from_dict(create_database_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


