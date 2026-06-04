# Readiness Review Gates

Lane ID: `ALPHA-OPERATOR-TEST-BATCH-C-RUNTIME-FIREWALL-001`

Status: gates documented; no gate is passed by this memo.

## Gate rule

No downstream gate is passed by the existence of this firewall memo, by packet preparation, by future limited operator feedback, by future result import, or by future interpretation. Each gate requires a separate explicit readiness decision.

## Gate 1: operator-test execution gate

Required before claiming an operator test was executed:

- The approved packet must have been run manually by the named operator or another approved operator.
- Filled feedback and defect records must exist as records, not invented summaries.
- Stop conditions must be checked.
- Preservation boundaries must be followed.

Not enough:

- Packet preparation.
- Empty templates.
- Planned tasks.
- Informal statements that feedback exists without preserved records.

## Gate 2: results-import gate

Required before importing future operator-test records:

- Confirm the import is records-only.
- Preserve source records without rewriting them into validation claims.
- State that results import is not validation.
- Avoid scoring, rescoring, benchmark totals, or unapproved interpretation.

Not enough:

- Positive or negative operator comments.
- A completed template without an approved preservation/import lane.
- Any desire to update Google Sheets or scored artifacts.

## Gate 3: interpretation gate

Required before interpreting future imported operator-test feedback:

- Use a separate interpretation lane.
- Stay within the limited operator-test and portable-surface evidence boundary.
- Distinguish usability feedback from validation.
- Preserve non-claims around production readiness, runtime readiness, Batch C, `/v1/solve`, provider orchestration, and exact billing.

Not enough:

- Record import alone.
- A small number of positive operator notes.
- Lack of defects in a limited operator packet.

## Gate 4: Batch C readiness gate

Required before starting Batch C:

- A separate Batch C readiness decision.
- Approved Batch C objective and scope.
- Approved prompt set and prompt-provenance rules.
- Approved capture, scoring, unblinding, and preservation plan.
- Stop conditions and non-claim boundaries.
- Confirmation that Batch C does not depend on fabricated or imported-as-validation results.

Not enough:

- Limited operator-test feedback.
- Limited operator-test interpretation.
- Prior portable-surface scored results.
- Completion of brevity/control refinement.
- This firewall memo.

## Gate 5: runtime wiring/readiness gate

Required before runtime work:

- A separate runtime wiring/readiness review.
- Named runtime surfaces and entrypoints.
- Instrumentation and observability requirements.
- Safety, rollback, and protected-surface review.
- Evidence plan for actual runtime behavior.
- Explicit authorization for any provider, model-routing, billing, or `/v1/solve` use.

Not enough:

- Portable contract wording.
- Operator-test feedback.
- Batch C planning.
- Docs-only interpretation.

## Gate 6: `/v1/solve` measurement gate

Required before claiming `/v1/solve` behavior:

- Separate measurement on the actual `/v1/solve` surface.
- Preserved request/response evidence subject to approved privacy and artifact rules.
- Runtime instrumentation sufficient to support the claim.
- Separate interpretation limited to measured evidence.

Not enough:

- Portable-surface outputs.
- Provider-agnostic prompt-contract behavior.
- Operator usability feedback.
- Runtime-adjacent documentation.

## Gate 7: provider orchestration and exact billing gate

Required before provider orchestration or exact billing claims:

- Separate provider orchestration authorization.
- Provider-adapter and routing readiness review.
- Billing instrumentation and reconciliation plan.
- Preserved measurements from live or approved simulated surfaces.
- Explicit accounting for failures, retries, fallbacks, budget guard behavior, and cost reconciliation.

Not enough:

- Any operator-test result.
- Any portable-surface score.
- Any docs-only interpretation.
- Any unmeasured runtime assumption.
