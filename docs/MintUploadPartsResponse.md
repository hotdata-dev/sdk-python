# MintUploadPartsResponse

Upload URLs for the requested parts.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parts** | [**List[MintedUploadPartResponse]**](MintedUploadPartResponse.md) | One URL per requested part, by part number. | 

## Example

```python
from hotdata.models.mint_upload_parts_response import MintUploadPartsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MintUploadPartsResponse from a JSON string
mint_upload_parts_response_instance = MintUploadPartsResponse.from_json(json)
# print the JSON string representation of the object
print(MintUploadPartsResponse.to_json())

# convert the object into a dict
mint_upload_parts_response_dict = mint_upload_parts_response_instance.to_dict()
# create an instance of MintUploadPartsResponse from a dict
mint_upload_parts_response_from_dict = MintUploadPartsResponse.from_dict(mint_upload_parts_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


