# Circuit Breakers

Per-adapter circuit breakers guard flaky adapters and expose metrics.

## States
- **closed**: normal operation. Failures increment a counter.
- **open**: adapter is skipped and a fallback result is returned.
- **half_open**: limited trial after recovery timeout.

### Transitions
1. `closed` → `open` when consecutive failures reach the threshold.
2. `open` → `half_open` after `recovery_timeout_ms`.
3. `half_open` → `closed` on success.
4. `half_open` → `open` on failure (jittered backoff applied).

Defaults:
```
failure_threshold: 5
recovery_timeout_ms: 10000
half_open_max_calls: 1
backoff_base_ms: 200 (±30% jitter)
```

## Metrics
```
alpha_adapter_breaker_state{adapter, state}
alpha_adapter_calls_total{adapter, result="success|failure|fallback"}
alpha_adapter_open_total{adapter}
```

## Fallback
When a breaker is open the adapter is skipped and the router may fall back to
LLM-only responses. The wrapper returns:
`{"adapter_skipped": true, "reason": "circuit_open"}`.

## Troubleshooting
- Check `/metrics` for breaker state and open counters.
- Reduce thresholds for noisy environments via adapter config.
