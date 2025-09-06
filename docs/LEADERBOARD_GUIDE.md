# Leaderboard Guide

Telemetry JSONL files begin with a `run_header` line containing a `run_id`,
regions list, and metadata. Subsequent lines record selections with a
`query_hash` that uniquely identifies the query text.

## Running

Generate a Markdown leaderboard from accumulated telemetry with:

```bash
make telemetry
```

## Interpreting Metrics

- **Diversity** – variety of distinct tools selected.
- **Tie-rate** – frequency of equal scores across tools.
- **Stability** – consistency of top tools across runs.

## Snapshots

Shortlist snapshots are written under `artifacts/shortlists/`. Keep these
under version control to diff between runs:

```bash
git diff -- artifacts/shortlists
```
