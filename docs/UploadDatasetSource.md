# UploadDatasetSource

Create dataset from a previously uploaded file

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **Dict[str, str]** | Optional explicit column definitions. Keys are column names, values are type specs. When provided, the schema is built from these definitions instead of being inferred. | [optional] 
**format** | **str** |  | [optional] 
**upload_id** | **str** |  | 

## Example

```python
from hotdata.models.upload_dataset_source import UploadDatasetSource

# TODO update the JSON string below
json = "{}"
# create an instance of UploadDatasetSource from a JSON string
upload_dataset_source_instance = UploadDatasetSource.from_json(json)
# print the JSON string representation of the object
print(UploadDatasetSource.to_json())

# convert the object into a dict
upload_dataset_source_dict = upload_dataset_source_instance.to_dict()
# create an instance of UploadDatasetSource from a dict
upload_dataset_source_from_dict = UploadDatasetSource.from_dict(upload_dataset_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


