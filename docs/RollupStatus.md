# RollupStatus

A rollup's state. Queries use a rollup only when it is `ready`.  - `building`: building its first rows. - `ready`: can answer queries. - `needs_rebuild`: a change to its table it cannot follow; it needs a rebuild. - `dropping`: being dropped. - `build_failed`: the build failed. Progress is kept; request a rebuild to   resume.

## Enum

* `BUILDING` (value: `'building'`)

* `READY` (value: `'ready'`)

* `NEEDS_REBUILD` (value: `'needs_rebuild'`)

* `DROPPING` (value: `'dropping'`)

* `BUILD_FAILED` (value: `'build_failed'`)

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


