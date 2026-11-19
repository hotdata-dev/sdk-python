# BatchCreateUploadRequest

Several files to upload in one call.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uploads** | [**List[CreateUploadRequest]**](CreateUploadRequest.md) |  | 

## Example

```python
from hotdata.models.batch_create_upload_request import BatchCreateUploadRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BatchCreateUploadRequest from a JSON string
batch_create_upload_request_instance = BatchCreateUploadRequest.from_json(json)
# print the JSON string representation of the object
print(BatchCreateUploadRequest.to_json())

# convert the object into a dict
batch_create_upload_request_dict = batch_create_upload_request_instance.to_dict()
# create an instance of BatchCreateUploadRequest from a dict
batch_create_upload_request_from_dict = BatchCreateUploadRequest.from_dict(batch_create_upload_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


