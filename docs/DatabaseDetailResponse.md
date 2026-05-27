# DatabaseDetailResponse

Response body for GET /databases/{database_id}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attachments** | [**List[DatabaseAttachmentInfo]**](DatabaseAttachmentInfo.md) |  | 
**default_connection_id** | **str** |  | 
**expires_at** | **datetime** | When this database expires. | [optional] 
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


