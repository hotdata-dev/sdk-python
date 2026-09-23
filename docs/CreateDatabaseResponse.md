# CreateDatabaseResponse

Response body for POST /databases

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created** | **bool** | Whether this call brought the database into existence.  Only &#x60;false&#x60; when &#x60;if_not_exists&#x60; found a database already carrying the requested name, in which case nothing was created and the existing one is returned. The response status says the same thing — &#x60;201&#x60; against &#x60;200&#x60; — but generated clients often surface only the body, so it is stated here as well.  Always sent. It is declared optional so that a client built against a newer version of this API still accepts a response from a deployment that predates the field. Absent therefore means \&quot;this deployment cannot say\&quot;, which is not the same as &#x60;false&#x60; — test for the two values explicitly rather than for truthiness. | [optional] 
**default_catalog** | **str** | Name the database&#39;s default catalog answers to inside its query scope (&#x60;default&#x60; unless overridden at create time). | 
**default_connection_id** | **str** | Id of the connection that backs this database&#39;s &#x60;default&#x60; catalog. Two uses: pass it as &#x60;connection_id&#x60; to &#x60;POST /v1/databases/{other}/catalogs&#x60; to attach this database&#39;s catalog into another database, and as the connection in the managed-tables load endpoint (&#x60;POST /v1/connections/{id}/schemas/{s}/tables/{t}/loads&#x60;) to load tables declared at create time. Other connection endpoints (list, get, health, delete, cache purge) refuse to act on it. In SQL, address the catalog as &#x60;default&#x60; inside an &#x60;X-Database-Id&#x60; scope, not by this id. | 
**default_schema** | **str** | Schema that unqualified table names resolve to inside this database&#39;s query scope. &#x60;main&#x60; unless the database declares a single schema or a &#x60;default_schema&#x60; was set at create time. | 
**expires_at** | **datetime** | When this database expires. | [optional] 
**forked_from** | [**ForkedFromInfo**](ForkedFromInfo.md) | Set on a database created by forking another one: where it came from and which state of the source it copied. | [optional] 
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


