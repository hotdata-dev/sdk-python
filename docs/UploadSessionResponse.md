# UploadSessionResponse

A new upload, with everything needed to upload and finalize the file.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**finalize_token** | **str** | Token to send in the &#x60;X-Upload-Finalize-Token&#x60; header when you request part URLs or finalize. Returned only once. | 
**headers** | **Dict[str, str]** | Headers to send with each &#x60;PUT&#x60;. Currently always empty. | 
**mode** | **str** | &#x60;single&#x60;: &#x60;PUT&#x60; the whole file to &#x60;url&#x60;. &#x60;multipart&#x60;: &#x60;PUT&#x60; each part to its own URL. | 
**part_size** | **int** | For a &#x60;multipart&#x60; upload, the size of every part except the last, in bytes. Split the file by this size, not evenly by part count, or a part may fall under the 5 MiB minimum and finalize fails. | [optional] 
**part_urls** | **List[str]** | For a &#x60;multipart&#x60; upload of known size, one URL per part, in order: &#x60;PUT&#x60; part *i* to &#x60;part_urls[i - 1]&#x60; and keep each response&#39;s &#x60;ETag&#x60; for finalize. Absent for a streaming upload. | [optional] 
**upload_id** | **str** | ID of the upload. Use it to finalize the upload and then to load it. | 
**url** | **str** | URL to &#x60;PUT&#x60; the file to, for a &#x60;single&#x60; upload. Expires soon. | [optional] 

## Example

```python
from hotdata.models.upload_session_response import UploadSessionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UploadSessionResponse from a JSON string
upload_session_response_instance = UploadSessionResponse.from_json(json)
# print the JSON string representation of the object
print(UploadSessionResponse.to_json())

# convert the object into a dict
upload_session_response_dict = upload_session_response_instance.to_dict()
# create an instance of UploadSessionResponse from a dict
upload_session_response_from_dict = UploadSessionResponse.from_dict(upload_session_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


