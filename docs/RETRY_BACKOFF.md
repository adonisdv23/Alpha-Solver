# Retry Backoff

Alpha Solver adapters use an exponential backoff policy with full jitter for
transient failures.  The defaults are:

- `max_retries=3`
- `base_ms=100`
- `max_sleep_ms=1000`
- `timeout_ceiling_ms=2000`

Sleep time for attempt *n* is drawn from `rand(0, base_ms * 2**(n-1))` and
clamped by `max_sleep_ms`.  Total backoff time will never exceed the ceiling.

Only transient errors are retried.  Examples:

- HTTP 429/5xx, timeouts or connection resets are **transient**
- validation errors or most 4xx codes are **fatal**

Retries are executed only when the operation is known to be idempotent.  For
state‑changing operations an explicit idempotency key must be supplied.

Metrics emitted:

- `alpha_adapter_retry_total{adapter, outcome="success|giveup", attempts="N"}`
- `alpha_adapter_retry_sleep_ms_sum{adapter}`

Logs record each failed attempt in a redacted one‑line format:
`adapter=<name> attempt=<n> err_class=<cls> transient=<bool>`.

## Troubleshooting

- Ensure the adapter was invoked with an idempotency key before expecting
  retries for write operations.
- Increase `max_retries` or `base_ms` if transient errors persist but latency
  budget allows.
