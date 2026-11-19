# IngestStreamRequest

Request body for POST /streams/{stream_id}/spans/ingest/sync

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**spans** | **List[Dict[str, object]]** | Rows to append. Each row is an object of field names to values. | 

## Example

```python
from hotdata.models.ingest_stream_request import IngestStreamRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IngestStreamRequest from a JSON string
ingest_stream_request_instance = IngestStreamRequest.from_json(json)
# print the JSON string representation of the object
print(IngestStreamRequest.to_json())

# convert the object into a dict
ingest_stream_request_dict = ingest_stream_request_instance.to_dict()
# create an instance of IngestStreamRequest from a dict
ingest_stream_request_from_dict = IngestStreamRequest.from_dict(ingest_stream_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


