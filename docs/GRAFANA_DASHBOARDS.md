# Grafana Dashboards

These dashboards visualise key Alpha Solver metrics using Prometheus data.

## Available Dashboards

The repository includes three importable dashboards under
`observability/grafana/dashboards/`:

- **alpha_solver_overview.json** – latency percentiles, error rate,
  throughput, budget over events, tokens and cost totals.
- **alpha_gates.json** – gate trigger counts, policy redactions and
  gate latency.
- **alpha_adapters.json** – adapter success rate, latency and circuit
  breaker state.

Each dashboard uses the `$__rate_interval` variable and supports an
optional `$tenant` template to filter series when tenant labels are
present.

## Importing

1. Open Grafana and navigate to *Dashboards → Import*.
2. Upload one of the JSON files and select your Prometheus data source
   when prompted.
3. Repeat for the remaining dashboards. Placeholders:
   `![Overview](overview.png)` `![Gates](gates.png)` `![Adapters](adapters.png)`

## Prometheus Scrape Configuration

```yaml
scrape_configs:
  - job_name: alpha-solver
    metrics_path: /metrics
    static_configs:
      - targets: ['alpha-solver:8000']
```

## Example Alert Rules

```yaml
- alert: AlphaSolverLatencyP95
  expr: histogram_quantile(0.95,
          sum(rate(alpha_solver_latency_ms_bucket[5m])) by (le)) > 500
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: Alpha Solver p95 latency > 500ms

- alert: AlphaSolverErrorRate
  expr: (sum(rate(alpha_solver_errors_total[5m])) /
         sum(rate(alpha_solver_route_decision_total[5m]))) * 100 > 5
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: Alpha Solver error rate above 5%

- alert: AlphaSolverBudgetOver
  expr: sum(rate(alpha_solver_budget_verdict_total{verdict="over"}[5m])) > 0
  for: 1m
  labels:
    severity: info
  annotations:
    summary: Budget over events detected
```

These examples can be adapted to match your SLO targets and alerting
pipeline.
