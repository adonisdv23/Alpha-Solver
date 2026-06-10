# Blocker review

## Blocker group (exactly one shared root cause)

```
The accepted import summary does not currently machine-confirm MLA-006 and
MLA-007 as expected safety blocks.
```

Members:

```
MLA-006: EXPECTED_SAFETY_BLOCK_UNCONFIRMED (P1)
MLA-007: EXPECTED_SAFETY_BLOCK_UNCONFIRMED (P1)
```

No new blocker classes or unrelated root causes were combined into this group.
Verification against the unchanged accepted import
(`verification-interpretation-result.json`) reports exactly these two defects
(`blocked`, p0=0, p1=2, p2=0, p3=0) and nothing else, so the group boundary is
exact.

## Root cause

One shared root cause, inherited from the #461 scenario design meeting the
importer's v1 representation:

1. The MLA-006 and MLA-007 acceptance scenarios verify that the dry-run
   wrapper's artifact store **rejects before writing**: path traversal
   (MLA-006) and overwrite with `overwrite=false` (MLA-007) raise
   `ArtifactStoreError` and produce no new JSON artifacts — that rejection-
   before-write *is* the safety behavior under test.
2. Consequently the only records of the two rejections are operator-attested
   prose in the #461 packet (task-execution-ledger rows, stop-state-review
   rows, raw-artifact README `Notes:` lines). No machine-readable artifact
   anywhere in the packet contains the error value (full inventory in
   `artifactstoreerror-confirmation-review.md`).
3. The importer's v1 contract sets `expected_safety_block_confirmed` only from
   a validated `stop-state.json` artifact. With no artifacts (MLA-006) or only
   allowed-first-invocation artifacts (MLA-007), it correctly emits
   `expected_safety_block_confirmed: false`.
4. The fixed engine (#467) truthfully reports an expected block that the import
   summary does not confirm: P1 `EXPECTED_SAFETY_BLOCK_UNCONFIRMED`.

Neither tool misbehaves against its own contract. The gap is that the
*evidence needed for machine confirmation does not exist in machine-readable
form*, and the lane contract forbids deriving confirmation from the prose
sources that do exist.

## Why an importer-only fix is not supported by the evidence

The lane prefers an importer-only fix, but only for a `tooling_false_positive`
caused by an importer representation gap — i.e., the machine-readable evidence
exists and the importer merely fails to represent it. That premise fails here:

- For MLA-006 there is **no artifact file at all** (`raw-artifacts-index.md`
  row: Produced "None"; directory contains only `README.md`). There is no
  artifact path or JSON pointer an importer could read.
- For MLA-007 the only machine-readable artifacts record the **opposite**
  signal — the allowed first invocation (`/allowed = true`,
  `/gate_status = "allowed_for_local_dry_run_wrapper"`). The blocked second
  invocation left no machine-readable record.
- Every occurrence of the exact error values is prose. An importer patched to
  mine the ledger "Observed result" cells or README `Notes:` lines would
  confirm from prose-only inference and from "prior docs say the task passed" —
  both forbidden confirmation sources. The patch would *fabricate* a
  machine-readable confirmation the underlying evidence does not contain.
- The ArtifactStoreError confirmation rule requires six elements
  (exact artifact path; exact JSON pointer/field path; exact error value;
  proof of blocked/rejected unsafe action; proof of task ownership; proof of
  contract match) and mandates: if any element is missing, classify as
  `operator_review_needed` or `evidence_defect` and **do not patch importer
  behavior**. Elements 1–3 (and machine-readable forms of 4–6) are missing for
  both tasks (`artifactstoreerror-confirmation-review.md`).

## Decision

Classification: `operator_review_needed` (rationale and rejected alternatives
in `classification-result.md`). The group is routed to explicit operator
review (`operator-review-required.md`); both P1 defects remain open at P1.
