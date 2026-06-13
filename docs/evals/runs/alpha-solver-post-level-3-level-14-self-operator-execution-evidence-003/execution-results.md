# Execution results

## Safe local dry-run wrapper with supplied approval artifact

Command: embedded Python invocation of `run_local_dry_run_wrapper(...)` using `candidate-task.json` and `operator-approval-artifact.json`.

Exit code: `0`

Observed summary:

```json
{"allowed": false, "artifact_paths": {"dry_run_result": "dry-run-result.json", "execution_gate_result": "execution-gate-result.json", "stop_state": "stop-state.json"}, "dry_run_status": "blocked_by_missing_approval", "reason_code": "approval_invalid"}
```

Generated artifacts:

- `artifacts/execution-gate-result.json`
- `artifacts/dry-run-result.json`
- `artifacts/stop-state.json`

Interpretation: the real approval artifact was ingested, but the local gate did not accept it because the exact hard-stop phrase required by the validator was not present with the required lowercase spelling. The gate failed closed and no approved post-gate execution action occurred.

## Result import

Command:

```bash
python scripts/import_self_operator_acceptance_results.py --packet-dir docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-operator-supervised-local-acceptance-execution --output-dir docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-execution-evidence-003/artifacts --output-name result-import-summary.json
```

Exit code: `0`

Observed stdout:

```text
Self Operator acceptance import: status=import_ready_with_expected_blocks; tasks=10; artifacts=23; output=docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-execution-evidence-003/artifacts/result-import-summary.json
Evidence boundary: results are not interpreted; MVP readiness is not claimed.
```

Interpretation: result import was exercised against an existing local acceptance packet, read-only, with output written only under this packet.

## Acceptance interpretation

Command:

```bash
python scripts/interpret_self_operator_acceptance.py --import-summary docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-execution-evidence-003/artifacts/result-import-summary.json --operator-decision docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-execution-evidence-003/operator-approval-artifact.json --output docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-execution-evidence-003/artifacts/acceptance-interpretation.json
```

Exit code: `1`

Observed stdout:

```text
interpretation=blocked tasks=10 defects=3 p0=0 p1=2 operator_decision=invalid confirmation_type=none machine_readable_artifact_confirmation=false non_claim='does not claim MVP readiness'
```

Observed stderr:

```text
blocked: operator decision not consumed: schema must be self_operator.expected_safety_block_operator_review.v1, got None; lane_id must be ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-TO-LEVEL-14-SELF-OPERATOR-EXPECTED-SAFETY-BLOCK-OPERATOR-REVIEW-001, got 'ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-EXECUTION-EVIDENCE-003'; operator_decision must be ACCEPT_LEDGER_LEVEL_CONFIRMATION, got None; accepted_tasks must be exactly ['MLA-006', 'MLA-007'], got None; confirmation_type must be operator_ledger_level_acceptance, got None; machine_readable_artifact_confirmation must be false: operator ledger-level acceptance is not machine-readable artifact confirmation; source_artifacts_mutated must be false; readiness_claimed must be false
```

Interpretation: acceptance interpretation was exercised locally and correctly remained blocked. The supplied approval artifact is not the separate expected-safety-block operator-review artifact.

## Verdict and DEF-001 status

Verdict: `APPROVAL_CAPTURED_EXECUTION_BLOCKED_BY_LOCAL_SAFETY_GATE`

DEF-001 status: `DEF-001_FURTHER_PARTIALLY_RETIRED`
