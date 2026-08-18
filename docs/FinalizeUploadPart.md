# FinalizeUploadPart

One part of a multi-part upload, supplied at finalize. Single-`PUT` uploads have no parts.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**e_tag** | **str** | The &#x60;ETag&#x60; response header returned by that part&#39;s &#x60;PUT&#x60;. | 
**part_number** | **int** | The 1-based part number you uploaded this part as. | 

## Example

```python
from hotdata.models.finalize_upload_part import FinalizeUploadPart

# TODO update the JSON string below
json = "{}"
# create an instance of FinalizeUploadPart from a JSON string
finalize_upload_part_instance = FinalizeUploadPart.from_json(json)
# print the JSON string representation of the object
print(FinalizeUploadPart.to_json())

# convert the object into a dict
finalize_upload_part_dict = finalize_upload_part_instance.to_dict()
# create an instance of FinalizeUploadPart from a dict
finalize_upload_part_from_dict = FinalizeUploadPart.from_dict(finalize_upload_part_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


