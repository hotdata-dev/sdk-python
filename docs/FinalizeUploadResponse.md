# FinalizeUploadResponse

A finalized upload, ready to load into a table.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_type** | **str** |  | [optional] 
**created_at** | **datetime** |  | 
**size_bytes** | **int** | Size of the uploaded file in bytes. | 
**status** | **str** |  | 
**upload_id** | **str** |  | 

## Example

```python
from hotdata.models.finalize_upload_response import FinalizeUploadResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FinalizeUploadResponse from a JSON string
finalize_upload_response_instance = FinalizeUploadResponse.from_json(json)
# print the JSON string representation of the object
print(FinalizeUploadResponse.to_json())

# convert the object into a dict
finalize_upload_response_dict = finalize_upload_response_instance.to_dict()
# create an instance of FinalizeUploadResponse from a dict
finalize_upload_response_from_dict = FinalizeUploadResponse.from_dict(finalize_upload_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


