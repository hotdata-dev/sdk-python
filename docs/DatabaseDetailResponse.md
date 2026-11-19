# DatabaseDetailResponse

Response body for GET /databases/{database_id}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attachments** | [**List[DatabaseAttachmentInfo]**](DatabaseAttachmentInfo.md) | Catalogs attached from other connections or databases. | 
**created_at** | **datetime** | When the database was created. | [optional] 
**default_catalog** | **str** | Name of the database&#39;s own catalog in SQL. | 
**default_connection_id** | **str** | ID of the connection behind the database&#39;s own catalog. Use it to load tables through the connection endpoints, or to attach this catalog to another database. | 
**default_schema** | **str** | Schema that unqualified table names resolve to. | 
**expires_at** | **datetime** | When the database expires. | [optional] 
**forked_from** | [**ForkedFromInfo**](ForkedFromInfo.md) | Present on a fork: the database it was copied from. | [optional] 
**id** | **str** |  | 
**name** | **str** |  | [optional] 

## Example

```python
from hotdata.models.database_detail_response import DatabaseDetailResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseDetailResponse from a JSON string
database_detail_response_instance = DatabaseDetailResponse.from_json(json)
# print the JSON string representation of the object
print(DatabaseDetailResponse.to_json())

# convert the object into a dict
database_detail_response_dict = database_detail_response_instance.to_dict()
# create an instance of DatabaseDetailResponse from a dict
database_detail_response_from_dict = DatabaseDetailResponse.from_dict(database_detail_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


