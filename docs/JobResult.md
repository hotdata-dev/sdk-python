# JobResult

Job-specific result payload. The shape depends on the job type. Null while the job is pending or running.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_id** | **str** |  | 
**duration_ms** | **int** |  | 
**rows_synced** | **int** |  | 
**schema_name** | **str** |  | 
**table_name** | **str** |  | 
**warnings** | [**List[RefreshWarning]**](RefreshWarning.md) |  | [optional] 
**errors** | [**List[TableRefreshError]**](TableRefreshError.md) |  | [optional] 
**tables_failed** | **int** |  | 
**tables_refreshed** | **int** |  | 
**total_rows** | **int** |  | 
**columns** | **List[str]** |  | 
**created_at** | **datetime** |  | 
**index_name** | **str** |  | 
**index_type** | **str** |  | 
**metric** | **str** | Distance metric this index was built with. Only present for vector indexes. | [optional] 
**source_column** | **str** | Source text column for an embedding-backed vector index. A query searches it via &#x60;vector_distance(&lt;source_column&gt;, …)&#x60;; the indexed &#x60;columns&#x60; hold the generated embedding column instead. Absent for BM25, sorted, and direct (existing-column) vector indexes. | [optional] 
**status** | [**IndexStatus**](IndexStatus.md) |  | 
**updated_at** | **datetime** |  | 

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


