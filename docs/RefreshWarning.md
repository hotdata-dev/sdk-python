# RefreshWarning

Non-fatal warning that occurred during a refresh operation. Used to report issues like failed deletion scheduling that don't prevent the refresh from succeeding.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | 
**schema_name** | **str** |  | [optional] 
**table_name** | **str** |  | [optional] 

## Example

```python
from hotdata.models.refresh_warning import RefreshWarning

# TODO update the JSON string below
json = "{}"
# create an instance of RefreshWarning from a JSON string
refresh_warning_instance = RefreshWarning.from_json(json)
# print the JSON string representation of the object
print(RefreshWarning.to_json())

# convert the object into a dict
refresh_warning_dict = refresh_warning_instance.to_dict()
# create an instance of RefreshWarning from a dict
refresh_warning_from_dict = RefreshWarning.from_dict(refresh_warning_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


