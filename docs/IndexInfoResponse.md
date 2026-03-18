# IndexInfoResponse

Response for index endpoints.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**index_name** | **str** |  | 
**index_type** | **str** |  | 
**metric** | **str** | Distance metric this index was built with. Only present for vector indexes. | [optional] 
**sort_columns** | **List[str]** |  | 
**status** | [**IndexStatus**](IndexStatus.md) |  | 
**text_columns** | **List[str]** |  | 
**updated_at** | **datetime** |  | 
**vector_columns** | **List[str]** |  | 

## Example

```python
from hotdata.models.index_info_response import IndexInfoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of IndexInfoResponse from a JSON string
index_info_response_instance = IndexInfoResponse.from_json(json)
# print the JSON string representation of the object
print(IndexInfoResponse.to_json())

# convert the object into a dict
index_info_response_dict = index_info_response_instance.to_dict()
# create an instance of IndexInfoResponse from a dict
index_info_response_from_dict = IndexInfoResponse.from_dict(index_info_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


