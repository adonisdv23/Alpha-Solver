# Observability

## Leaderboard & Overview
```bash
python scripts/telemetry_leaderboard.py --paths telemetry/*.jsonl --format all
python scripts/overview_md.py
```

## Replay a Plan or Shortlist
```bash
python scripts/replay.py --plan artifacts/last_plan.json
```

## Benchmark Queries
```bash
python scripts/bench.py --queries-file docs/queries.sample.txt --regions US --repeat 3
```

## Reading `overview.md`
The overview report lists run metadata and per-query top-k tables with:
- `tool_id`: ID of the tool
- `score`: raw score
- `confidence`: 0-1 normalized confidence
- `reason`: short explanation of the score
If telemetry leaderboards were generated, links appear at the end.
