# GetResultResponse

Response body for GET /results/{id} Returns status and optionally the result data

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **List[str]** |  | [optional] 
**error_message** | **str** |  | [optional] 
**nullable** | **List[bool]** |  | [optional] 
**result_id** | **str** |  | 
**row_count** | **int** |  | [optional] 
**rows** | **List[List[object]]** | Array of rows, where each row is an array of column values. | [optional] 
**status** | **str** |  | 

## Example

```python
from hotdata.models.get_result_response import GetResultResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetResultResponse from a JSON string
get_result_response_instance = GetResultResponse.from_json(json)
# print the JSON string representation of the object
print(GetResultResponse.to_json())

# convert the object into a dict
get_result_response_dict = get_result_response_instance.to_dict()
# create an instance of GetResultResponse from a dict
get_result_response_from_dict = GetResultResponse.from_dict(get_result_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


