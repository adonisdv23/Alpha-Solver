# Execution results

## Safe local dry-run wrapper

Command: embedded Python invocation of `run_local_dry_run_wrapper(...)` using `candidate-task.json` and `approval_record=None`.

Exit code: `0`

Observed summary:

```json
{"allowed": false, "artifact_paths": {"dry_run_result": "dry-run-result.json", "execution_gate_result": "execution-gate-result.json", "stop_state": "stop-state.json"}, "dry_run_status": "blocked_by_missing_approval", "reason_code": "missing_approval"}
```

Generated artifacts:

- `artifacts/execution-gate-result.json`
- `artifacts/dry-run-result.json`
- `artifacts/stop-state.json`

Interpretation: preflight/gate/dry-run wrapper and stop-state handling were exercised, but the flow stopped before approved execution because no real operator approval was available.

## Result import

Command:

```bash
python scripts/import_self_operator_acceptance_results.py --packet-dir docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-operator-supervised-local-acceptance-execution --output-dir docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-execution-evidence-002/artifacts --output-name result-import-summary.json
```

Exit code: `0`

Observed stdout:

```text
Self Operator acceptance import: status=import_ready_with_expected_blocks; tasks=10; artifacts=23; output=docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-execution-evidence-002/artifacts/result-import-summary.json
Evidence boundary: results are not interpreted; MVP readiness is not claimed.
```

Interpretation: result import was exercised against an existing local acceptance packet, read-only, with output written only under this packet.

## Acceptance interpretation

Command:

```bash
python scripts/interpret_self_operator_acceptance.py --import-summary docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-execution-evidence-002/artifacts/result-import-summary.json --output docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-execution-evidence-002/artifacts/acceptance-interpretation.json
```

Exit code: `1`

Observed stdout:

```text
interpretation=blocked tasks=10 defects=2 p0=0 p1=2 operator_decision=not_provided confirmation_type=none machine_readable_artifact_confirmation=false non_claim='does not claim MVP readiness'
```

Interpretation: acceptance interpretation was exercised and correctly blocked because no operator-decision artifact was provided. This is not an agent error; it is the expected evidence-boundary stop condition for this lane.

## Validation checks

Validation results are recorded after final checker execution in the final response. The required static checkers were run locally/offline and made no provider/model/token/API calls.

## Required static checker results

| Command | Exit code | Observed result |
| --- | ---: | --- |
| `python scripts/check_local_llm_doc_paths.py` | 0 | `Local LLM/post-Level doc path/link check passed (1475 files scanned).` |
| `python scripts/check_local_llm_evidence_boundaries.py` | 0 | `Local LLM evidence-boundary static check passed (1876 files scanned).` |
| `python scripts/check_local_llm_packet_consistency.py` | 0 | `Local LLM packet consistency check passed (146 packet directories scanned).` |
