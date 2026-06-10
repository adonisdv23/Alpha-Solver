# Checks run

All commands ran from the repository root on branch `claude/stoic-euler-lgc5pl`
(based on `main` at `fe2ca99`).

## Required checks

### `git status --short`

```
 M alpha/self_operator/result_import.py
 M tests/test_self_operator_result_import.py
?? alpha/self_operator/import_blocker_triage.py
?? docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/
?? scripts/triage_self_operator_import_blocker.py
?? tests/test_self_operator_import_blocker_triage.py
```

All changed paths are inside the lane's allowed file list.

### `git diff --name-only`

```
alpha/self_operator/result_import.py
tests/test_self_operator_result_import.py
```

### `git diff --check`

No whitespace errors (exit 0).

### `python scripts/triage_self_operator_import_blocker.py --help`

Exit 0; usage printed.

## Triage run (real packet)

```
python scripts/triage_self_operator_import_blocker.py \
  --packet-dir docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-operator-supervised-local-acceptance-execution \
  --import-summary docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-local-acceptance-result-import-tooling/import-output/acceptance-import-summary.json \
  --output-dir docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import
```

Output: `classification=expected_synthetic_marker`; exit 0;
result written to `import-blocker-triage-result.json`.

## Tests

### `python -m pytest -q tests/test_self_operator_import_blocker_triage.py`

11 passed.

### `python -m pytest -q tests/test_self_operator_result_import.py`

19 passed (14 pre-existing, 5 added).

### Adjacent self-operator suites

`python -m pytest -q tests/test_self_operator_release_gate.py
tests/test_self_operator_acceptance_interpretation.py tests/test_self_operator_dry_run.py
tests/test_self_operator_command_classification.py` — 61 passed.

### Full suite comparison

`python -m pytest -q --continue-on-collection-errors` fails the identical set of 24
pre-existing tests on unmodified `main` and on this branch (missing optional
dependencies such as `fastapi`/`httpx`/`anyio`/`starlette`, plus sandbox subprocess
constraints). No regression from this change.

## Accepted import rerun (real packet)

```
python scripts/import_self_operator_acceptance_results.py \
  --packet-dir docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-operator-supervised-local-acceptance-execution \
  --output-dir docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import \
  --output-name accepted-import-summary.json
```

Output: `status=import_ready_with_expected_blocks; tasks=10; artifacts=23`; exit 0.

Baseline before the fix (same command, output to a temporary directory):
`status=blocked_source_mutation_concern`; exit 1; `evidence_boundary_status:
blocked_evidence_boundary_failure` also present as a latent secondary blocker.

## Packet consistency

```
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import
```

`Local LLM packet consistency check passed (1 packet directories scanned).` Exit 0.

## Source-packet integrity

Recomputed SHA-256 checksums for the three MLA-010 artifacts match the #461
`artifact-ledger.md` values; the read-only no-mutation property of triage and import is
also asserted by tests
(`test_triage_is_read_only_and_deterministic`,
`test_actual_461_packet_classifies_expected_synthetic_marker_without_mutation`,
`test_handles_actual_461_packet_if_present_without_mutating_it`).
