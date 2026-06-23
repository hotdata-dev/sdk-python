# LoadManagedTableRequest

Request body for `POST /v1/connections/{connection_id}/schemas/{schema}/tables/{table}/loads`.  Publishes a previously-uploaded file as the new contents of the named managed table. CSV and JSON uploads are converted to columnar storage on load; Parquet uploads are published directly. `mode` is fixed to `\"replace\"` today; the field is kept in the request body so future modes (e.g. append) are an additive change.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**format** | **str** | File format of the upload: &#x60;\&quot;csv\&quot;&#x60;, &#x60;\&quot;json\&quot;&#x60;, or &#x60;\&quot;parquet\&quot;&#x60;. Optional — when omitted, the format is auto-detected from the upload&#39;s &#x60;Content-Type&#x60; and, failing that, from the file contents. Provide it explicitly to override detection or when the contents are ambiguous. &#x60;\&quot;json\&quot;&#x60; expects newline-delimited JSON (one object per line), not a JSON array. | [optional] 
**mode** | **str** | Load mode. Only &#x60;\&quot;replace\&quot;&#x60; is supported in this release. | 
**upload_id** | **str** | ID of a previously-staged upload (see &#x60;POST /v1/files&#x60;). The upload is claimed atomically; concurrent loads against the same &#x60;upload_id&#x60; return 409. | 

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


