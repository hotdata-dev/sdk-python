# ManagedSchemaResponse

Response body for a successful add-schema request. Echoes the normalised (lowercased) names so callers see exactly what was persisted.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_id** | **str** | Connection backing the catalog the schema was added to. For a database default catalog this is the database&#39;s &#x60;default_connection_id&#x60;. | 
**var_schema** | **str** |  | 
**tables** | **List[str]** |  | 

## Example

```python
from hotdata.models.managed_schema_response import ManagedSchemaResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ManagedSchemaResponse from a JSON string
managed_schema_response_instance = ManagedSchemaResponse.from_json(json)
# print the JSON string representation of the object
print(ManagedSchemaResponse.to_json())

# convert the object into a dict
managed_schema_response_dict = managed_schema_response_instance.to_dict()
# create an instance of ManagedSchemaResponse from a dict
managed_schema_response_from_dict = ManagedSchemaResponse.from_dict(managed_schema_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


