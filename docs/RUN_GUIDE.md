# Run Guide

This guide shows how to set up the Alpha Solver in a few minutes and run it.

## Setup
1. Install Python 3.12.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Build the tools canon:
   ```bash
   python scripts/build_tools_canon.py
   ```

## Determinism
Use `--seed` to make runs reproducible. The CLI prints the effective seed and
records it in plan artifacts. If omitted, a seed is derived from the clock.

## Example Runs
```bash
# Plan only
python -m alpha.cli --plan-only --regions "US" --queries docs/queries.txt

# Explain mode
python -m alpha.cli --explain --regions "US" --queries docs/queries.txt

# Execute locally
python -m alpha.cli --execute --regions "US" --queries docs/queries.txt
```

Artifacts such as plans and traces are written under `artifacts/` by default or
under the directory provided via `--outdir`.

## Troubleshooting
- Missing queries file: ensure the path passed to `--queries` exists.
- Empty regions list: pass `--regions "US,EU"` or similar.
- To inspect determinism, run twice with the same `--seed` and compare plan
  outputs.
