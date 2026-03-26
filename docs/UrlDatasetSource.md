# UrlDatasetSource

Create dataset from an external HTTP URL

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **Dict[str, str]** | Optional explicit column definitions. Keys are column names, values are type specs. | [optional] 
**format** | **str** |  | [optional] 
**url** | **str** |  | 

## Example

```python
from hotdata.models.url_dataset_source import UrlDatasetSource

# TODO update the JSON string below
json = "{}"
# create an instance of UrlDatasetSource from a JSON string
url_dataset_source_instance = UrlDatasetSource.from_json(json)
# print the JSON string representation of the object
print(UrlDatasetSource.to_json())

# convert the object into a dict
url_dataset_source_dict = url_dataset_source_instance.to_dict()
# create an instance of UrlDatasetSource from a dict
url_dataset_source_from_dict = UrlDatasetSource.from_dict(url_dataset_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


