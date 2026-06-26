# UploadSessionResponse

A created upload session: everything needed to upload the bytes directly to storage and later finalize the upload.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**finalize_token** | **str** | One-time token that authorizes finalizing this upload. Returned exactly once at create time — store it; it cannot be retrieved again. | 
**headers** | **Dict[str, str]** | Headers you must send verbatim with each &#x60;PUT&#x60;. Currently always empty; present so a future mode can require signed headers without changing the response shape. | 
**mode** | **str** | Upload mode: &#x60;single&#x60; (upload the whole file with one &#x60;PUT&#x60; to &#x60;url&#x60;) or &#x60;multipart&#x60; (upload each part with one &#x60;PUT&#x60; to the matching entry in &#x60;part_urls&#x60;). Modeled as a string so additional modes can be added later without breaking clients. | 
**part_size** | **int** | For a &#x60;multipart&#x60; upload, the size in bytes to split the file into: send bytes &#x60;[(i-1) * part_size, i * part_size)&#x60; to &#x60;part_urls[i - 1]&#x60;, with the last part carrying the remainder. Slice by this value — do **not** divide the file evenly by &#x60;part_urls.len()&#x60;, which can make a non-final part smaller than the 5 MiB minimum that storage requires (the upload then fails at finalize). Absent for &#x60;single&#x60; uploads. | [optional] 
**part_urls** | **List[str]** | For a &#x60;multipart&#x60; upload, the per-part URLs in ascending part order: &#x60;PUT&#x60; your file&#39;s part *i* (1-based) to &#x60;part_urls[i - 1]&#x60; and keep each response&#39;s &#x60;ETag&#x60;, then pass the &#x60;{part_number, e_tag}&#x60; list to finalize. Absent for &#x60;single&#x60; uploads. | [optional] 
**upload_id** | **str** | Identifier for this upload. Pass it to the finalize endpoint and to the managed-table load endpoint once finalized. | 
**url** | **str** | The URL to &#x60;PUT&#x60; the raw file bytes to, for a &#x60;single&#x60; upload. Short-lived — upload promptly and finalize. Absent for &#x60;multipart&#x60; uploads (use &#x60;part_urls&#x60;). | [optional] 

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


