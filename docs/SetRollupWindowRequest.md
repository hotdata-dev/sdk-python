# SetRollupWindowRequest

Sets how long rows of a rollup's table can still be changed.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**window_secs** | **int** | How long, in seconds, after a row&#39;s time it can still be changed or deleted. Applies to every rollup on the table. | 

## Example

```python
from hotdata.models.set_rollup_window_request import SetRollupWindowRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SetRollupWindowRequest from a JSON string
set_rollup_window_request_instance = SetRollupWindowRequest.from_json(json)
# print the JSON string representation of the object
print(SetRollupWindowRequest.to_json())

# convert the object into a dict
set_rollup_window_request_dict = set_rollup_window_request_instance.to_dict()
# create an instance of SetRollupWindowRequest from a dict
set_rollup_window_request_from_dict = SetRollupWindowRequest.from_dict(set_rollup_window_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


