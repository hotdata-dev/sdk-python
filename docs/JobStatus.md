# JobStatus

Status of a background job. `succeeded`, `partially_succeeded` and `failed` are final; keep polling while it is `pending` or `running`.  - `pending`: queued, or waiting to retry. - `running`: in progress. - `succeeded`: finished; all its work succeeded. - `partially_succeeded`: finished with a `result`, but some of its work   failed (for example, some databases in a bulk creation). See   `error_message`. - `failed`: failed and will not be retried. See `error_message`.

## Enum

* `PENDING` (value: `'pending'`)

* `RUNNING` (value: `'running'`)

* `SUCCEEDED` (value: `'succeeded'`)

* `PARTIALLY_SUCCEEDED` (value: `'partially_succeeded'`)

* `FAILED` (value: `'failed'`)

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


