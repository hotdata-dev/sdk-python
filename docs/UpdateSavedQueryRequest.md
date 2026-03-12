# UpdateSavedQueryRequest

Request body for PUT /v1/queries/{id}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category_override** | **object** | Override the auto-detected category. Send &#x60;null&#x60; to clear (revert to auto). | [optional] 
**description** | **object** |  | [optional] 
**name** | **object** | Optional new name. When omitted the existing name is preserved. | [optional] 
**sql** | **object** | Optional new SQL. When omitted the existing SQL is preserved. | [optional] 
**table_size_override** | **object** | User annotation for table size. Send &#x60;null&#x60; to clear. | [optional] 
**tags** | **List[str]** |  | [optional] 

## Example

```python
from hotdata.models.update_saved_query_request import UpdateSavedQueryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateSavedQueryRequest from a JSON string
update_saved_query_request_instance = UpdateSavedQueryRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateSavedQueryRequest.to_json())

# convert the object into a dict
update_saved_query_request_dict = update_saved_query_request_instance.to_dict()
# create an instance of UpdateSavedQueryRequest from a dict
update_saved_query_request_from_dict = UpdateSavedQueryRequest.from_dict(update_saved_query_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


