# AddManagedTableRequest

Request body for adding a table to an existing schema: `POST /v1/connections/{id}/schemas/{schema}/tables` and `POST /v1/databases/{id}/schemas/{schema}/tables`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **List[str]** | Columns that uniquely identify a row, enabling the key-based load modes (&#x60;delete&#x60;, &#x60;update&#x60;, &#x60;upsert&#x60;) on this table: those loads match rows by these columns&#39; values. Omit (the default) to declare no key; the table can still be loaded with &#x60;replace&#x60; and &#x60;append&#x60;, but key-based modes are then rejected. | [optional] 
**key_determines** | **List[str]** | Columns whose value is determined by this table&#39;s &#x60;key&#x60;: for every uploaded row, every stored row sharing its key holds the same value of these columns.  Declaring this lets a keyed mutation (&#x60;delete&#x60;, &#x60;update&#x60;, &#x60;upsert&#x60;) restrict its search for prior versions to the values the upload carries, which prunes far harder than the key alone when the key&#39;s own file statistics are weak. Omit (the default) for the unrestricted search.  **Correctness-affecting, not a hint.** If the assertion is false, a mutation supersedes one version of a key and appends beside another, silently duplicating it. Declare it only where the invariant is established. | [optional] 
**name** | **str** |  | 
**partition_by** | [**List[TablePartitionKey]**](TablePartitionKey.md) | Partition keys for this table, applied in order. Omit for no partitioning. Declared when the table is created and fixed thereafter. | [optional] 
**sorted_by** | [**List[TableSortKey]**](TableSortKey.md) | Sort keys for this table, applied in order. Omit for no sort order. Declared when the table is created and fixed thereafter. | [optional] 

## Example

```python
from hotdata.models.add_managed_table_request import AddManagedTableRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddManagedTableRequest from a JSON string
add_managed_table_request_instance = AddManagedTableRequest.from_json(json)
# print the JSON string representation of the object
print(AddManagedTableRequest.to_json())

# convert the object into a dict
add_managed_table_request_dict = add_managed_table_request_instance.to_dict()
# create an instance of AddManagedTableRequest from a dict
add_managed_table_request_from_dict = AddManagedTableRequest.from_dict(add_managed_table_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


