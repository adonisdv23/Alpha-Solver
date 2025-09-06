# Run Guide

## Quick start
```bash
python -m alpha.cli run --queries "find calendar tools" --regions US --plan-only --seed 1234
python -m alpha.cli run --queries-file docs/queries.sample.txt --regions US EU --explain
```

## CLI usage
```bash
python -m alpha.cli --examples           # show sample commands
python -m alpha.cli run --queries "demo" --regions US
python -m alpha.cli sweep --queries-file docs/queries.sample.txt --regions US EU
python -m alpha.cli telemetry --paths telemetry/*.jsonl --topk 5 --format md
python -m alpha.cli quick-audit          # repository audit
```

## Queries file format
- Lines starting with `#` are comments
- Blank lines ignored
- `@file path/to/other.txt` includes content (recursive, cycle-safe)

## Modes
- `--plan-only`: emit `artifacts/last_plan.json`
- `--explain`: plan + explanations, no execution
- `--execute`: default

## Troubleshooting
- `error: No queries provided.` → pass `--queries` or `--queries-file`
- `error: unknown command` → run `python -m alpha.cli --help`
