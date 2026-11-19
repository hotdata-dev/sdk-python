# FinalizeUploadRequest

Completes an upload so it can be loaded into a table. A `single` upload needs no body.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parts** | [**List[FinalizeUploadPart]**](FinalizeUploadPart.md) | Every uploaded part, for a &#x60;multipart&#x60; upload. | [optional] 

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


