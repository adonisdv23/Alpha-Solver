# NEW-RETRY-SLO-001 · CI Gate: Retry & Breaker SLOs

Encode stricter retry SLO and circuit-breaker timing in CI gates.

- Failure-injection tests export retry counts and breaker open durations.
- p95 retry count must remain below 2.
- p95 breaker open time must remain below 100ms.
- Jitter is required for both metrics.
- CI job `reliability-slo` fails when thresholds are breached.
