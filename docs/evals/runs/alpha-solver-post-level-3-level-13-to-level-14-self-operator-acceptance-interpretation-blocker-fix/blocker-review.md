# Blocker review

## Input reviewed (read-only)

- Prompt 3 packet:
  `docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-interpretation-and-release-gate-apply/`
  (`interpretation-result.json`, `interpretation-result.md`, `defect-register.md`,
  `p0-p1-review.md`, `earliest-blocker.md`, `selected-next-lane.md`). Verified
  present on current `main` (commit `18bc4fe`, PR #466) before any edit.
- Accepted import summary (read-only input of Prompt 3, unmodified):
  `docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json`
  (sha256 `a54ebd46e8533b17738b302e6177b282348f811d7f6b694f75bea7ba2cf8285c`,
  unchanged before and after this lane).
- Real execution evidence (read-only):
  `docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-operator-supervised-local-acceptance-execution/task-execution-ledger.md`
  and the manual acceptance plan
  `docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-manual-local-acceptance-packet/manual-local-acceptance-tasks.md`.
- Tooling sources: `alpha/self_operator/acceptance_interpretation.py` (engine,
  #464), `alpha/self_operator/result_import.py` (importer, #463/#465),
  `alpha/self_operator/release_gate.py` (gate, #462),
  `scripts/interpret_self_operator_acceptance.py`,
  `tests/fixtures/self_operator_acceptance_import/complete_import_summary.json`.

## Blocker group (one shared root cause)

All 10 Prompt 3 defects, plus the latent MLA-010 expectation-map divergence that
the Prompt 3 defect register explicitly assigned to this fix lane, share one root
cause: the importer and the engine both label their interface
`self_operator.acceptance_import_summary.v1` but disagree on its shape, and the
engine misreads the importer's actual output.

Field-level verification performed in this lane (all reproduced from source):

1. **4 × P1 `EXPECTED_SAFETY_BLOCK_ALLOWED` (MLA-002..MLA-005).** The importer
   records `status: "import_ready_with_expected_blocks"` and
   `expected_safety_block_confirmed: true`. The engine's `_observed_outcome`
   token-matched `ready` inside `import_ready_with_expected_blocks` and never
   read `expected_safety_block_confirmed`, so a confirmed safety block was
   reported as "allowed". The #461 ledger records these tasks as blocked with
   stop-states. **False positive.**
2. **2 × P1 `EXPECTED_SAFETY_BLOCK_ALLOWED` (MLA-006, MLA-007).** The #461
   ledger records both as blocked via `ArtifactStoreError` (path-traversal and
   overwrite rejection) without stop-state artifacts; the importer recorded
   plain `import_ready` with `expected_safety_block_confirmed: false` and no
   observed-outcome marker. The engine's claim that the tasks were **allowed**
   is false (false-positive message, same parsing root cause), but the import
   summary genuinely does not confirm the blocks, so a truthful interpretation
   must still block. These two are restated, not resolved (see
   `remaining-defects.md`).
3. **4 × P2 `IMPORT_SUMMARY_INCOMPLETE`.** The engine required top-level
   booleans (`redaction_safe`, `evidence_boundary_preserved`,
   `source_mutation_absent`, `non_execution_proof`); the importer emits the same
   determinations as status strings (`redaction_status: "redacted"`,
   `evidence_boundary_status: "present"`,
   `source_artifact_mutation_status: "not_present"`,
   `non_execution_status: "present"`). The information is present under
   different names. **False positive.**
4. **Latent expectation-map divergence (MLA-010).** The engine's
   `EXPECTED_SAFE_TASK_IDS` listed MLA-010, but the acceptance plan (non-execution
   proof: "Stop if proposed commands execute"), the #461 ledger
   (`dry_run_status=blocked_by_failed_preflight; allowed=False`, stop-state
   artifact), and the accepted import
   (`import_ready_with_expected_blocks`, `expected_safety_block_confirmed: true`)
   all record MLA-010 as an expected safety block. The engine's own test fixture
   encoded the same wrong expectation. **Engine-side expectation defect, same
   interface-contract root cause.**

## Classification

**`tooling_false_positive`** — exactly one classification, applied to the single
shared-root-cause group above.

Rationale: the engine asserted safety failures ("expected safety-blocked task
was allowed", "missing required safety field") that the read-only evidence
contradicts; the cause is interpretation-tooling parsing and an
interpretation-tooling expectation map, not the underlying safety gates, the
importer's accepted output, or the product. No P0 evidence-boundary or
source-mutation defect was reported. The release-gate checker is not directly
responsible (it never ran and embeds no MLA expectation map), so it is out of
scope.

Not chosen:

- `true_product_defect`: no product safety gate failed; the ledger shows every
  expected block occurred.
- `evidence_defect`: the accepted import summary faithfully records what the
  importer's v1 contract can represent; it was not mutated and is not treated as
  defective by this lane. The MLA-006/MLA-007 representation gap is routed (see
  `remaining-defects.md`) rather than silently absorbed into this PR.
- `documentation_gap`, `operator_review_needed`, `deferred_non_blocking`: the
  defects are mechanical tooling false positives with code-level fixes; nothing
  here is non-blocking, and no operator judgement call is required for the false
  positives themselves.

## Severity handling

No defect was downgraded or reclassified as non-blocking. The two defects that
could not be shown false (MLA-006, MLA-007) remain P1 and continue to force a
`blocked` readiness implication in the fixed engine.
