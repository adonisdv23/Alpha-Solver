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
