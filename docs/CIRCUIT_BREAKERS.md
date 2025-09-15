# Circuit Breakers

Adapters are wrapped with a light–weight circuit breaker to prevent cascading
failures when upstream services misbehave. Each adapter maintains its own
breaker state machine:

```
CLOSED --(failures >= threshold)--> OPEN --(timeout)--> HALF_OPEN
HALF_OPEN --(success)--> CLOSED
HALF_OPEN --(failure)--> OPEN (with backoff)
```

## Defaults
- `failure_threshold`: 5 consecutive failures
- `recovery_timeout_ms`: 10000 ms before half‑open trial
- `half_open_max_calls`: 1
- `backoff_base_ms`: 200 with ±30% jitter

These values can be overridden in configuration under the `adapters` section.

## Behaviour
- **Closed** – calls flow through normally.
- **Open** – calls short‑circuit and a structured fallback is returned:
  `{"adapter_skipped": true, "reason": "circuit_open"}`.
- **Half‑open** – allows a limited trial call to probe recovery.

Repeated failures while half‑open push the breaker back to open and extend the
next recovery window using exponential backoff with jitter.

## Metrics
The following Prometheus metrics are exported per adapter:

- `alpha_adapter_breaker_state{adapter, state}` – gauge with current state
- `alpha_adapter_calls_total{adapter, result}` – success/failure/fallback counts
- `alpha_adapter_open_total{adapter}` – total number of times the breaker opened

## Troubleshooting
- Inspect the metrics above to determine why an adapter is being skipped.
- Increase `failure_threshold` or decrease `recovery_timeout_ms` if the breaker
  is too aggressive for a given adapter.
- Ensure no secrets are included in logs; only counts and reasons are logged.
