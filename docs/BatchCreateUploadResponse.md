# BatchCreateUploadResponse

Response body for `POST /v1/uploads/batch`: one created session per requested file, in request order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uploads** | [**List[UploadSessionResponse]**](UploadSessionResponse.md) |  | 

## Example

```python
from hotdata.models.batch_create_upload_response import BatchCreateUploadResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BatchCreateUploadResponse from a JSON string
batch_create_upload_response_instance = BatchCreateUploadResponse.from_json(json)
# print the JSON string representation of the object
print(BatchCreateUploadResponse.to_json())

# convert the object into a dict
batch_create_upload_response_dict = batch_create_upload_response_instance.to_dict()
# create an instance of BatchCreateUploadResponse from a dict
batch_create_upload_response_from_dict = BatchCreateUploadResponse.from_dict(batch_create_upload_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


