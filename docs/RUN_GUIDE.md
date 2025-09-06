# Run Guide

## Quick Start

```bash
make test
make telemetry
make quick-audit
```

## Environment Variables

| Name | Description |
|------|-------------|
| `ALPHA_RECENCY` | Optional recency weight (e.g. `0.15`) |
| `ALPHA_REGION_WEIGHTS` | Path to region weights JSON |
| `ALPHA_POLICY_DRYRUN` | Set `1` to disable policy enforcement |
| `ALPHA_BUDGET` | Maximum allowed tool steps |
| `ALPHA_MAX_ERRORS` | Fail fast after this many errors |
| `ALPHA_TELEMETRY_SCRUB` | Scrub sensitive fields from telemetry |

## Short Sweep

```bash
python scripts/overnight_run.py --regions "US,EU" --k 5 --queries docs/queries.txt
```

Artifacts are written under `artifacts/` by default:

- `artifacts/leaderboard.md`
- `artifacts/shortlists/<region>/<query_hash>.json`

Set `ALPHA_ARTIFACTS_DIR` to override the output root.
