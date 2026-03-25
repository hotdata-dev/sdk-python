# CreateIndexRequest

Request body for POST .../indexes

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_async** | **bool** | When true, create the index as a background job and return a job ID for polling. | [optional] 
**columns** | **List[str]** | Columns to index. Required for all index types. | 
**index_name** | **str** |  | 
**index_type** | **str** | Index type: \&quot;sorted\&quot; (default), \&quot;bm25\&quot;, or \&quot;vector\&quot; | [optional] 
**metric** | **str** | Distance metric for vector indexes: \&quot;l2\&quot; (default), \&quot;cosine\&quot;, or \&quot;dot\&quot;. Only relevant when index_type &#x3D; \&quot;vector\&quot;. | [optional] 

## Example

```python
from hotdata.models.create_index_request import CreateIndexRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateIndexRequest from a JSON string
create_index_request_instance = CreateIndexRequest.from_json(json)
# print the JSON string representation of the object
print(CreateIndexRequest.to_json())

# convert the object into a dict
create_index_request_dict = create_index_request_instance.to_dict()
# create an instance of CreateIndexRequest from a dict
create_index_request_from_dict = CreateIndexRequest.from_dict(create_index_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


