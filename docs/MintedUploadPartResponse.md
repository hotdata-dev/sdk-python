# MintedUploadPartResponse

One minted part URL.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**part_number** | **int** | The 1-based part number this URL is for. | 
**url** | **str** | Short-lived URL to &#x60;PUT&#x60; this part&#39;s bytes to. Keep the response&#39;s &#x60;ETag&#x60; and pass the &#x60;{part_number, e_tag}&#x60; pair to finalize. | 

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


