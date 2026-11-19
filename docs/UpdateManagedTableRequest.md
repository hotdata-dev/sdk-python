# UpdateManagedTableRequest

New value for a table's `constant_per_key` setting. Other fields are rejected, because a table's `key`, `partition_by` and `sorted_by` cannot be changed.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**constant_per_key** | **List[str]** | Columns that always hold the same value for rows with the same &#x60;key&#x60;. Replaces the current list; send &#x60;[]&#x60; to clear it. If it is not true, keyed loads silently duplicate rows. | [optional] 

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


