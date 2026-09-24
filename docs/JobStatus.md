# JobStatus

Current status of a background job. One of five values:  - `pending` — queued, not started yet. - `running` — currently executing. - `succeeded` — finished, everything it was asked to do worked. - `partially_succeeded` — finished, but some of its work failed while the   rest succeeded (for example some of the databases in a bulk creation).   Read `error_message` for what was skipped. - `failed` — did not finish; every retry was used up. Read `error_message`.  `succeeded`, `partially_succeeded`, and `failed` are final — a job in one of those will not change again, so a poll loop can stop there. `pending` and `running` mean keep polling. Treat `partially_succeeded` as its own outcome rather than folding it into either success or failure: the job produced a `result`, but not for all of its work.

## Enum

* `PENDING` (value: `'pending'`)

* `RUNNING` (value: `'running'`)

* `SUCCEEDED` (value: `'succeeded'`)

* `PARTIALLY_SUCCEEDED` (value: `'partially_succeeded'`)

* `FAILED` (value: `'failed'`)

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


