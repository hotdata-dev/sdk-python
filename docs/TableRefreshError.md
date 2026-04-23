# TableRefreshError

Error details for a failed table refresh.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** |  | 
**schema_name** | **str** |  | 
**table_name** | **str** |  | 

## Example

```python
from hotdata.models.table_refresh_error import TableRefreshError

# TODO update the JSON string below
json = "{}"
# create an instance of TableRefreshError from a JSON string
table_refresh_error_instance = TableRefreshError.from_json(json)
# print the JSON string representation of the object
print(TableRefreshError.to_json())

# convert the object into a dict
table_refresh_error_dict = table_refresh_error_instance.to_dict()
# create an instance of TableRefreshError from a dict
table_refresh_error_from_dict = TableRefreshError.from_dict(table_refresh_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


