# UploadInfo

Single upload info for listing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_type** | **object** |  | [optional] 
**created_at** | **datetime** |  | 
**id** | **str** |  | 
**size_bytes** | **int** |  | 
**status** | **str** |  | 

## Example

```python
from hotdata.models.upload_info import UploadInfo

# TODO update the JSON string below
json = "{}"
# create an instance of UploadInfo from a JSON string
upload_info_instance = UploadInfo.from_json(json)
# print the JSON string representation of the object
print(UploadInfo.to_json())

# convert the object into a dict
upload_info_dict = upload_info_instance.to_dict()
# create an instance of UploadInfo from a dict
upload_info_from_dict = UploadInfo.from_dict(upload_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


