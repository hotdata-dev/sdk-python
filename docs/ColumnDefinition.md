# ColumnDefinition

A column's type in a load request's `columns` map. Either a type name, such as `\"BIGINT\"` or `\"DECIMAL(10,2)\"`, or an object such as `{ \"type\": \"DECIMAL\", \"precision\": 10, \"scale\": 2 }`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**precision** | **int** | Total digits for &#x60;DECIMAL&#x60; or &#x60;NUMERIC&#x60;, from 1 to 38. | [optional] 
**scale** | **int** | Digits after the decimal point for &#x60;DECIMAL&#x60; or &#x60;NUMERIC&#x60;. Requires &#x60;precision&#x60; and cannot exceed it; defaults to 0. | [optional] 
**type** | **str** | Type name, such as &#x60;\&quot;DECIMAL\&quot;&#x60;, &#x60;\&quot;TIMESTAMP\&quot;&#x60; or &#x60;\&quot;VARCHAR\&quot;&#x60;. | 

## Example

```python
from hotdata.models.column_definition import ColumnDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnDefinition from a JSON string
column_definition_instance = ColumnDefinition.from_json(json)
# print the JSON string representation of the object
print(ColumnDefinition.to_json())

# convert the object into a dict
column_definition_dict = column_definition_instance.to_dict()
# create an instance of ColumnDefinition from a dict
column_definition_from_dict = ColumnDefinition.from_dict(column_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


