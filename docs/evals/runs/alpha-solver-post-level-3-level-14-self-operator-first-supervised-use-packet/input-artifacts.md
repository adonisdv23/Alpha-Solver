# Input artifacts

Exact inputs the first supervised use may read. Everything below is
consumed read-only; the run mutates none of it.

## Repository inputs (read-only)

| Input | Role |
| --- | --- |
| `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet/` | This packet: the charter the run executes against. |
| `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-post-closeout-operator-use-prep/` | The prep packet whose contract, scope, confirmation, redaction, stop-state, and preservation rules bind the run. |
| `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization/mvp-operator-runbook.md` | Canonical operator runbook. |
| Existing Self Operator packet directories under `docs/evals/runs/` (the `alpha-solver-post-level-3-*` and `alpha-solver-post-level-7-*` packets) | The subject of the consistency review; read only by the deterministic checker. |
| `scripts/check_local_llm_packet_consistency.py` | The deterministic read-only checker the target reviews and runs. |
| `scripts/check_self_operator_release_gate.py` | The deterministic read-only precondition checker. |
| `alpha/self_operator/` modules (`approval.py`, `preflight.py`, `execution_gate.py`, `dry_run.py`, `artifact_store.py`, `redaction.py`, `stop_state.py`) | The gate-and-record pipeline, invoked as a library, unmodified. |

## Operator-drafted inputs (created for the run, outside the repository)

| Input | Role |
| --- | --- |
| Approval record JSON (`self_operator.approval_record.v1`) | Drafted per `operator-confirmation-required.md`; kept below the output root, never committed raw. |
| Proposed task JSON | One docs-only task whose `proposed_commands` contain only the checker command text from `execution-command-plan.md`; kept below the output root, never committed raw. |

## Explicit input exclusions

No credentials, secrets, tokens, provider configuration, model
configuration, API endpoints, browser profiles, deployment manifests, or
billing data may appear in any input. If any such value is found in any
input, the run aborts before execution (`abort-conditions.md`).
