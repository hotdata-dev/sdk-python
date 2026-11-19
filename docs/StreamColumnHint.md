# StreamColumnHint

A stream column defined at creation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Row field the column holds. | 
**role** | **str** | &#x60;large_text&#x60; or &#x60;normal&#x60;. A &#x60;large_text&#x60; column is stored separately, so queries that do not use it do not read it. When omitted, the first request decides it. | [optional] 
**type** | **str** | Column type: &#x60;string&#x60;, &#x60;int64&#x60;, &#x60;float64&#x60;, &#x60;boolean&#x60;, &#x60;timestamp(ns)&#x60;, &#x60;timestamp(us)&#x60;, &#x60;timestamp(ms)&#x60;, &#x60;timestamp(s)&#x60;, &#x60;list&lt;T&gt;&#x60; or &#x60;map&lt;T&gt;&#x60;. When omitted, the first request decides it. | [optional] 

## Example

```python
from hotdata.models.stream_column_hint import StreamColumnHint

# TODO update the JSON string below
json = "{}"
# create an instance of StreamColumnHint from a JSON string
stream_column_hint_instance = StreamColumnHint.from_json(json)
# print the JSON string representation of the object
print(StreamColumnHint.to_json())

# convert the object into a dict
stream_column_hint_dict = stream_column_hint_instance.to_dict()
# create an instance of StreamColumnHint from a dict
stream_column_hint_from_dict = StreamColumnHint.from_dict(stream_column_hint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


