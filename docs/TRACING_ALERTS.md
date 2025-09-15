# Distributed Tracing & Alerts

This project ships with light‑weight helpers for distributed tracing and
in‑process alerting.

## Tracing

`service.otel` exposes `init_tracer()` and a `span()` context manager.  The
tracer uses an in‑memory exporter so traces can be inspected locally without
external infrastructure.

Example:

```python
from service import otel

tracer = otel.init_tracer()

with otel.span("alpha.router", request_id="123", tenant_id="acme"):
    with otel.span("alpha.gates"):
        with otel.span("alpha.adapter"):
            pass
```

Span attributes such as `decision`, `budget_verdict`, `cost_usd`, `tokens` and
`latency_ms` are supported.  Obvious PII (`user_input`, `secret`, etc.) is
redacted automatically.

## Alerts

`service.alerts.AlertManager` monitors request latencies and budget events.  Two
rules are provided:

* **p95 latency** – emits `{"type": "p95_latency"}` when the observed 95th
  percentile latency over the rolling window exceeds `p95_target_ms`.
* **budget overrun** – emits `{"type": "budget_over"}` when `record_budget_over`
  is called.

Alerts are delivered to a callback (defaults to storing events in memory) and
can be consumed by logging or other systems.

## Troubleshooting

* Ensure `opentelemetry-sdk` is installed.  The helpers fall back to a no‑op
  implementation if the package is missing.
* Spans missing?  Confirm `init_tracer()` was called before emitting spans.

