# Rollup

A rollup on a database's table: what it keeps, and its state. Queries use it only when `status` is `ready`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bucket_width_secs** | **int** | Width of each time bucket, in seconds. | 
**covered_until** | **datetime** | End (exclusive) of the time range the rollup has built; null until the build&#39;s first step. Build progress, not freshness: queries also read the table for rows the rollup has not absorbed, so answers are the same either way. It advances while &#x60;building&#x60;, and after the table is replaced it describes the old table until the rollup is rebuilt. | [optional] 
**created_at** | **datetime** | When the rollup was declared. | 
**database_id** | **str** | Database that holds the table. | 
**dimensions** | **List[str]** | Columns rows are grouped by, besides the time bucket. | 
**error** | **str** | Why the build failed, when status is &#x60;build_failed&#x60;; null otherwise. | [optional] 
**failed_at** | **datetime** | When the build failed, when status is &#x60;build_failed&#x60;; null otherwise. | [optional] 
**filter** | **str** | Condition a row must pass to be kept; absent when every row is kept. | [optional] 
**id** | **str** | Rollup ID. | 
**measures** | [**List[RollupMeasure]**](RollupMeasure.md) | The measures, as declared. | 
**schema_name** | **str** | Schema of the table. | 
**status** | [**RollupStatus**](RollupStatus.md) |  | 
**table_name** | **str** | The table the rollup is declared on. | 
**time_column** | **str** | Timestamp column rows are bucketed by. | 
**updated_at** | **datetime** | When the rollup last changed. | 
**window_secs** | **int** | How long, in seconds, after a row&#39;s time it can still be changed or deleted. Shared by every rollup on the table. Null when the table&#39;s state cannot be read, or the table was dropped and created again since the rollup was declared. | [optional] 

## Example

```python
from hotdata.models.rollup import Rollup

# TODO update the JSON string below
json = "{}"
# create an instance of Rollup from a JSON string
rollup_instance = Rollup.from_json(json)
# print the JSON string representation of the object
print(Rollup.to_json())

# convert the object into a dict
rollup_dict = rollup_instance.to_dict()
# create an instance of Rollup from a dict
rollup_from_dict = Rollup.from_dict(rollup_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


