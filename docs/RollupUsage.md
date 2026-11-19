# RollupUsage

Whether a query used a rollup.  - `used`: a rollup answered at least part of the query. - `not_ready`: a table the query read has a rollup, but none is ready   (building, needing a rebuild, or failed). - `not_matched`: a ready rollup exists, but none can answer this query's   shape: its filter, grouping, bucket width or aggregates. - `unavailable`: rollups were not used this time for a transient reason;   the query read the table, and the same query later can use the rollup.  Answers are the same whichever it is.

## Enum

* `USED` (value: `'used'`)

* `NOT_READY` (value: `'not_ready'`)

* `NOT_MATCHED` (value: `'not_matched'`)

* `UNAVAILABLE` (value: `'unavailable'`)

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


