# JobResult

What a finished job produced. The shape depends on the job's `job_type`:  - `create_index`: the created index. - `managed_load`: the table's row count and schema after the load. - `bulk_create_databases`: how many databases were requested and created,   and whether the batch was cancelled.  Other job types have no result.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**algorithm** | **str** | Vector index algorithm: &#x60;hnsw&#x60; or &#x60;ivf&#x60;. Absent for other index types. | [optional] 
**columns** | **List[str]** | Indexed columns. | 
**created_at** | **datetime** | When the index was created. | 
**index_name** | **str** | Index name. | 
**index_type** | **str** | Index type: &#x60;sorted&#x60;, &#x60;bm25&#x60; or &#x60;vector&#x60;. | 
**metric** | **str** | Distance metric of a vector index. Absent for other index types. | [optional] 
**nlist** | **int** | Number of clusters an &#x60;ivf&#x60; index was built with. Can be lower than the requested &#x60;nlist&#x60;, because it is capped by the number of vectors the clusters were fitted to. | [optional] 
**probe_fraction** | **float** | Share of an &#x60;ivf&#x60; index each search reads, from 0 (exclusive) to 1, when set at creation. When absent, Hotdata picks the share for each search. | [optional] 
**source_column** | **str** | Text column an embedding-based vector index was built from; search it with &#x60;vector_distance(&lt;source_column&gt;, …)&#x60;. &#x60;columns&#x60; then holds the generated embedding column. Absent for other indexes. | [optional] 
**status** | [**IndexStatus**](IndexStatus.md) |  | 
**updated_at** | **datetime** | When the index was last updated. | 
**vector_precision** | **str** | Precision a vector index stores each number at, such as &#x60;int8&#x60;. Always set for &#x60;ivf&#x60; (default &#x60;int8&#x60;); for &#x60;hnsw&#x60;, set only when chosen at creation, and otherwise it matches the column. | [optional] 
**arrow_schema_json** | **str** | The table&#39;s schema, as a JSON string. | 
**connection_id** | **str** | ID of the connection that holds the table. | 
**row_count** | **int** | Total rows in the table after the load. | 
**schema_name** | **str** | Schema of the table. | 
**table_name** | **str** | Table that was loaded. | 
**batch_id** | **str** | ID of the batch. | 
**cancelled** | **bool** | Whether the batch was stopped before it finished. | 
**created** | **int** | Number of databases created. | 
**requested** | **int** | Number of databases requested. | 

## Example

```python
from hotdata.models.job_result import JobResult

# TODO update the JSON string below
json = "{}"
# create an instance of JobResult from a JSON string
job_result_instance = JobResult.from_json(json)
# print the JSON string representation of the object
print(JobResult.to_json())

# convert the object into a dict
job_result_dict = job_result_instance.to_dict()
# create an instance of JobResult from a dict
job_result_from_dict = JobResult.from_dict(job_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


