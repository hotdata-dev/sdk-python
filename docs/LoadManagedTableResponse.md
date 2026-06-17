# LoadManagedTableResponse

Response body for `POST /v1/connections/{connection_id}/schemas/{schema}/tables/{table}/loads`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**arrow_schema_json** | **str** | Schema of the loaded table, as JSON. | 
**connection_id** | **str** |  | 
**row_count** | **int** | Total rows in the published parquet file. | 
**schema_name** | **str** |  | 
**table_name** | **str** |  | 

## Example

```python
from hotdata.models.load_managed_table_response import LoadManagedTableResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LoadManagedTableResponse from a JSON string
load_managed_table_response_instance = LoadManagedTableResponse.from_json(json)
# print the JSON string representation of the object
print(LoadManagedTableResponse.to_json())

# convert the object into a dict
load_managed_table_response_dict = load_managed_table_response_instance.to_dict()
# create an instance of LoadManagedTableResponse from a dict
load_managed_table_response_from_dict = LoadManagedTableResponse.from_dict(load_managed_table_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


