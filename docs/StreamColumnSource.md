# StreamColumnSource

The object field and key a `map_key` column holds.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | Key inside that field. | 
**map** | **str** | Name of the object field. | 

## Example

```python
from hotdata.models.stream_column_source import StreamColumnSource

# TODO update the JSON string below
json = "{}"
# create an instance of StreamColumnSource from a JSON string
stream_column_source_instance = StreamColumnSource.from_json(json)
# print the JSON string representation of the object
print(StreamColumnSource.to_json())

# convert the object into a dict
stream_column_source_dict = stream_column_source_instance.to_dict()
# create an instance of StreamColumnSource from a dict
stream_column_source_from_dict = StreamColumnSource.from_dict(stream_column_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


