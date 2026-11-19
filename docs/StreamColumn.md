# StreamColumn

One column of a stream's table.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_from** | [**StreamColumnSource**](StreamColumnSource.md) | For a &#x60;map_key&#x60; column, the object field and key it holds. | [optional] 
**indexed** | **bool** | True for the &#x60;large_text&#x60; column that has a text index. Omitted when false. | [optional] 
**name** | **str** | Column name. | 
**role** | **str** | &#x60;time&#x60;, &#x60;large_text&#x60;, &#x60;normal&#x60;, &#x60;map_key&#x60; or &#x60;extra&#x60;. | 
**type** | **str** | Column type: &#x60;string&#x60;, &#x60;int64&#x60;, &#x60;float64&#x60;, &#x60;boolean&#x60;, &#x60;timestamp(ns)&#x60;, &#x60;timestamp(us)&#x60;, &#x60;timestamp(ms)&#x60;, &#x60;timestamp(s)&#x60;, &#x60;list&lt;T&gt;&#x60; or &#x60;map&lt;T&gt;&#x60;. | 

## Example

```python
from hotdata.models.stream_column import StreamColumn

# TODO update the JSON string below
json = "{}"
# create an instance of StreamColumn from a JSON string
stream_column_instance = StreamColumn.from_json(json)
# print the JSON string representation of the object
print(StreamColumn.to_json())

# convert the object into a dict
stream_column_dict = stream_column_instance.to_dict()
# create an instance of StreamColumn from a dict
stream_column_from_dict = StreamColumn.from_dict(stream_column_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


