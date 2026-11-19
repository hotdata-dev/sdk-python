# ManagedTableConstantPerKeyResponse

A table's `constant_per_key` setting after an update.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_id** | **str** | ID of the connection that holds the table. For a database, this is its &#x60;default_connection_id&#x60;. | 
**constant_per_key** | **List[str]** | Columns now set as constant per key. Empty means none. | 
**var_schema** | **str** | Schema name, in lowercase. | 
**table** | **str** | Table name, in lowercase. | 

## Example

```python
from hotdata.models.managed_table_constant_per_key_response import ManagedTableConstantPerKeyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ManagedTableConstantPerKeyResponse from a JSON string
managed_table_constant_per_key_response_instance = ManagedTableConstantPerKeyResponse.from_json(json)
# print the JSON string representation of the object
print(ManagedTableConstantPerKeyResponse.to_json())

# convert the object into a dict
managed_table_constant_per_key_response_dict = managed_table_constant_per_key_response_instance.to_dict()
# create an instance of ManagedTableConstantPerKeyResponse from a dict
managed_table_constant_per_key_response_from_dict = ManagedTableConstantPerKeyResponse.from_dict(managed_table_constant_per_key_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


