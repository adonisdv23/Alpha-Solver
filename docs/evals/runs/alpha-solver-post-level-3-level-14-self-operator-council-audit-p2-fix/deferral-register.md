# Deferral register

Each entry below is an explicit, recorded deferral. A deferral is not a resolution: the underlying evidence remains missing until the unblock condition is met. Operator acceptance of this packet constitutes acceptance of these deferrals as recorded.

## DEF-001 — Self Operator execution evidence (P2-004)

- What is missing: execution evidence for the Self Operator candidate — logs, test-run records, or runtime artifacts demonstrating behavior of the package under audit. The Council run evaluated process evidence only; both Execution Integrity seats reported this gap.
- Why deferred: producing execution evidence requires running product behavior, which is forbidden in this documentation-only lane and was forbidden in the Council lane.
- Unblock condition: a future, separately authorized execution-evidence lane produces and records run artifacts with inputs, outputs, and success/failure criteria.
- Standing constraint: this deferral is a hard precondition for any lane that would expand the Self Operator beyond operator-supervised local use. The release-gate review lane may proceed for the narrow scope only; see the pass conditions in `release-gate-acceptance-criteria.md`. No output of this packet or of the Council run may be described as evidence that the Self Operator executes correctly.

## DEF-002 — Product-level security/privacy review (P2-005)

- What is missing: a product-level security/privacy review for the Self Operator: threat model, secret scan, dependency vulnerability analysis, privacy assessment.
- Why deferred: the surviving Security / Privacy Council seat recorded this gap as deferrable at the current stage; performing the review is outside this documentation-only lane. The Venice - Auto platform failure left this lens covered by a single substantive seat, which strengthens the case for a dedicated review later.
- Unblock condition: a dedicated security/privacy review lane completes and records its artifacts.
- Standing constraint: must be met before any exposure beyond the operator-supervised self-operator context. Recorded as scheduled-not-started.

## DEF-003 — Prior targeted Fable delta audit full text

- What is missing: the full text of the prior targeted post-annex Fable delta audit. It is not in this repository; only its summarized result is cited in Council bundle documents.
- Why deferred: the document is operator-held; importing it was not in scope for this lane.
- Unblock condition: the operator adds the full audit text to the repository or supplies it to the release-gate review lane on request.
- Standing constraint: until then, the audit may be cited only as "reported no P0/P1 blockers" — a summarized model/auditor judgment, not independent proof, and not a basis for treating F-1/N-1 confirmation as complete.

## DEF-004 — Custody note: Council raw capture and synthesis report

- What is off-repository: the cleaned raw Council capture file (16 usable raw audit responses plus 1 documented failed platform slot, with per-slot SHA-256 prefixes and character counts in its manifest) and `ALPHA-SOLVER-COUNCIL-SYNTHESIS-REPORT-001`.
- Why recorded: repository traceability. `council-synthesis-summary.md` summarizes them, but the controlling documents are operator-held.
- Unblock condition: optional future import into the repository; not required for the release-gate review lane provided the operator can produce the documents on request.

## Backlog (recorded, not deferral-gated)

- No-go-list enforcement check in CI (VER-002 outcome; see `repo-state-verification.md`).
- Red-team adversarial annex for the Self Operator (out of scope for the Council lane; raised by two red-team seats).
