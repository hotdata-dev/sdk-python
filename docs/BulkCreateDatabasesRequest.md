# BulkCreateDatabasesRequest

Request body for POST /databases/bulk.  One template plus a count, so the body stays small whatever `count` is. Any schemas and tables declared here are applied to every database in the batch; load data into them afterwards exactly as you would for a database created one at a time.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | How many databases to create. | 
**default_catalog** | **str** | Name the default catalog answers to inside each database, as on a single create. Defaults to &#x60;default&#x60;. | [optional] 
**default_schema** | **str** | Schema that unqualified table names resolve to inside each database. | [optional] 
**expires_at** | **str** | When the created databases expire. Accepts an RFC 3339 timestamp or a relative duration such as &#x60;24h&#x60;, &#x60;90m&#x60;, or &#x60;7d&#x60;. | [optional] 
**idempotency_key** | **str** | Repeat this value to retry a request safely. A retry carrying a key that was already used returns the original batch — the same &#x60;batch_id&#x60; and the same databases — instead of creating a second set.  The key identifies the request, not its contents: reusing a key with a different &#x60;count&#x60; or template returns the original batch unchanged rather than reporting a mismatch. Use a fresh key per distinct request. | [optional] 
**name_template** | **str** | Optional display-label pattern for each database. &#x60;{index}&#x60; is replaced with the database&#39;s zero-based position — for example &#x60;tenant-{index}&#x60; produces &#x60;tenant-0&#x60;, &#x60;tenant-1&#x60;, and so on. Labels are not identifiers and are not required to be unique. | [optional] 
**schemas** | [**List[DatabaseDefaultSchemaDecl]**](DatabaseDefaultSchemaDecl.md) | Schemas and tables to declare on every database in the batch, in the same shape a single create accepts. The declaration applies identically to each database, so a batch of 10,000 declaring one table yields 10,000 databases that each hold that table and are ready to load — with no follow-up call per database. Omitted or empty means each database starts with no tables. | [optional] 

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


