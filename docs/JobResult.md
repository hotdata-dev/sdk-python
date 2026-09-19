# JobResult

What a finished background job produced. Absent while the job is `pending` or `running`, and absent for job types that report no payload.  Which shape you get is decided by the job's `job_type`, so read `job_type` first and then the matching object — the payload carries no discriminator of its own:  - `create_index` — the created index, in the same shape the index listing   returns. - `managed_load` — the load receipt: rows published and the table's schema   as published, in the same shape a synchronous load returns. - `bulk_create_databases` — the batch's counters: how many databases were   requested, how many were created, and whether the batch was stopped early.  The remaining job types — `noop` and the vacuum, compaction, and cleanup sweeps — report their outcome through `status` and `error_message` alone and leave this absent even once they finish.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | **List[str]** |  | 
**created_at** | **datetime** |  | 
**index_name** | **str** |  | 
**index_type** | **str** |  | 
**metric** | **str** | Distance metric this index was built with. Only present for vector indexes. | [optional] 
**source_column** | **str** | Source text column for an embedding-backed vector index. A query searches it via &#x60;vector_distance(&lt;source_column&gt;, …)&#x60;; the indexed &#x60;columns&#x60; hold the generated embedding column instead. Absent for BM25, sorted, and direct (existing-column) vector indexes. | [optional] 
**status** | [**IndexStatus**](IndexStatus.md) |  | 
**updated_at** | **datetime** |  | 
**vector_precision** | **str** | How precisely this vector index stores each number of a vector, when it was created with an explicit precision. Absent means it stores at the same precision as the column, which is the default. Also absent for BM25 and sorted indexes. | [optional] 
**arrow_schema_json** | **str** | Schema of the loaded table, as JSON. | 
**connection_id** | **str** |  | 
**row_count** | **int** | Total number of rows in the table after the load. | 
**schema_name** | **str** |  | 
**table_name** | **str** |  | 
**batch_id** | **str** | Batch these databases belong to. | 
**cancelled** | **bool** | True when the batch was stopped before finishing. | 
**created** | **int** | How many were created. | 
**requested** | **int** | How many databases were asked for. | 

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


