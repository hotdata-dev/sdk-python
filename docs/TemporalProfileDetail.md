# TemporalProfileDetail

Date or timestamp column.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max** | **str** | Latest value as ISO-8601 string | 
**min** | **str** | Earliest value as ISO-8601 string | 

## Example

```python
from hotdata.models.temporal_profile_detail import TemporalProfileDetail

# TODO update the JSON string below
json = "{}"
# create an instance of TemporalProfileDetail from a JSON string
temporal_profile_detail_instance = TemporalProfileDetail.from_json(json)
# print the JSON string representation of the object
print(TemporalProfileDetail.to_json())

# convert the object into a dict
temporal_profile_detail_dict = temporal_profile_detail_instance.to_dict()
# create an instance of TemporalProfileDetail from a dict
temporal_profile_detail_from_dict = TemporalProfileDetail.from_dict(temporal_profile_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


