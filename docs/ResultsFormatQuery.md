# ResultsFormatQuery

Schema for the `?format=` query parameter on `GET /v1/results/{id}`.  Documents the canonical values accepted (`arrow`, `json`). The handler's negotiator (`negotiate_results_format`) is intentionally permissive — case-insensitive, with unknown values falling through to the `Accept` header — so this enum only declares the spec-level contract for clients and SDK generators.

## Enum

* `ARROW` (value: `'arrow'`)

* `JSON` (value: `'json'`)

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


