# CreateDatasetRequest

Request body for POST /v1/datasets

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** |  | 
**source** | [**DatasetSource**](DatasetSource.md) |  | 
**storage_backend** | **str** | Optional storage backend: &#x60;\&quot;parquet\&quot;&#x60; (default) or &#x60;\&quot;ducklake\&quot;&#x60;. &#x60;\&quot;ducklake\&quot;&#x60; requires &#x60;ducklake.metadata_pg_url&#x60; to be configured at engine boot; the engine also rejects the combo of &#x60;storage_backend: \&quot;ducklake\&quot;&#x60; with a saved-query source or with explicit geometry columns (both deferred to a follow-up). | [optional] 
**table_name** | **str** | Optional table_name - if not provided, derived from label | [optional] 

## Example

```python
from hotdata.models.create_dataset_request import CreateDatasetRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDatasetRequest from a JSON string
create_dataset_request_instance = CreateDatasetRequest.from_json(json)
# print the JSON string representation of the object
print(CreateDatasetRequest.to_json())

# convert the object into a dict
create_dataset_request_dict = create_dataset_request_instance.to_dict()
# create an instance of CreateDatasetRequest from a dict
create_dataset_request_from_dict = CreateDatasetRequest.from_dict(create_dataset_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


