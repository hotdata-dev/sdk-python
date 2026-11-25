# QueryParam

A parameter a saved query declares. Its SQL refers to it as `$name`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default** | **object** | Value used when an execution does not supply one. Without a default, every execution must supply the parameter. &#x60;null&#x60; is a valid default. | [optional] 
**description** | **str** | What the parameter is for. | [optional] 
**name** | **str** | Name used in the SQL after &#x60;$&#x60;. Letters, digits and underscores, starting with a letter or underscore. | 
**type** | **str** | Type of the value: &#x60;string&#x60;, &#x60;int&#x60;, &#x60;float&#x60;, &#x60;bool&#x60;, &#x60;timestamp&#x60;, &#x60;date&#x60; or &#x60;interval&#x60;. | 

## Example

```python
from hotdata.models.query_param import QueryParam

# TODO update the JSON string below
json = "{}"
# create an instance of QueryParam from a JSON string
query_param_instance = QueryParam.from_json(json)
# print the JSON string representation of the object
print(QueryParam.to_json())

# convert the object into a dict
query_param_dict = query_param_instance.to_dict()
# create an instance of QueryParam from a dict
query_param_from_dict = QueryParam.from_dict(query_param_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


