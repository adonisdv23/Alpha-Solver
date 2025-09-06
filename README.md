# Alpha Solver

Alpha Solver is a lightweight planning and execution engine for tool selection.

## Quick Start
See [docs/RUN_GUIDE.md](docs/RUN_GUIDE.md) for setup instructions and example
commands to run the CLI.

## Telemetry Leaderboard (offline, stdlib-only)

Generate a Markdown leaderboard from telemetry JSONL files:

```bash
python scripts/telemetry_leaderboard.py --paths telemetry/*.jsonl --topk 5 --format md --out artifacts/leaderboard.md
```

To produce CSV output instead:

```bash
python scripts/telemetry_leaderboard.py --paths telemetry/*.jsonl --topk 5 --format csv --out artifacts/leaderboard.csv
```

## Recency priors (optional)

```markdown
optional recency signal via dated priors
export ALPHA_RECENCY_PRIORS_PATH=registries/priors/dated_priors.sample.json
export ALPHA_RECENCY_WEIGHT=0.15
export ALPHA_RECENCY_HALFLIFE_DAYS=90
python scripts/preflight.py # validates priors & registry IDs
```

## Shortlist snapshots

```vbnet
produced by runner / overnight sweep
artifacts/shortlists/<region>/<query_hash>.json

contains rank, tool_id, score, prior; useful for audits and diffs
```
