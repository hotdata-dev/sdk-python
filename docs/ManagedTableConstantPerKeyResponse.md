# ManagedTableConstantPerKeyResponse

The declaration as it now stands after a `constant-per-key` write.  Echoed back rather than returning `204` so a caller can confirm what actually took effect instead of assuming its request applied — the same reason `/v1/information_schema` reports the field.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_id** | **str** |  | 
**constant_per_key** | **List[str]** | The columns now declared constant per key. Empty means no declaration, i.e. the unrestricted search. | 
**var_schema** | **str** |  | 
**table** | **str** |  | 

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


