# ApiErrorDetail

Details of an API error.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Machine-readable error code, such as &#x60;BAD_REQUEST&#x60; or &#x60;NOT_FOUND&#x60;. | 
**message** | **str** | Human-readable description of the error. | 

## Example

```python
from hotdata.models.api_error_detail import ApiErrorDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ApiErrorDetail from a JSON string
api_error_detail_instance = ApiErrorDetail.from_json(json)
# print the JSON string representation of the object
print(ApiErrorDetail.to_json())

# convert the object into a dict
api_error_detail_dict = api_error_detail_instance.to_dict()
# create an instance of ApiErrorDetail from a dict
api_error_detail_from_dict = ApiErrorDetail.from_dict(api_error_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


