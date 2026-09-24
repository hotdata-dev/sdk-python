# UpdateManagedTableRequest

Request body for setting the columns a table declares constant per key: `PUT /v1/connections/{id}/schemas/{schema}/tables/{table}/constant-per-key` and `PUT /v1/databases/{id}/schemas/{schema}/tables/{table}/constant-per-key`.  The body carries the complete new value: send an empty array to remove the declaration. Sending any other field is rejected — `key`, `partition_by` and `sorted_by` are fixed when the table is created.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**constant_per_key** | **List[str]** | Columns whose value is the same for every row sharing this table&#39;s key.  Send &#x60;[]&#x60; to revoke the declaration, which restores the unrestricted search on the next load — this is the kill switch if a declaration turns out to be false.  **Correctness-affecting, not a hint.** If the assertion is false, a keyed mutation supersedes one version of a key and appends beside another, silently duplicating it. | [optional] 

## Example

```python
from hotdata.models.update_managed_table_request import UpdateManagedTableRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateManagedTableRequest from a JSON string
update_managed_table_request_instance = UpdateManagedTableRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateManagedTableRequest.to_json())

# convert the object into a dict
update_managed_table_request_dict = update_managed_table_request_instance.to_dict()
# create an instance of UpdateManagedTableRequest from a dict
update_managed_table_request_from_dict = UpdateManagedTableRequest.from_dict(update_managed_table_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


