# DatabaseCountResponse

Response body for GET /databases/count.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** | Total databases matching the filters, across all pages. | 

## Example

```python
from hotdata.models.database_count_response import DatabaseCountResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseCountResponse from a JSON string
database_count_response_instance = DatabaseCountResponse.from_json(json)
# print the JSON string representation of the object
print(DatabaseCountResponse.to_json())

# convert the object into a dict
database_count_response_dict = database_count_response_instance.to_dict()
# create an instance of DatabaseCountResponse from a dict
database_count_response_from_dict = DatabaseCountResponse.from_dict(database_count_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


