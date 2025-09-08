# Observability

## JSONL Search
```bash
jq -r 'select(.event=="run_summary")' telemetry/telemetry.jsonl
```

## Replay Harness
```bash
alpha-solver replay --session SESSION_ID
```

## Benchmark
```bash
alpha-solver bench --quick
head bench_out/bench.csv
```

## Accessibility CLI
```bash
alpha-solver a11y-check --input artifacts/replays/SESSION_ID.jsonl
cat artifacts/a11y/summary.json
```

## Governance Flags
```bash
alpha-solver run --queries demo --budget-max-steps 5 --budget-max-seconds 1 --breaker-max-fails 2
```

## Leaderboard & Overview
```bash
python scripts/telemetry_leaderboard.py --paths telemetry/*.jsonl --format all
python scripts/overview_md.py
```

The overview report lists run metadata and per-query top-k tables. If telemetry
leaderboards were generated, links appear at the end.
