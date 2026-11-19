# IngestStreamResponse

Response body for POST /streams/{stream_id}/spans/ingest/sync

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[StreamColumn]**](StreamColumn.md) | The stream&#39;s columns. Present only on the request that sets them. | [optional] 
**rows_added** | **int** | Rows the request added. | 

## Example

```python
from hotdata.models.ingest_stream_response import IngestStreamResponse

# TODO update the JSON string below
json = "{}"
# create an instance of IngestStreamResponse from a JSON string
ingest_stream_response_instance = IngestStreamResponse.from_json(json)
# print the JSON string representation of the object
print(IngestStreamResponse.to_json())

# convert the object into a dict
ingest_stream_response_dict = ingest_stream_response_instance.to_dict()
# create an instance of IngestStreamResponse from a dict
ingest_stream_response_from_dict = IngestStreamResponse.from_dict(ingest_stream_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


