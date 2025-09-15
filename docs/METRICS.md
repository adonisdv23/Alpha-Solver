# Metrics Aggregation

`MetricsAggregator` centralizes collection of key series and exposes a Prometheus
endpoint at `/metrics`.

## Series

- `alpha_solver_gate_total{gate="..."}` – gate decisions
- `alpha_solver_replay_total{result="..."}` – replay outcomes
- `alpha_solver_budget_total{verdict="..."}` – budget verdicts
- `alpha_solver_adapter_calls_total{adapter="..."}` – adapter invocations
- `alpha_solver_adapter_latency_ms_bucket{adapter="...",le="..."}` – adapter latency histogram

## Usage

```python
from alpha.metrics.aggregator import MetricsAggregator

agg = MetricsAggregator()
agg.record_gate("low_confidence")
app = agg.asgi_app()  # expose /metrics
```

Scrape with Prometheus:

```bash
curl http://localhost:8000/metrics
```

The exporter is lightweight; scraping p95 is under 100ms in tests.
