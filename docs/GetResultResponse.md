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
**total_row_count** | **int** | Grand total rows in the full result, ignoring &#x60;offset&#x60; and &#x60;limit&#x60;. Present whenever the result is &#x60;ready&#x60;, and carrying the same value as the &#x60;X-Total-Row-Count&#x60; response header.  Compare it against &#x60;row_count&#x60; to tell whether this body is the whole result: &#x60;row_count &lt; total_row_count&#x60; means the rest is still there, one page further on. Without it a windowed fetch cannot tell a full result from a truncated one from the body alone. | [optional] 

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


