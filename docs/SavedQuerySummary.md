# SavedQuerySummary

Saved query summary for listing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**description** | **str** |  | 
**id** | **str** |  | 
**latest_version** | **int** |  | 
**name** | **str** |  | 
**tags** | **List[str]** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from hotdata.models.saved_query_summary import SavedQuerySummary

# TODO update the JSON string below
json = "{}"
# create an instance of SavedQuerySummary from a JSON string
saved_query_summary_instance = SavedQuerySummary.from_json(json)
# print the JSON string representation of the object
print(SavedQuerySummary.to_json())

# convert the object into a dict
saved_query_summary_dict = saved_query_summary_instance.to_dict()
# create an instance of SavedQuerySummary from a dict
saved_query_summary_from_dict = SavedQuerySummary.from_dict(saved_query_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


