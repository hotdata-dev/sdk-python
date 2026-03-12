# ExecuteSavedQueryRequest

Request body for POST /v1/queries/{id}/execute

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **object** |  | [optional] 

## Example

```python
from hotdata.models.execute_saved_query_request import ExecuteSavedQueryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExecuteSavedQueryRequest from a JSON string
execute_saved_query_request_instance = ExecuteSavedQueryRequest.from_json(json)
# print the JSON string representation of the object
print(ExecuteSavedQueryRequest.to_json())

# convert the object into a dict
execute_saved_query_request_dict = execute_saved_query_request_instance.to_dict()
# create an instance of ExecuteSavedQueryRequest from a dict
execute_saved_query_request_from_dict = ExecuteSavedQueryRequest.from_dict(execute_saved_query_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


