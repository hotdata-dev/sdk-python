# ConnectionTypeDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auth** | **object** |  | [optional] 
**config_schema** | **object** |  | [optional] 
**label** | **str** |  | 
**name** | **str** |  | 

## Example

```python
from hotdata.models.connection_type_detail import ConnectionTypeDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectionTypeDetail from a JSON string
connection_type_detail_instance = ConnectionTypeDetail.from_json(json)
# print the JSON string representation of the object
print(ConnectionTypeDetail.to_json())

# convert the object into a dict
connection_type_detail_dict = connection_type_detail_instance.to_dict()
# create an instance of ConnectionTypeDetail from a dict
connection_type_detail_from_dict = ConnectionTypeDetail.from_dict(connection_type_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


