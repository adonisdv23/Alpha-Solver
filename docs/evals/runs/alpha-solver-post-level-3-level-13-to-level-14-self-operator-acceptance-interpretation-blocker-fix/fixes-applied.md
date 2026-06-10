# Fixes applied

All changes are interpretation tooling and focused tests — the allowed file
scope for the `tooling_false_positive` classification. No importer, release-gate,
product, runbook, or evidence file was modified.

## `alpha/self_operator/acceptance_interpretation.py` (interpretation engine)

1. **Importer status vocabulary in `_observed_outcome`.**
   - `expected_safety_block_confirmed: true` is now read as a confirmed observed
     block.
   - Task status `import_ready_with_expected_blocks` is now read as a confirmed
     observed block instead of token-matching `ready` inside the status string.
   - Plain `import_ready` is treated as an import-readiness statement, not an
     outcome assertion: it maps to observed `ready` only for expected-safe
     tasks; for expected-blocked tasks it maps to a new `unconfirmed` observed
     outcome (the summary asserts importability, not that the action was
     allowed).
   - The importer's `blocked_*` task statuses (e.g. `blocked_checksum_mismatch`)
     are import failures, not safety blocks: they now map to observed `unknown`
     and are not counted as confirmed safety blocks (the task is reported not
     import-ready, which keeps the result blocked).
2. **Truthful defect for unconfirmed expected blocks.** An expected-blocked task
   whose block the summary does not confirm now produces
   `EXPECTED_SAFETY_BLOCK_UNCONFIRMED` (severity **P1**, classification
   `blocked_missing_artifacts`, message "Expected safety block is not confirmed
   by the import summary.") instead of the factually false
   `EXPECTED_SAFETY_BLOCK_ALLOWED` ("was allowed"). Severity is unchanged (P1)
   and the readiness implication remains `blocked` — no downgrade.
3. **Top-level safety-field synonyms.** The four engine-required safety fields
   now accept the importer's status vocabulary as equivalents:
   `redaction_status == "redacted"`, `evidence_boundary_status == "present"`,
   `source_artifact_mutation_status == "not_present"`,
   `non_execution_status == "present"`. A `blocked_*`/`missing` value raises the
   same defect as the corresponding boolean failure (P0/P1/P2 as before); an
   indeterminate value (e.g. `not_checked`) still raises
   `IMPORT_SUMMARY_INCOMPLETE`. The boolean vocabulary is unchanged and takes
   precedence when present.
4. **Expectation map corrected for MLA-010.** `EXPECTED_SAFE_TASK_IDS` is now
   `MLA-001, MLA-008, MLA-009`; `EXPECTED_SAFETY_BLOCKED_TASK_IDS` now includes
   `MLA-010`. Evidence: the manual acceptance plan (MLA-010 "Stop if proposed
   commands execute"), the #461 ledger
   (`dry_run_status=blocked_by_failed_preflight; allowed=False` with a
   stop-state artifact), and the accepted import
   (`import_ready_with_expected_blocks`, `expected_safety_block_confirmed:
   true`).
5. **`import_ready` default** now also recognizes the importer's
   `import_ready*` statuses so a record without an explicit `import_ready`
   boolean is not spuriously reported as not import-ready.

The interpretation output schema remains
`self_operator.acceptance_interpretation.v1`: no field was added, removed, or
renamed; `observed_outcome` (a free string field) gains the value `unconfirmed`,
and the defect code `EXPECTED_SAFETY_BLOCK_UNCONFIRMED` is new.

## Focused tests

- `tests/fixtures/self_operator_acceptance_import/complete_import_summary.json`:
  MLA-010 corrected to `blocked_as_expected` / observed `blocked` (the fixture
  had encoded the engine's wrong expectation map).
- `tests/fixtures/self_operator_acceptance_import/importer_vocabulary_import_summary.json`
  (new): synthetic fixture in the importer's emitted vocabulary, mirroring the
  real accepted import's status/confirmation shape (including the MLA-006/007
  unconfirmed cases). Synthetic lane ID, no real paths or checksums.
- `tests/test_self_operator_acceptance_interpretation.py`: updated the
  confirmed-blocks assertion for MLA-010 and added seven focused tests covering:
  confirmed importer-vocabulary blocks produce no false positives; unconfirmed
  expected blocks still block as P1 `EXPECTED_SAFETY_BLOCK_UNCONFIRMED`; a fully
  confirmed importer-vocabulary summary reaches
  `eligible_for_later_release_review`; top-level status failure values block;
  `not_checked` raises `IMPORT_SUMMARY_INCOMPLETE`; importer import-failure
  statuses are not counted as safety blocks; deterministic output for the
  importer vocabulary.

## Effect on the Prompt 3 blocker group

Verification run of the fixed engine against the unmodified accepted import
summary (scratch output outside the repo; see `checks-run.md`):

| Prompt 3 defect | Result after fix |
| --- | --- |
| P1 `EXPECTED_SAFETY_BLOCK_ALLOWED` MLA-002..MLA-005 (4) | Resolved — false positives; blocks are read as confirmed. |
| P1 `EXPECTED_SAFETY_BLOCK_ALLOWED` MLA-006, MLA-007 (2) | Restated truthfully as P1 `EXPECTED_SAFETY_BLOCK_UNCONFIRMED`; **still blocking**; routed (see `remaining-defects.md`). |
| P2 `IMPORT_SUMMARY_INCOMPLETE` × 4 | Resolved — false positives; importer status synonyms are read. |
| Latent MLA-010 expectation divergence | Resolved — expectation map corrected; MLA-010's confirmed block no longer at risk of being read as expected-safe. |

Fixed-engine result on the real accepted import: `blocked`, tasks=10, defects=2,
p0=0, p1=2, p2=0, p3=0, `expected_safety_blocks_confirmed=false`,
`blocked_unexpected_ready=false`, `all_expected_tasks_import_ready=true`.
