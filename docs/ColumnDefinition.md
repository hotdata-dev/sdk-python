# ColumnDefinition

The declared type of one column, as written in a load request's `columns` map.  Accepts either a bare type name or an object carrying the extra parameters some types need:  - simple: `\"VARCHAR\"`, `\"BIGINT\"`, `\"DECIMAL(10,2)\"` - detailed: `{ \"type\": \"DECIMAL\", \"precision\": 10, \"scale\": 2 }`

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**precision** | **int** | Total number of digits for &#x60;DECIMAL&#x60; / &#x60;NUMERIC&#x60; (1–38). | [optional] 
**scale** | **int** | Number of digits after the decimal point for &#x60;DECIMAL&#x60; / &#x60;NUMERIC&#x60;. Requires &#x60;precision&#x60;, and cannot exceed it. | [optional] 
**type** | **str** | The type name, e.g. &#x60;\&quot;DECIMAL\&quot;&#x60;, &#x60;\&quot;TIMESTAMP\&quot;&#x60;, &#x60;\&quot;VARCHAR\&quot;&#x60;. | 

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


