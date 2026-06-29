# MintUploadPartsRequest

Request body for `POST /v1/uploads/{upload_id}/parts`: mint presigned upload URLs for specific parts of a streaming (unknown-size) multi-part upload.  Provide the 1-based part numbers you want URLs for. Mint parts as you upload, and re-request a part number if its URL expires before you finish — the parts you have already uploaded are unaffected.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**part_numbers** | **List[int]** | The 1-based part numbers to mint URLs for. Must be non-empty; each number must be between 1 and the maximum number of parts allowed. | 

## Example

```python
from hotdata.models.mint_upload_parts_request import MintUploadPartsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of MintUploadPartsRequest from a JSON string
mint_upload_parts_request_instance = MintUploadPartsRequest.from_json(json)
# print the JSON string representation of the object
print(MintUploadPartsRequest.to_json())

# convert the object into a dict
mint_upload_parts_request_dict = mint_upload_parts_request_instance.to_dict()
# create an instance of MintUploadPartsRequest from a dict
mint_upload_parts_request_from_dict = MintUploadPartsRequest.from_dict(mint_upload_parts_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


