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

## Reasons & Confidence

Each shortlist item now includes:

- `confidence`: normalized 0-1 score relative to other items in the shortlist.
- `explain`: component scores (lexical, semantic, priors, recency, total).
- `reason`: plain text summary of the score parts.

## Optional region weights

Provide a JSON file mapping region codes to multipliers:

```bash
export ALPHA_REGION_WEIGHTS_PATH=registries/region_weights.sample.json
python scripts/preflight.py  # validates file if set
```

Weights (if any) are applied to scores before tie-breaks.

## Audit reminder

Keep shortlist snapshots under `artifacts/shortlists/` and run `make telemetry`
to collect usage logs for later review.
