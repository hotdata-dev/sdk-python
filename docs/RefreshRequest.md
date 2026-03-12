# RefreshRequest

Request body for POST /refresh

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_id** | **object** |  | [optional] 
**data** | **bool** |  | [optional] 
**include_uncached** | **bool** | Controls whether uncached tables are included in connection-wide data refresh.  - &#x60;false&#x60; (default): Only refresh tables that already have cached data.   This is the common case for keeping existing data up-to-date. - &#x60;true&#x60;: Also sync tables that haven&#39;t been cached yet, essentially performing   an initial sync for any new tables discovered since the connection was created.  This field only applies to connection-wide data refresh (when &#x60;data&#x3D;true&#x60; and &#x60;table_name&#x60; is not specified). It has no effect on single-table refresh or schema refresh operations. | [optional] 
**schema_name** | **object** |  | [optional] 
**table_name** | **object** |  | [optional] 

## Example

```python
from hotdata.models.refresh_request import RefreshRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RefreshRequest from a JSON string
refresh_request_instance = RefreshRequest.from_json(json)
# print the JSON string representation of the object
print(RefreshRequest.to_json())

# convert the object into a dict
refresh_request_dict = refresh_request_instance.to_dict()
# create an instance of RefreshRequest from a dict
refresh_request_from_dict = RefreshRequest.from_dict(refresh_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


