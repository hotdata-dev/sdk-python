# ConnectionTypeSummary


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** |  | 
**name** | **str** |  | 

## Example

```python
from hotdata.models.connection_type_summary import ConnectionTypeSummary

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectionTypeSummary from a JSON string
connection_type_summary_instance = ConnectionTypeSummary.from_json(json)
# print the JSON string representation of the object
print(ConnectionTypeSummary.to_json())

# convert the object into a dict
connection_type_summary_dict = connection_type_summary_instance.to_dict()
# create an instance of ConnectionTypeSummary from a dict
connection_type_summary_from_dict = ConnectionTypeSummary.from_dict(connection_type_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


