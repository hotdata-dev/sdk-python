# CreateSavedQueryRequest

Request body for POST /v1/queries

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | [optional] 
**name** | **str** |  | 
**params** | [**List[QueryParam]**](QueryParam.md) | Parameters the SQL uses, written in it as &#x60;$name&#x60;. Each value is checked against its type and bound as a value when the query runs, never as SQL text. Every &#x60;$name&#x60; in the SQL must be declared here, and every declared parameter must appear in the SQL. | [optional] 
**sql** | **str** |  | 
**tags** | **List[str]** |  | [optional] 

## Example

```python
from hotdata.models.create_saved_query_request import CreateSavedQueryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSavedQueryRequest from a JSON string
create_saved_query_request_instance = CreateSavedQueryRequest.from_json(json)
# print the JSON string representation of the object
print(CreateSavedQueryRequest.to_json())

# convert the object into a dict
create_saved_query_request_dict = create_saved_query_request_instance.to_dict()
# create an instance of CreateSavedQueryRequest from a dict
create_saved_query_request_from_dict = CreateSavedQueryRequest.from_dict(create_saved_query_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


