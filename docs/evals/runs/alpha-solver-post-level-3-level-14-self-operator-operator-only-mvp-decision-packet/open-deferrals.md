# Open deferrals

These deferrals are carried forward from the PR #493 deferral register and the PR #495
operator sign-off. They remain open. Operator sign-off accepted them as open deferrals;
it did not resolve the underlying missing evidence. None of them is marked complete or
resolved by this packet.

## DEF-001 — Self Operator execution evidence

- Status: open deferral. Explicitly accepted as an open deferral in the PR #495
  `operator-signoff-record.md`.
- What remains missing: execution evidence for the Self Operator candidate — logs,
  test-run records, or runtime artifacts demonstrating behavior of the package under
  audit.
- Standing constraint: this remains a hard precondition before expanding the Self
  Operator beyond operator-supervised local use. No output of this packet may be
  described as evidence that the Self Operator executes correctly.

## DEF-002 — Product-level security/privacy review

- Status: open deferral. Explicitly accepted as an open deferral in the PR #495
  `operator-signoff-record.md`.
- What remains missing: a product-level security/privacy review for the Self Operator:
  threat model, secret scan, dependency vulnerability analysis, privacy assessment.
- Standing constraint: this remains required before any exposure beyond the
  operator-supervised self-operator context.

## DEF-003 — Prior targeted Fable delta audit full text

- Status: open deferral. Explicitly accepted as an open deferral in the PR #495
  `operator-signoff-record.md`.
- What remains missing: the full text of the prior targeted post-annex Fable delta audit.
  It is operator-held or missing from repository evidence; only its summarized result is
  cited in Council bundle documents.
- Standing constraint: it may be cited only as "reported no P0/P1 blockers" — a
  summarized model/auditor judgment, not independent proof, and not a basis for treating
  F-1/N-1 confirmation as complete.

## DEF-004 — Custody note: Council raw capture and synthesis report

- Status: custody traceability note. Preserved as a custody note; not converted into
  repository evidence by this lane.
- What is off-repository: the cleaned raw Council capture file (16 usable raw audit
  responses plus 1 documented failed platform slot) and
  `ALPHA-SOLVER-COUNCIL-SYNTHESIS-REPORT-001`. The controlling documents are
  operator-held.
- Standing constraint: DEF-004 is not a hard blocker for this lane provided the operator
  can produce the operator-held documents on request. This packet does not claim those
  documents are present in the repository.

## Summary table

| Deferral | Subject | Open? | Treated as resolved evidence? |
|---|---|---|---|
| DEF-001 | Self Operator execution evidence | Yes — open | No |
| DEF-002 | Product-level security/privacy review | Yes — open | No |
| DEF-003 | Prior targeted Fable delta audit full text | Yes — open | No |
| DEF-004 | Council raw capture and synthesis report custody | Custody note | No (operator-held, not repository evidence) |
