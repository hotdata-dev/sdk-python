# SubmitJobResponse

A background job that was started. Poll `status_url` to follow it.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Job ID. | 
**status** | [**JobStatus**](JobStatus.md) | Current job status. | 
**status_url** | **str** | Path to poll for the job&#39;s status. | 

## Example

```python
from hotdata.models.submit_job_response import SubmitJobResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitJobResponse from a JSON string
submit_job_response_instance = SubmitJobResponse.from_json(json)
# print the JSON string representation of the object
print(SubmitJobResponse.to_json())

# convert the object into a dict
submit_job_response_dict = submit_job_response_instance.to_dict()
# create an instance of SubmitJobResponse from a dict
submit_job_response_from_dict = SubmitJobResponse.from_dict(submit_job_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


