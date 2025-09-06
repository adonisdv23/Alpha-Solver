# Run Guide

## Quick start

```bash
python -m alpha.cli run --queries "find calendar tools" --regions US --plan-only --seed 1234
python -m alpha.cli run --queries-file docs/queries.sample.txt --regions US EU --explain
```

## Queries file format

Lines starting with `#` are comments

Blank lines ignored

`@file path/to/other.txt` includes content (recursive, cycle-safe)

## Modes

- `--plan-only`: emit `artifacts/last_plan.json`
- `--explain`: plan + explanations, no execution
- `--execute`: default

