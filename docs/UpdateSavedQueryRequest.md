# UpdateSavedQueryRequest

Request body for PUT /v1/queries/{id}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category_override** | **str** | Category to use instead of the detected one, such as &#x60;point_lookup&#x60; or &#x60;join&#x60;. Send &#x60;null&#x60; to go back to the detected category. | [optional] 
**description** | **str** | New description. Omit to keep the current one. | [optional] 
**name** | **str** | New name. Omit to keep the current one. | [optional] 
**sql** | **str** | New SQL. Omit to keep the current SQL. | [optional] 
**table_size_override** | **str** | Your own label for the table size. Send &#x60;null&#x60; to clear it. | [optional] 
**tags** | **List[str]** | New tags, replacing the current ones. Omit to keep them. | [optional] 

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


