# ResultsFormatQuery

Schema for the `?format=` query parameter on `GET /v1/results/{id}`.  Documents the canonical values that SDKs should treat as a closed set (`arrow`, `json`, `csv`, `md`, `parquet`). The runtime handler's negotiator (`negotiate_results_format`) additionally accepts `markdown` as an alias for `md` — case-insensitive, with unknown values falling through to the `Accept` header — but `markdown` is intentionally NOT listed in this enum so SDK generators emit a single canonical `Markdown` (or equivalent) variant rather than two distinct ones for the same logical format.

## Enum

* `ARROW` (value: `'arrow'`)

* `JSON` (value: `'json'`)

* `CSV` (value: `'csv'`)

* `MD` (value: `'md'`)

* `PARQUET` (value: `'parquet'`)

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


