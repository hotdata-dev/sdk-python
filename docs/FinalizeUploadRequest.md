# FinalizeUploadRequest

Request body for `POST /v1/uploads/{upload_id}/finalize`.  Finalizing confirms the bytes were uploaded and makes the upload usable as managed-table contents. The request body is optional for single-`PUT` uploads; send `parts` only for a future multi-part upload.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parts** | [**List[FinalizeUploadPart]**](FinalizeUploadPart.md) | Parts to assemble, for a multi-part upload. Omit for single-&#x60;PUT&#x60; uploads (the common case). | [optional] 

## Example

```python
from hotdata.models.finalize_upload_request import FinalizeUploadRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FinalizeUploadRequest from a JSON string
finalize_upload_request_instance = FinalizeUploadRequest.from_json(json)
# print the JSON string representation of the object
print(FinalizeUploadRequest.to_json())

# convert the object into a dict
finalize_upload_request_dict = finalize_upload_request_instance.to_dict()
# create an instance of FinalizeUploadRequest from a dict
finalize_upload_request_from_dict = FinalizeUploadRequest.from_dict(finalize_upload_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


