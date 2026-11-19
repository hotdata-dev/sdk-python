# CreateUploadRequest

A file you plan to upload. The response gives you short-lived URLs to `PUT` the bytes to. One upload can be at most 16 GiB by default; for more data, load several uploads with `mode: append`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**checksum_algo** | **str** | Checksum algorithm for &#x60;checksum_value&#x60;. Only &#x60;sha256&#x60; is accepted. | [optional] 
**checksum_value** | **str** | Checksum of the file. Stored with the upload but not verified. | [optional] 
**content_encoding** | **str** | Content encoding, such as &#x60;gzip&#x60;, kept with the upload. | [optional] 
**content_type** | **str** | MIME type of the file. A load uses it to detect the file format when &#x60;format&#x60; is not set. | [optional] 
**declared_size_bytes** | **int** | Exact file size in bytes, checked again when you finalize. Omit it to stream a file of unknown size and get part URLs from &#x60;POST /v1/uploads/{upload_id}/parts&#x60; as you go. | [optional] 
**filename** | **str** | File name, kept for your reference. It does not affect the upload or load. | [optional] 
**part_size** | **int** | Preferred part size in bytes for a multi-part upload. Hotdata adjusts it to the allowed range; the size it uses is returned as &#x60;part_size&#x60;. | [optional] 

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


