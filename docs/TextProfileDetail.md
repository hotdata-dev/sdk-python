# TextProfileDetail

High-cardinality text column (>200 distinct values).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**avg_length** | **float** | Average string length | 
**max_length** | **int** | Longest string length in the column | 
**min_length** | **int** | Shortest string length in the column | 

## Example

```python
from hotdata.models.text_profile_detail import TextProfileDetail

# TODO update the JSON string below
json = "{}"
# create an instance of TextProfileDetail from a JSON string
text_profile_detail_instance = TextProfileDetail.from_json(json)
# print the JSON string representation of the object
print(TextProfileDetail.to_json())

# convert the object into a dict
text_profile_detail_dict = text_profile_detail_instance.to_dict()
# create an instance of TextProfileDetail from a dict
text_profile_detail_from_dict = TextProfileDetail.from_dict(text_profile_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


