# Determinism CLI

The determinism harness replays recorded routing decisions multiple times and
reports whether the outputs remain stable.  It is intended for quick
verification in CI and for local experiments.

## Usage

```bash
python -m cli.determinism \
  --replay-file data/datasets/replay/replay_small.jsonl \
  --runs 10 \
  --seed 123 \
  --out-json artifacts/determinism_report.json \
  --out artifacts/determinism_report.txt
```

* `--replay-file` – path to a JSONL file with records to replay.
* `--runs` – number of times each record is executed (default `10`).
* `--seed` – random seed passed to each run (default `123`).
* `--skip-tags` – comma separated tags that, if present in `skip_reason`, will
  cause the record to be ignored.
* `--out-json`/`--out` – optional paths for machine and human readable reports.
* `--fast` – reduce runs (max `3`) for local smoke tests.

Exit codes:

* `0` – all records stable.
* `4` – at least one record flapped.
* `2` – invalid arguments or missing replay file.
* `5` – unexpected internal error.

## Interpreting diffs

When a mismatch is detected the CLI prints the first record that flapped along
with a compact set of key changes.  Sensitive values are redacted before being
rendered.  JSON reports include full lists of mismatches for further analysis.

## CI integration

The CLI is lightweight and runs within a few seconds on the default replay set.
It can be wired into CI to guard against accidental introduction of
nondeterministic routing behaviour.  Store the generated reports as artifacts
for inspection when failures occur.
