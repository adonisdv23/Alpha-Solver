# Alpha Solver

Alpha Solver is a lightweight planning and execution engine for tool selection.

## Install & Run

```bash
pip install -e .
alpha-solver run --queries "demo" --plan-only
```

## CLI & Quick Start
See [docs/RUN_GUIDE.md](docs/RUN_GUIDE.md) for more examples and details.

```bash
python -m alpha.cli run --queries "demo query" --regions US --plan-only --seed 1234
python -m alpha.cli run --queries-file docs/queries.sample.txt --regions US EU --explain
python -m alpha.cli --examples  # show sample commands
```


## Local executors

See [docs/EXECUTORS.md](docs/EXECUTORS.md) for built-in math and CSV executors.

The sandbox executor can run tiny subprocesses with resource limits:

```bash
python - <<'PY'
from alpha.executors.sandbox import run_subprocess
print(run_subprocess(["echo", "hi"], timeout_s=1))
PY
```

```bash
python -m alpha.executors.math_exec "2+2"
```

## Using Tree-of-Thought

```python
from alpha_solver_entry import _tree_of_thought
result = _tree_of_thought("solve x")
print(result["final_answer"], result["confidence"])
```

Note: `_tree_of_thought` is imported from `alpha_solver_entry` (a small shim)
because the canonical file name is hyphenated for historical reasons.

```python
_tree_of_thought(
    query: str,
    *,
    seed: int = 42,
    branching_factor: int = 3,
    score_threshold: float = 0.70,
    max_depth: int = 5,
    timeout_s: int = 10,
    dynamic_prune_margin: float = 0.15,
    low_conf_threshold: float = 0.60,        # SAFE-OUT policy
    enable_cot_fallback: bool = True,        # SAFE-OUT policy
) -> dict
```

### Safety: Low-Confidence Fallback (SAFE-OUT)

Tree-of-Thought exposes two thresholds:

- `score_threshold` – accept a path inside the solver (default `0.70`); if no path ≥ threshold, ToT returns best-so-far with reason `"below_threshold"`.
- `low_conf_threshold` – trigger SAFE-OUT policy (default `0.60`); if final confidence < this, the policy routes to `cot_fallback` (when enabled) or `best_effort`.

Returned policy output schema:

```python
{
  "final_answer": "...",
  "route": "tot" | "cot_fallback" | "best_effort",
  "confidence": 0.0,
  "reason": "ok" | "low_confidence" | "timeout" | "below_threshold",
  "notes": "...",
  "tot": { "answer": "...", "confidence": 0.0, "path": [], "explored_nodes": 0, "config": {...}, "reason": "ok|timeout|below_threshold" },
  "cot": { "answer": "...", "confidence": 0.0, "steps": [] }  # present only if fallback executed
}
```

Usage:

```python
from alpha_solver_entry import _tree_of_thought

result = _tree_of_thought(
    "vague query",
    score_threshold=0.70,
    low_conf_threshold=0.60,
)
print(result["route"], result["final_answer"])
```

### ToT Multi-Branch

Enable breadth-limited exploration:

```python
_tree_of_thought("q", multi_branch=True, max_width=3, max_nodes=200)
```

| Config | Default | Description |
| --- | --- | --- |
| `multi_branch` | `True` | Enable beam search |
| `max_width` | `3` | Nodes kept per layer |
| `max_nodes` | `200` | Total exploration cap |

### Progressive Router

Escalates prompt complexity when early progress is low. Profiles: `basic` → `structured` → `constrained`.

### Agents v12 (groundwork)

Flags for future multi-agent routing. Default implementations are deterministic no-ops.

### Benchmarks

Run deterministic benchmarks comparing CoT vs ToT variants:

```bash
python scripts/bench_reasoners.py
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

## Observability & Nightly

- `make telemetry` – generate leaderboards and overview
- `make replay` – replay the last plan deterministically
- `make bench` – benchmark sample queries

See [docs/OBSERVABILITY.md](docs/OBSERVABILITY.md) for details.

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

## Preflight

Validate the registry and basic settings:

```bash
make preflight
# or
python scripts/preflight.py --fix-ids
```

## Determinism switch

Set `ALPHA_DETERMINISM=1` to lock a global seed and a single UTC
timestamp in session traces for reproducible runs.

## Governance (MVP)

The lightweight policy engine enforces step/time budgets and a simple
circuit breaker, with optional data classification.  Decisions are logged to
`artifacts/policy_audit.jsonl`.

CLI flags:

```bash
--policy-dry-run
--budget-max-steps INT
--budget-max-seconds FLOAT
--breaker-max-fails INT
--data-policy PATH
```

See [docs/POLICY.md](docs/POLICY.md) for details.

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Release process

See [RELEASE.md](RELEASE.md). Release notes are generated with `make release-notes`.
