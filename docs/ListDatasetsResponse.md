# ListDatasetsResponse

Response body for GET /v1/datasets

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of datasets returned in this response | 
**datasets** | [**List[DatasetSummary]**](DatasetSummary.md) |  | 
**has_more** | **bool** | Whether there are more datasets available after this page | 
**limit** | **int** | Limit used for this request | 
**offset** | **int** | Pagination offset used for this request | 

## Example

```python
from hotdata.models.list_datasets_response import ListDatasetsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListDatasetsResponse from a JSON string
list_datasets_response_instance = ListDatasetsResponse.from_json(json)
# print the JSON string representation of the object
print(ListDatasetsResponse.to_json())

# convert the object into a dict
list_datasets_response_dict = list_datasets_response_instance.to_dict()
# create an instance of ListDatasetsResponse from a dict
list_datasets_response_from_dict = ListDatasetsResponse.from_dict(list_datasets_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


