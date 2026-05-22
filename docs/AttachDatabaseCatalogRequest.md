# AttachDatabaseCatalogRequest

Request body for POST /databases/{database_id}/catalogs

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alias** | **str** | Optional alias under which this catalog is reachable inside the database. When omitted, it is reachable by the connection&#39;s name. | [optional] 
**connection_id** | **str** |  | 

## Example

```python
from hotdata.models.attach_database_catalog_request import AttachDatabaseCatalogRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AttachDatabaseCatalogRequest from a JSON string
attach_database_catalog_request_instance = AttachDatabaseCatalogRequest.from_json(json)
# print the JSON string representation of the object
print(AttachDatabaseCatalogRequest.to_json())

# convert the object into a dict
attach_database_catalog_request_dict = attach_database_catalog_request_instance.to_dict()
# create an instance of AttachDatabaseCatalogRequest from a dict
attach_database_catalog_request_from_dict = AttachDatabaseCatalogRequest.from_dict(attach_database_catalog_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


