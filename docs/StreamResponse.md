# StreamResponse

A stream.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column_hints** | [**List[StreamColumnHint]**](StreamColumnHint.md) | Columns the stream was created with. Omitted when there are none. | [optional] 
**columns** | [**List[StreamColumn]**](StreamColumn.md) | The stream&#39;s columns, in table order. Omitted until the first request sets them. | [optional] 
**id** | **str** | Stream ID. | 
**last_flushed_at** | **datetime** | When rows were last stored. Null before the first time. | [optional] 
**oldest_pending_age_ms** | **int** | How long the oldest of those rows has waited, in milliseconds. Null when none waits. | [optional] 
**pending_bytes** | **int** | Bytes of accepted rows that the answering server has not stored yet. Null when it holds none. | [optional] 
**retention_days** | **int** | Days of rows to keep. Omitted when none was set. | [optional] 
**rows** | **int** | Rows stored in the table. | 
**var_schema** | **str** | Schema of the stream&#39;s table. | 
**status** | **str** | &#x60;waiting_for_data&#x60; until the first request, then &#x60;active&#x60;. | 
**table** | **str** | Table the stream writes to. | 
**time_column** | **str** | Row field that holds each row&#39;s time. Null when Hotdata sets the time in &#x60;_ingested_at&#x60;. | [optional] 
**time_unit** | **str** | Format of &#x60;time_column&#x60;: &#x60;ns&#x60;, &#x60;us&#x60;, &#x60;ms&#x60;, &#x60;s&#x60; or &#x60;rfc3339&#x60;. Null when &#x60;time_column&#x60; is null. | [optional] 

## Example

```python
from hotdata.models.stream_response import StreamResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StreamResponse from a JSON string
stream_response_instance = StreamResponse.from_json(json)
# print the JSON string representation of the object
print(StreamResponse.to_json())

# convert the object into a dict
stream_response_dict = stream_response_instance.to_dict()
# create an instance of StreamResponse from a dict
stream_response_from_dict = StreamResponse.from_dict(stream_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


