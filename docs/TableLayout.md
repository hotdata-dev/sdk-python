# TableLayout

How a table's data files are written. Set when the table is created and fixed after that.  - `analytical` (default): data pages sized for scans. - `point_lookup`: small data pages, so fetching rows by ID is cheap, as   vector search results do. Scans of the table read more pages.

## Enum

* `ANALYTICAL` (value: `'analytical'`)

* `POINT_LOOKUP` (value: `'point_lookup'`)

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


