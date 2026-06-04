# ManagedTableResponse

Response body for a successful add-table request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_id** | **str** |  | 
**var_schema** | **str** |  | 
**table** | **str** |  | 

## Example

```python
from hotdata.models.managed_table_response import ManagedTableResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ManagedTableResponse from a JSON string
managed_table_response_instance = ManagedTableResponse.from_json(json)
# print the JSON string representation of the object
print(ManagedTableResponse.to_json())

# convert the object into a dict
managed_table_response_dict = managed_table_response_instance.to_dict()
# create an instance of ManagedTableResponse from a dict
managed_table_response_from_dict = ManagedTableResponse.from_dict(managed_table_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


