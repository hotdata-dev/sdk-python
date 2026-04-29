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
**created_at** | **datetime** |  | 
**id** | **str** |  | 
**status** | [**IndexStatus**](IndexStatus.md) |  | 
**version** | **int** |  | 
**columns** | **List[str]** |  | 
**index_name** | **str** |  | 
**index_type** | **str** |  | 
**metric** | **str** | Distance metric this index was built with. Only present for vector indexes. | [optional] 
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


