# ResultInfo

Summary of a persisted query result for listing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**error_message** | **str** |  | [optional] 
**id** | **str** |  | 
**status** | **str** |  | 

## Example

```python
from hotdata.models.result_info import ResultInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ResultInfo from a JSON string
result_info_instance = ResultInfo.from_json(json)
# print the JSON string representation of the object
print(ResultInfo.to_json())

# convert the object into a dict
result_info_dict = result_info_instance.to_dict()
# create an instance of ResultInfo from a dict
result_info_from_dict = ResultInfo.from_dict(result_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


