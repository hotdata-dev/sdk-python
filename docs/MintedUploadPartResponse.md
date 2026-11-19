# MintedUploadPartResponse

An upload URL for one part.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**part_number** | **int** | Part number, starting at 1. | 
**url** | **str** | URL to &#x60;PUT&#x60; the part to. Expires soon. Keep the response&#39;s &#x60;ETag&#x60; for finalize. | 

## Example

```python
from hotdata.models.minted_upload_part_response import MintedUploadPartResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MintedUploadPartResponse from a JSON string
minted_upload_part_response_instance = MintedUploadPartResponse.from_json(json)
# print the JSON string representation of the object
print(MintedUploadPartResponse.to_json())

# convert the object into a dict
minted_upload_part_response_dict = minted_upload_part_response_instance.to_dict()
# create an instance of MintedUploadPartResponse from a dict
minted_upload_part_response_from_dict = MintedUploadPartResponse.from_dict(minted_upload_part_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


