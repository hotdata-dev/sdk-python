# MintUploadPartsResponse

Response body for `POST /v1/uploads/{upload_id}/parts`: the minted part URLs, in ascending part-number order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parts** | [**List[MintedUploadPartResponse]**](MintedUploadPartResponse.md) | The minted part URLs, in ascending part-number order. &#x60;PUT&#x60; each part&#39;s bytes to its URL and keep the response&#39;s &#x60;ETag&#x60; to pass to finalize. | 

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


