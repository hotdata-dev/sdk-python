# CreateDatabaseRequest

Request body for POST /databases

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_catalog** | **str** | Optional name the database&#39;s auto-created default catalog answers to inside its query scope. Must be a valid SQL identifier (&#x60;[a-z0-9_]&#x60;, not starting with a digit) and may not collide with the reserved catalog names &#x60;hotdata&#x60; or &#x60;information_schema&#x60;. Defaults to &#x60;default&#x60; when omitted, so &#x60;default.main.&lt;table&gt;&#x60; keeps working. | [optional] 
**default_schema** | **str** | Optional schema that unqualified table names resolve to inside this database&#39;s query scope. Must be a valid SQL identifier (&#x60;[a-z0-9_]&#x60;, not starting with a digit). When omitted, a database that declares exactly one schema adopts that schema as its default; otherwise unqualified names resolve to &#x60;main&#x60;. Fully-qualified names (&#x60;&lt;catalog&gt;.&lt;schema&gt;.&lt;table&gt;&#x60;) are unaffected, and a per-query &#x60;default_schema&#x60; still takes precedence. | [optional] 
**expires_at** | **str** | When this database expires. Accepts either an RFC 3339 timestamp (e.g. &#x60;\&quot;2026-06-01T00:00:00Z\&quot;&#x60;) or a relative duration suffixed with &#x60;h&#x60; (hours), &#x60;m&#x60; (minutes), or &#x60;d&#x60; (days) — for example &#x60;\&quot;24h\&quot;&#x60;, &#x60;\&quot;48h\&quot;&#x60;, or &#x60;\&quot;7d\&quot;&#x60;. Omitted (or empty) means the database never expires. Expiry is best-effort: the database will not be deleted before &#x60;expires_at&#x60;, but cleanup may run later than the exact timestamp. | [optional] 
**name** | **str** | Optional free-form display label (for UIs/CLIs). Not unique. Not an identifier — databases are always addressed by &#x60;id&#x60;.  Accepts the legacy &#x60;description&#x60; key as an alias so clients that predate the rename keep populating this field. | [optional] 
**schemas** | [**List[DatabaseDefaultSchemaDecl]**](DatabaseDefaultSchemaDecl.md) | Optional schemas/tables to declare on the database&#39;s auto-created default catalog. Tables declared here can be loaded via the standard managed-table load endpoint targeting &#x60;default_connection_id&#x60;. Omitted or empty means the default catalog starts empty. | [optional] 

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


