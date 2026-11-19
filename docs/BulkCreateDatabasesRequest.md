# BulkCreateDatabasesRequest

Creates many databases from one template. Each database gets the same schemas and tables.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | How many databases to create. | 
**default_catalog** | **str** | Name of each database&#39;s own catalog in SQL. Defaults to &#x60;default&#x60;. | [optional] 
**default_schema** | **str** | Schema that unqualified table names resolve to in each database. | [optional] 
**expires_at** | **str** | When the databases expire: a future RFC 3339 timestamp, or a duration such as &#x60;24h&#x60;, &#x60;90m&#x60; or &#x60;7d&#x60;. | [optional] 
**idempotency_key** | **str** | Key that makes the request safe to retry. A repeated key returns the original batch, even if the rest of the request differs. | [optional] 
**name_template** | **str** | Name pattern for the databases. Must contain &#x60;{index}&#x60;, which becomes each database&#39;s zero-padded position (&#x60;tenant-00&#x60; to &#x60;tenant-99&#x60; for a count of 100); a batch suffix is added to each name. | [optional] 
**schemas** | [**List[DatabaseDefaultSchemaDecl]**](DatabaseDefaultSchemaDecl.md) | Schemas and tables to create in every database. | [optional] 

## Example

```python
from hotdata.models.bulk_create_databases_request import BulkCreateDatabasesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BulkCreateDatabasesRequest from a JSON string
bulk_create_databases_request_instance = BulkCreateDatabasesRequest.from_json(json)
# print the JSON string representation of the object
print(BulkCreateDatabasesRequest.to_json())

# convert the object into a dict
bulk_create_databases_request_dict = bulk_create_databases_request_instance.to_dict()
# create an instance of BulkCreateDatabasesRequest from a dict
bulk_create_databases_request_from_dict = BulkCreateDatabasesRequest.from_dict(bulk_create_databases_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


