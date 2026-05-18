# LoadManagedTableRequest

Request body for `POST /v1/connections/{connection_id}/schemas/{schema}/tables/{table}/loads`.  Publishes a previously-uploaded parquet file as the new generation for the named managed table. `mode` is fixed to `\"replace\"` today; the field is kept in the request body so future modes (e.g. append) are an additive change.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mode** | **str** | Load mode. Only &#x60;\&quot;replace\&quot;&#x60; is supported in this release. | 
**upload_id** | **str** | ID of a previously-staged upload (see &#x60;POST /v1/files&#x60;). The upload must reference a parquet file. The upload is claimed atomically; concurrent loads against the same &#x60;upload_id&#x60; return 409. | 

## Example

```python
from hotdata.models.load_managed_table_request import LoadManagedTableRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LoadManagedTableRequest from a JSON string
load_managed_table_request_instance = LoadManagedTableRequest.from_json(json)
# print the JSON string representation of the object
print(LoadManagedTableRequest.to_json())

# convert the object into a dict
load_managed_table_request_dict = load_managed_table_request_instance.to_dict()
# create an instance of LoadManagedTableRequest from a dict
load_managed_table_request_from_dict = LoadManagedTableRequest.from_dict(load_managed_table_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


