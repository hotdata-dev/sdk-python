# DeclareRollupRequest

A rollup to declare on one table. A rollup keeps pre-aggregated rows, one per time bucket and set of dimension values, and answers matching aggregate queries from them.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bucket_width_secs** | **int** | Width of each time bucket, in seconds. Buckets align to the Unix epoch, in UTC. A query uses the rollup when its own time buckets are a multiple of this width. | 
**dimensions** | **List[str]** | Columns to group by, besides the time bucket. A query can also filter on these columns and still use the rollup. | [optional] 
**filter** | **str** | SQL condition a row must pass to be kept; omit it to keep every row. A query uses the rollup only when its &#x60;WHERE&#x60; clause contains each &#x60;AND&#x60;-joined part written the same way, and the condition must be deterministic (no subqueries, aggregates, &#x60;now()&#x60; or &#x60;random()&#x60;). | [optional] 
**measures** | [**List[RollupMeasure]**](RollupMeasure.md) | Aggregates each rollup row keeps. | 
**schema_name** | **str** | Schema that holds the table. | 
**table_name** | **str** | Table to roll up. | 
**time_column** | **str** | Timestamp column to bucket rows by. It must have no time zone, or be in UTC. | 
**window_secs** | **int** | How long, in seconds, after a row&#39;s time it can still be changed or deleted; later edits are refused, appends are always allowed. Shared by every rollup on the table: the first sets it (default one hour), later ones must match or omit it. | [optional] 

## Example

```python
from hotdata.models.declare_rollup_request import DeclareRollupRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeclareRollupRequest from a JSON string
declare_rollup_request_instance = DeclareRollupRequest.from_json(json)
# print the JSON string representation of the object
print(DeclareRollupRequest.to_json())

# convert the object into a dict
declare_rollup_request_dict = declare_rollup_request_instance.to_dict()
# create an instance of DeclareRollupRequest from a dict
declare_rollup_request_from_dict = DeclareRollupRequest.from_dict(declare_rollup_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


