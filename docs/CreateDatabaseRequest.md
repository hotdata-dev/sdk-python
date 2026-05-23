# CreateDatabaseRequest

Request body for POST /databases

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Optional free-form display label (for UIs/CLIs). Not unique. Not an identifier — databases are always addressed by &#x60;id&#x60;. | [optional] 
**expires_at** | **str** | When this database expires. Accepts either an RFC 3339 timestamp (e.g. &#x60;\&quot;2026-06-01T00:00:00Z\&quot;&#x60;) or a relative duration suffixed with &#x60;h&#x60; (hours), &#x60;m&#x60; (minutes), or &#x60;d&#x60; (days) — for example &#x60;\&quot;24h\&quot;&#x60;, &#x60;\&quot;48h\&quot;&#x60;, or &#x60;\&quot;7d\&quot;&#x60;. Defaults to &#x60;\&quot;24h\&quot;&#x60; when omitted. Expiry is best-effort: the database will not be deleted before &#x60;expires_at&#x60;, but cleanup may run later than the exact timestamp. | [optional] 
**schemas** | [**List[DatabaseDefaultSchemaDecl]**](DatabaseDefaultSchemaDecl.md) | Optional schemas/tables to declare on the database&#39;s auto-created &#x60;default&#x60; catalog. Mirrors the &#x60;config.schemas&#x60; field of a managed &#x60;POST /v1/connections&#x60;. Tables declared here can be loaded via the standard managed-table load endpoint targeting &#x60;default_connection_id&#x60;. Omitted or empty means the default catalog starts empty. | [optional] 

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


