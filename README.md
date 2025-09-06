# Alpha Solver

Alpha Solver is a lightweight planning and execution engine for tool selection.

## Quick Start
See [docs/RUN_GUIDE.md](docs/RUN_GUIDE.md) for setup instructions and example
commands to run the CLI. For development guidelines see
[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

## Local executors

See [docs/EXECUTORS.md](docs/EXECUTORS.md) for built-in math and CSV executors.

```bash
python -m alpha.executors.math_exec "2+2"
```

## Telemetry Leaderboard (offline, stdlib-only)

Generate a Markdown leaderboard from telemetry JSONL files:

```bash
python scripts/telemetry_leaderboard.py --paths telemetry/*.jsonl --topk 5 --format md --out artifacts/leaderboard.md
```

To produce CSV output instead:

```bash
python scripts/telemetry_leaderboard.py --paths telemetry/*.jsonl --topk 5 --format csv --out artifacts/leaderboard.csv
```

## Artifacts & Repro

See [docs/ARTIFACTS.md](docs/ARTIFACTS.md) for details on artifact schema
versioning and run snapshots.

```bash
python scripts/env_snapshot.py
python scripts/bundle_artifacts.py
```

## Plan Spine & Transparency

The runner can emit a minimal *plan spine* showing how a query will be solved.

```bash
python -m alpha.core.runner --plan-only --query "Test"
python -m alpha.core.runner --explain --query "Test"
```

`--plan-only` writes `artifacts/last_plan.json` without executing any steps.
`--explain` adds human readable summaries; omit both flags (or use `--execute`)
to run the plan and emit the same artifact with results.

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

## Governance v1

```bash
export ALPHA_BUDGET_STEPS=100
export ALPHA_MAX_ERRORS=5
# optional dry-run mode
export ALPHA_POLICY_DRYRUN=1
```

See [docs/GOVERNANCE.md](docs/GOVERNANCE.md) for full details.

## Audit reminder

Keep shortlist snapshots under `artifacts/shortlists/` and run `make telemetry`
to collect usage logs for later review.

## Further Reading

- [Leaderboard Guide](docs/LEADERBOARD_GUIDE.md)
- [Adding Tools](docs/ADDING_TOOLS.md)

## Telemetry Scrubbing

```bash
export ALPHA_TELEMETRY_SCRUB=1
# optional override
export ALPHA_TELEMETRY_SCRUB_FIELDS="query_text,raw_prompt"
```

## Formatting & Linting

We lint the **core library** with `ruff` (scoped to `alpha/`) in CI and pre-commit:
`ruff check alpha` (CI) and `ruff check --fix alpha` locally.
We lint the core library with Ruff. Black is temporarily **not** enforced in CI to avoid a noisy repo-wide rewrite; a one-time format PR will re-enable `black --check`. You can still run Black locally.

The `scripts/` and `tests/` trees are covered by `black` only to keep CI fast and noise-free.

CLI: `quick-audit` now invokes the audit script via `python -m scripts.quick_audit`, so it works both from the repo and when installed.
Use the make targets below to keep style consistent.

```bash
make fmt       # format with black
make fmt-check # check formatting
make lint      # run ruff check
```

Optional: install pre-commit hooks locally:

```bash
pip install pre-commit && pre-commit install
```
