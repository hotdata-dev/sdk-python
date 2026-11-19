# CreateConnectionRequest

Request body for POST /connections

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | **Dict[str, object]** | Connection settings. For &#x60;managed&#x60;, an optional &#x60;schemas&#x60; list declaring schemas and their tables. | 
**name** | **str** |  | 
**source_type** | **str** | Connection type. Only &#x60;managed&#x60; can be created: a catalog of tables you load data into. | 

## Example

```python
from hotdata.models.create_connection_request import CreateConnectionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConnectionRequest from a JSON string
create_connection_request_instance = CreateConnectionRequest.from_json(json)
# print the JSON string representation of the object
print(CreateConnectionRequest.to_json())

# convert the object into a dict
create_connection_request_dict = create_connection_request_instance.to_dict()
# create an instance of CreateConnectionRequest from a dict
create_connection_request_from_dict = CreateConnectionRequest.from_dict(create_connection_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


