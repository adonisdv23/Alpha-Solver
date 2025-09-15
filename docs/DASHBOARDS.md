# Dashboards & Admin (EPIC_DASH_001)

The Alpha Production Observability dashboard ships a curated slice of the core runtime metrics: gate decisions, replay outcomes, budget burn, adapter performance, and a composite reliability SLO. Use this document as the handoff for ops and release partners when rolling the dashboard into shared Grafana instances.

## Importing the JSON into Grafana

1. Download `alpha/dashboard/panels.json` and `alpha/dashboard/alerts.json` from the repository.
2. In Grafana, open **Dashboards → New → Import** and upload `panels.json`. Grafana will create a new dashboard using the saved layout and queries.
3. Navigate to **Alerting → Alert rules → New alert rule → Import** (Grafana 9+) and paste the contents of `alerts.json` to register the alert definitions.
4. Point both the dashboard panels and the alert rules at your Prometheus data source. The JSON expects a Prometheus data source named `Prometheus`; adjust the datasource if your environment uses a different name.
5. Save the imported resources and share the links with the on-call rotation. First load should complete in under two seconds with a warm Prometheus cache.

## Panel Catalog

| Panel | PromQL | Screenshot Placeholder |
| --- | --- | --- |
| Gate Decisions (5m rate) | `sum by (decision) (rate(gate_decisions_total{environment="prod"}[5m]))` | ![Gate Decisions Panel Placeholder](images/gate_decisions_panel.png) |
| Replay Pass Throughput | `sum(rate(replay_pass_total{environment="prod"}[5m]))` | ![Replay Pass Panel Placeholder](images/replay_pass_panel.png) |
| Budget Spend (¢ per hour) | `sum(increase(budget_spend_cents{environment="prod"}[1h]))` | ![Budget Spend Panel Placeholder](images/budget_spend_panel.png) |
| Adapter Latency P95 | `quantile_over_time(0.95, adapter_latency_ms{environment="prod"}[5m])` | ![Adapter Latency Panel Placeholder](images/adapter_latency_panel.png) |
| Reliability SLO | `(1 - ((sum(rate(retries_total{environment="prod"}[30m])) + sum(rate(breaker_open_total{environment="prod"}[30m]))) / sum(rate(requests_total{environment="prod"}[30m])))) * 100` | ![Reliability SLO Panel Placeholder](images/reliability_slo_panel.png) |

> _Replace the placeholder images above after the first dashboard render in your environment._

## Alert Coverage

The companion alert rules mirror the dashboard metrics and add high-signal reliability guardrails. Each rule is delivered in `alpha/dashboard/alerts.json` under the `dashboards_alerts_v1` template so it can be imported directly into Grafana alerting.

### Core Dashboard Alerts

- **Gate Decision Denial Spike** – Watches the ratio of `gate_decisions_total` with `decision="denied"` exceeding 20% for five minutes.
- **Adapter Latency Regression** – Triggers when `quantile_over_time(0.95, adapter_latency_ms[5m])` rises above 750 ms for ten minutes.
- **Reliability SLO Burn** – Guards the SLO using retry and breaker counters to ensure the 99.5% target is met across a 30-minute window.

### Reliability Guardrail Alerts

- **Retry Saturation P95 High** – Uses `sum(max_over_time(retry_p95[10m]))` to detect when the 95th percentile retry count stays at or above two attempts for 15 minutes. Sustained high retries suggest downstream pressure or configuration drift.
- **Breaker Open Duration P95 High** – Tracks `sum(max_over_time(breaker_open_p95_ms[10m]))` and pages when the circuit breaker open duration P95 stays at or above 100 ms for 15 minutes, highlighting availability risk.
- **HTTP 5xx Ratio High** – Averages `http_5xx_ratio` via `sum(avg_over_time(http_5xx_ratio[5m]))` and fires when responses stay above the 1% error budget threshold for 10 minutes, signalling service regressions.

## Obs-card Snippet

Copy/paste the following one-liner into PRs, incidents, or release notes to provide quick context:

```
> obs-card alpha-dashboards gate=ok replay=ok budget=steady adapter_p95=<-ms slo=99.9%
```

Update the tokens (`ok`, `steady`, `99.9%`, etc.) with the latest readings before posting.
