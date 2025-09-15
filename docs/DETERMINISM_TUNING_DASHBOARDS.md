# Determinism & Weight Tuning Dashboards

Two Grafana dashboards ship for replay stability and weight tuning.

## Exporting the tuning report

The tuning harness emits a JSON summary which can be normalised with
`report_export`:

```bash
python -m service.tuning.report_export --in artifacts/tuning_report.json --out artifacts/tuning_report.json
```

The file `artifacts/tuning_report.json` is consumed by the weight tuning
panels.

## Importing dashboards

1. Open Grafana → *Dashboards* → *Import*.
2. Upload `observability/grafana/dashboards/determinism.json` for replay
   stability metrics.
3. Upload `observability/grafana/dashboards/weights_tuning.json` for
   BEFORE→AFTER comparisons of accuracy, win rate and factor weights.

## Expected panels

- **Determinism**: Replay pass %, flap rate, runs by status, latency p50/p95,
  errors over time and a table of recent replay failures.
- **Weight Tuning**: BEFORE vs AFTER accuracy and win rate, factor weight bar
  chart and top per-factor deltas, with a link to the raw report.

These dashboards rely on Prometheus series such as
`alpha_solver_replay_runs_total` and JSON fields like
`before.accuracy` and `per_factor`.
