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
python -m alpha.cli replay --session SESSION_ID
python -m alpha.cli bench --quick
python -m alpha.cli a11y-check --input artifacts/replays/SESSION_ID.jsonl
```

Governance limits:

```bash
alpha-solver run --queries demo --budget-max-steps 5 --budget-max-seconds 2 --breaker-max-fails 1
```

## MVP Quality Gates

```bash
alpha eval run --dataset datasets/mvp_golden.jsonl --scorers em,f1 --seed 1337
alpha gate check --report artifacts/eval/latest_report.json
```

See [docs/evaluation.md](docs/evaluation.md) and
[docs/quality-gates.md](docs/quality-gates.md) for details.


## Local executors

See [docs/EXECUTORS.md](docs/EXECUTORS.md) for built-in math and CSV executors.

The sandbox executor can run tiny subprocesses with resource limits:

```bash
python - <<'PY'
from alpha.executors.sandbox import run_subprocess
print(run_subprocess(["echo", "hi"], timeout_s=1))
PY
```

## API Service

An experimental FastAPI wrapper is available for running the solver as a web
service. Start the stack (API + telemetry + monitoring) with:

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

See [docs/api.md](docs/api.md) for usage details.

```bash
python -m alpha.executors.math_exec "2+2"
```

## Using Tree-of-Thought

### Observability & Replay

`alpha-solver-v91-python.py` exposes optional observability flags:

```bash
python alpha-solver-v91-python.py "demo" --record mysession
python alpha-solver-v91-python.py "demo" --replay mysession --strict-accessibility
```

Logs can be redirected with `--log-path` and telemetry sent via `--telemetry-endpoint`.

```python
from alpha_solver_entry import _tree_of_thought
result = _tree_of_thought("solve x")
print(result["final_answer"], result["confidence"])
```

Note: `_tree_of_thought` is imported from `alpha_solver_entry` (a small shim)
because the canonical file name is hyphenated for historical reasons.

`_tree_of_thought` is the stable public API. Advanced users may import
`AlphaSolver` from `alpha_solver_entry`, which wraps the P3 observability
implementation in `alpha.solver.observability`.

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
    multi_branch: bool = False,
    max_width: int = 3,
    max_nodes: int = 100,
    enable_progressive_router: bool = False,
    router_min_progress: float = 0.3,
    enable_agents_v12: bool = False,
    agents_v12_order: tuple[str, ...] = ("decomposer", "checker", "calculator"),
    scorer: str = "composite",
    scorer_weights: dict[str, float] | None = None,
    enable_cache: bool = True,
    cache_path: str | None = None,
) -> dict
```

Configuration highlights:

| key | default | description |
|---|---|---|
| `scorer` | `"composite"` | Path scoring strategy (`lexical`, `constraint`, `composite`). |
| `scorer_weights` | `{\"lexical\": 0.6, \"constraint\": 0.4}` | Weights for composite scorer. |
| `enable_cache` | `True` | Enable persistent ToT cache. |
| `cache_path` | `artifacts/cache/tot_cache.json` | Location for cache file. |

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

### `alpha_solver_cli.py`

A thin wrapper around `_tree_of_thought` exposes router and SAFE-OUT flags:

```bash
python alpha_solver_cli.py "demo" --multi-branch --max-width 2 --max-nodes 4 \
    --enable-progressive-router --router-escalation basic,structured,constrained \
    --low-conf-threshold 0.5 --no-cot-fallback
```

### Multi-Branch ToT & Progressive Router

```python
from alpha_solver_entry import _tree_of_thought


def demo_router() -> None:
    """Run a deterministic progressive-router example."""
    env = _tree_of_thought(
        "color puzzle",
        seed=42,
        multi_branch=True,
        max_width=2,
        max_nodes=4,
        enable_progressive_router=True,
        router_escalation=("basic", "structured", "constrained"),
        router_min_progress=0.8,
    )
    print(env["final_answer"])
    print(env["diagnostics"]["router"]["stage"])
    print(env["diagnostics"]["tot"]["explored_nodes"])


if __name__ == "__main__":
    demo_router()
```

Sample output:

```text
To proceed, clarify: color puzzle
structured
2
```

Determinism: beam expansion sorts candidates by score (rounded to 3 decimals) and lexical path.

| option | default | description |
| --- | --- | --- |
| `max_width` | `3` | Beam width for multi-branch search |
| `max_nodes` | `100` | Node expansion limit |
| `router_escalation` | `basic→structured→constrained` | Progressive stages |

### SAFE-OUT v1.1 (State Machine & Structured Recovery)

```python
from alpha_solver_entry import _tree_of_thought

result = _tree_of_thought("unclear query")
print(result["route"])
print(result["phases"])
print(result["notes"])
```

Example output:

```json
{
  "final_answer": "To proceed, clarify: unclear query …",
  "route": "cot_fallback",
  "confidence": 0.5,
  "reason": "low_confidence",
  "notes": "Confidence below 0.60; used chain-of-thought fallback. | phases: init->assess->fallback->finalize",
  "tot": {"confidence": 0.55, "reason": "ok", ...},
  "cot": {"confidence": 0.5, "steps": []},
  "phases": ["init", "assess", "fallback", "finalize"]
}
```

_tree_of_thought maintains backward compatibility: existing keys are unchanged; phases and enriched notes are additive.

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

## Agents v12: what’s enabled by the flag

Setting `enable_agents_v12=True` wires deterministic helper agents
(`decomposer`, `checker`, `calculator`) used for simple arithmetic reasoning.
The flag is off by default and enabling it only affects branch ordering and scoring.

## SAFE-OUT v1.2: richer reasons & evidence

SAFE-OUT now emits additional reason codes and an `evidence` list summarising
why a result was considered low confidence. Fallback routes include
`recovery_notes` describing any escalations.

## Config layering (defaults/env/CLI)

Configuration is now loaded via `alpha.config.loader.load_config`. Defaults are
stored centrally and can be overridden by environment variables (`ALPHA_*`) or
explicit keyword arguments.

## Telemetry schema v1 + Tiny Web Viz

Telemetry events carry a `schema_version` (`1.0.0`) and can be validated with
`alpha.reasoning.logging.validate_event`. The `viz/index.html` viewer renders
JSONL telemetry logs without external dependencies.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Release process

See [RELEASE.md](RELEASE.md). Release notes are generated with `make release-notes`.
