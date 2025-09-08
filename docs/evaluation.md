# Evaluation Harness

The evaluation harness runs deterministic checks over small datasets.

## Datasets

Datasets are newline-delimited JSON (`.jsonl`) files with fields:
`id`, `prompt`, `expected`, and optional `meta`.

A sample dataset lives at `datasets/mvp_golden.jsonl`.

## Scorers

Available scorers:

* `em` – exact string match.
* `f1` – token level F1.
* `regex` – passes when output matches `meta.regex`.
* `num` – numeric close with tolerances.

## Running

```bash
python -m alpha.cli.main eval run --dataset datasets/mvp_golden.jsonl --scorers em,f1 --seed 1337
```

Reports are written to `artifacts/eval/latest_report.json` and include
metrics, latency percentiles and cost per call. Use a fixed seed to keep
results deterministic.
