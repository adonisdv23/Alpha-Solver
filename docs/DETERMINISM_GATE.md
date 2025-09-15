# Determinism Gate

The determinism gate runs a small replay set multiple times and fails if any
run diverges.  It helps catch non-deterministic behaviour before merge.

## Usage

```bash
python -m service.replay.gate --runs 10 --replay-file data/datasets/replay/replay_small.jsonl
```

Options:

- `--runs N` – number of repeated runs (default `10`).
- `--seed S` – seed for pseudo random noise (default `123`).
- `--replay-file PATH` – JSONL replay set.
- `--skip-tags TAGS` – comma separated list of tags to skip
  (`known_flaky,external_tool_missing` by default).
- `--timeout-ms` – abort after this many milliseconds (default `60000`).
- `--fast` – shortcut for local iteration; limits runs to two.

## Output

The gate prints a summary line and either `PASS` or `FAIL` with a minimal diff
showing changed fields.  Records marked with any skip tag are ignored and the
count is reported.

Example pass:

```
determinism_gate: runs=10 seed=123 set=data/datasets/replay/replay_small.jsonl
determinism_gate: PASS (10/10 stable)
```

Example failure:

```
determinism_gate: runs=10 seed=123 set=data/datasets/replay/replay_small.jsonl
determinism_gate: FAIL after run 3 — diffs: winner: 1.000000->1.123000 (Δ=+0.123000)
```

## Known Skips

Records may include a `tags` field with labels such as `known_flaky`.  Passing
`--skip-tags` with those labels causes the gate to ignore them and continue.
The log reports how many records were skipped.

## CI

The gate is integrated into CI and should complete within ~90 seconds.  On
failure the log is uploaded as an artifact for inspection.
