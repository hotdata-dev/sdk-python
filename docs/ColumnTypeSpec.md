# ColumnTypeSpec

A column type plus the parameters that cannot be expressed by a bare name.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**precision** | **int** | Total number of digits for &#x60;DECIMAL&#x60; / &#x60;NUMERIC&#x60; (1–38). | [optional] 
**scale** | **int** | Number of digits after the decimal point for &#x60;DECIMAL&#x60; / &#x60;NUMERIC&#x60;. Requires &#x60;precision&#x60;, and cannot exceed it. | [optional] 
**type** | **str** | The type name, e.g. &#x60;\&quot;DECIMAL\&quot;&#x60;, &#x60;\&quot;TIMESTAMP\&quot;&#x60;, &#x60;\&quot;VARCHAR\&quot;&#x60;. | 

## Example

```python
from hotdata.models.column_type_spec import ColumnTypeSpec

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnTypeSpec from a JSON string
column_type_spec_instance = ColumnTypeSpec.from_json(json)
# print the JSON string representation of the object
print(ColumnTypeSpec.to_json())

# convert the object into a dict
column_type_spec_dict = column_type_spec_instance.to_dict()
# create an instance of ColumnTypeSpec from a dict
column_type_spec_from_dict = ColumnTypeSpec.from_dict(column_type_spec_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


