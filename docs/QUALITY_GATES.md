# Quality Gates

This project includes a lightweight evaluation harness and quality gate
configuration. The harness can score a dataset using simple metrics and output a
report which is checked against thresholds defined in `config/quality_gate.yaml`.

```
python -m alpha.cli.main eval run --dataset datasets/mvp_golden.jsonl --scorers em,f1
python -m alpha.cli.main gate check --report artifacts/eval/latest_report.json
```

Budgets such as accuracy, latency and cost can be inspected via:

```
python -m alpha.cli.main budgets show
```
