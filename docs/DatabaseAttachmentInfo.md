# DatabaseAttachmentInfo

One attached catalog inside a database.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alias** | **str** | Alias under which this catalog is reachable inside the database. When &#x60;None&#x60;, the catalog is reachable by its original connection name. | [optional] 
**connection_id** | **str** |  | 

## Example

```python
from hotdata.models.database_attachment_info import DatabaseAttachmentInfo

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseAttachmentInfo from a JSON string
database_attachment_info_instance = DatabaseAttachmentInfo.from_json(json)
# print the JSON string representation of the object
print(DatabaseAttachmentInfo.to_json())

# convert the object into a dict
database_attachment_info_dict = database_attachment_info_instance.to_dict()
# create an instance of DatabaseAttachmentInfo from a dict
database_attachment_info_from_dict = DatabaseAttachmentInfo.from_dict(database_attachment_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


