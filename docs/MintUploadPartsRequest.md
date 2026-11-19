# MintUploadPartsRequest

Part numbers to get upload URLs for. Use this for a streaming upload, or to replace a part URL that expired.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**part_numbers** | **List[int]** | Part numbers, from 1 to 10000, at most 100 per request. | 

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


