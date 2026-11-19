# RollupBuildResponse

A rollup and the job that builds it.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **str** | Background job that builds the rollup: poll &#x60;GET /v1/jobs/{job_id}&#x60; to follow it; the rollup becomes &#x60;ready&#x60; once the build catches up with the table. Null when the build could not be started: the rollup stays &#x60;building&#x60;, and rebuilding it starts the build. | [optional] 
**rollup** | [**Rollup**](Rollup.md) |  | 

## Example

```python
from hotdata.models.rollup_build_response import RollupBuildResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RollupBuildResponse from a JSON string
rollup_build_response_instance = RollupBuildResponse.from_json(json)
# print the JSON string representation of the object
print(RollupBuildResponse.to_json())

# convert the object into a dict
rollup_build_response_dict = rollup_build_response_instance.to_dict()
# create an instance of RollupBuildResponse from a dict
rollup_build_response_from_dict = RollupBuildResponse.from_dict(rollup_build_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


