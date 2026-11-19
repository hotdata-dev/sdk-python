# CreateStreamRequest

Request body for POST /databases/{database_id}/streams

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[StreamColumnHint]**](StreamColumnHint.md) | Columns to define up front, for fields the first rows may lack or whose type or role they cannot show. Other columns come from the first request. | [optional] 
**retention_days** | **int** | Days of rows to keep, 1 or more. Stored but not yet enforced. | [optional] 
**var_schema** | **str** | Schema of the table. Defaults to the database&#39;s default schema. | [optional] 
**table** | **str** | Table the stream writes to. It must not exist yet. | 
**time_column** | **str** | Row field that holds each row&#39;s time; every row must have it. Omit it and &#x60;time_unit&#x60; to have Hotdata add an &#x60;_ingested_at&#x60; column with the time each request arrived. | [optional] 
**time_unit** | **str** | Format of &#x60;time_column&#x60;: &#x60;ns&#x60;, &#x60;us&#x60;, &#x60;ms&#x60; or &#x60;s&#x60; for an integer since the Unix epoch, or &#x60;rfc3339&#x60; for text. Required with &#x60;time_column&#x60;, and only allowed with it. | [optional] 

## Example

```python
from hotdata.models.create_stream_request import CreateStreamRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateStreamRequest from a JSON string
create_stream_request_instance = CreateStreamRequest.from_json(json)
# print the JSON string representation of the object
print(CreateStreamRequest.to_json())

# convert the object into a dict
create_stream_request_dict = create_stream_request_instance.to_dict()
# create an instance of CreateStreamRequest from a dict
create_stream_request_from_dict = CreateStreamRequest.from_dict(create_stream_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


