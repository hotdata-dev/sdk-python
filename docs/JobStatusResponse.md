# JobStatusResponse

Response body for GET /v1/jobs/{id}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attempts** | **int** | Number of execution attempts (including the current one). | 
**completed_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | 
**error_message** | **str** | Error or warning message. Set when status is &#x60;failed&#x60; or &#x60;partially_succeeded&#x60;. | [optional] 
**id** | **str** |  | 
**job_type** | [**JobType**](JobType.md) |  | 
**result** | [**JobResult**](JobResult.md) | Job-specific result payload. Null while the job is pending or running. | [optional] 
**status** | [**JobStatus**](JobStatus.md) |  | 

## Example

```python
from hotdata.models.job_status_response import JobStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of JobStatusResponse from a JSON string
job_status_response_instance = JobStatusResponse.from_json(json)
# print the JSON string representation of the object
print(JobStatusResponse.to_json())

# convert the object into a dict
job_status_response_dict = job_status_response_instance.to_dict()
# create an instance of JobStatusResponse from a dict
job_status_response_from_dict = JobStatusResponse.from_dict(job_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


