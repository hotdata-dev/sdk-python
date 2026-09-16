# CreateUploadRequest

Request body for `POST /v1/uploads` and for each entry of `POST /v1/uploads/batch`.  Describes a single file you intend to upload. The response carries a short-lived URL to `PUT` the bytes to, so the file never passes through the API itself. The declared size is validated against the bytes you actually upload when you finalize.  One upload may be at most 16 GiB by default, whatever its format. To load more data than that into a single table, split it across several uploads and load each one with `mode: append`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**checksum_algo** | **str** | Integrity checksum algorithm you are volunteering for this file. Currently only &#x60;sha256&#x60; is accepted. Optional; pair with &#x60;checksum_value&#x60;. | [optional] 
**checksum_value** | **str** | Integrity checksum value, paired with &#x60;checksum_algo&#x60;. Optional. | [optional] 
**content_encoding** | **str** | Content encoding to record for the uploaded file (for example &#x60;gzip&#x60;). Optional. | [optional] 
**content_type** | **str** | Content type to record for the uploaded file (for example the Parquet, CSV, or JSON MIME type). Optional. | [optional] 
**declared_size_bytes** | **int** | The exact size, in bytes, of the file you will upload. Optional. When provided, it is checked at create time against the maximum upload size (16 GiB by default, the same for every file format), so an oversized file is refused before you transfer any of it; it is checked again at finalize against the bytes actually uploaded — a mismatch fails the finalize. Omit it to create a streaming (unknown-size) upload: the session is always multi-part and returns no part URLs up front; instead you mint part URLs on demand from &#x60;POST /v1/uploads/{upload_id}/parts&#x60; as you upload, and finalize checks only that the file is non-empty and within the maximum upload size. | [optional] 
**filename** | **str** | Original file name, recorded with the upload for your own bookkeeping. Optional and advisory — it does not affect how the file is uploaded or loaded. | [optional] 
**part_size** | **int** | Preferred size, in bytes, of each part for a large (multi-part) upload. Optional hint — the service clamps it to the allowed part-size range and to the maximum number of parts, and ignores it for small files uploaded with a single &#x60;PUT&#x60;. Omit to let the service choose. | [optional] 

## Example

```python
from hotdata.models.create_upload_request import CreateUploadRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateUploadRequest from a JSON string
create_upload_request_instance = CreateUploadRequest.from_json(json)
# print the JSON string representation of the object
print(CreateUploadRequest.to_json())

# convert the object into a dict
create_upload_request_dict = create_upload_request_instance.to_dict()
# create an instance of CreateUploadRequest from a dict
create_upload_request_from_dict = CreateUploadRequest.from_dict(create_upload_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


