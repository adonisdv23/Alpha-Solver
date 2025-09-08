# Quality Gates

Quality gates enforce minimum accuracy and resource budgets.

Default thresholds are defined in `config/quality_gate.yaml`:

```yaml
min_accuracy: 0.85
max_p95_ms: 750
max_p99_ms: 1200
max_cost_per_call: 0.01
primary_metric: em
```

## Checking a Report

```bash
alpha gate check --report artifacts/eval/latest_report.json
```

Non-zero exit codes indicate the gate failed. Budgets can be inspected
with:

```bash
alpha budgets show
```

Environment variables (e.g. `QUALITY_GATE_MIN_ACCURACY`) or CLI overrides
can tune the thresholds.
