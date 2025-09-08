# Quality Gates

This repository includes a minimal evaluation harness and quality gate.

1. **Evaluation Harness** – run evaluations over a golden dataset with
   simple exact match and F1 scorers.
2. **Quality Gate** – verify that metrics, latency and cost satisfy
   thresholds defined in `config/quality_gate.yaml`.
3. **Budgets** – show configured budget controls from
   `config/budget_controls.yaml`.

Example workflow:

```
python -m alpha.cli.main eval run --dataset datasets/mvp_golden.jsonl --scorers em,f1
python -m alpha.cli.main gate check --report artifacts/eval/latest_report.json
python -m alpha.cli.main budgets show
```
