# ApiErrorDetail

Error detail within an API error response

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** |  | 
**message** | **str** |  | 

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


