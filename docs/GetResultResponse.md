# GetResultResponse

A saved query result: its status and, once `ready`, its data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **List[str]** | Column names, in order. Present when &#x60;status&#x60; is &#x60;ready&#x60;. | [optional] 
**error_message** | **str** | Why the result failed. Present only when &#x60;status&#x60; is &#x60;failed&#x60;. | [optional] 
**nullable** | **List[bool]** | Whether each column, in the same order as &#x60;columns&#x60;, can hold nulls. | [optional] 
**result_id** | **str** |  | 
**row_count** | **int** | Number of rows in this response. | [optional] 
**rows** | **List[List[object]]** | Result rows. Each row is an array of values in column order. | [optional] 
**status** | **str** | &#x60;pending&#x60;, &#x60;processing&#x60;, &#x60;ready&#x60; or &#x60;failed&#x60;. | 
**total_row_count** | **int** | Number of rows in the full result, ignoring &#x60;offset&#x60; and &#x60;limit&#x60;. If &#x60;row_count&#x60; is smaller, more rows are available on later pages. | [optional] 

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


