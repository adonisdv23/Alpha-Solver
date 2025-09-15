# Metrics Aggregator

`alpha.metrics.aggregator.get_metrics_text` builds a Prometheus exposition
string from a small set of counters and histograms.

```python
from alpha.metrics.aggregator import get_metrics_text

# Increment custom counter and fetch exposition text
text = get_metrics_text(extra={"throttles": 2})
```

The output contains `gate_decisions_total`, `replay_pass_total`,
`budget_spend_cents`, and `adapter_latency_ms` series along with any counters
specified via the optional `extra` argument.
