# Decision rationale

Why the operator's `ACCEPT_LEDGER_LEVEL_CONFIRMATION` decision is recorded
here as a reasonable, bounded decision — and what the rationale deliberately
does not argue.

## Grounds supporting acceptance

1. **The attestation is consistent and uncontradicted.** #468's field-level
   review (`artifactstoreerror-confirmation-review.md`) found the prose
   evidence "consistent, operator-attested, and uncontradicted", with the
   observed-result prose matching the expected safety-block contract for both
   tasks (traversal rejection before write for MLA-006; overwrite rejection on
   second invocation for MLA-007). No artifact, ledger row, or review in any
   packet contradicts either block.

2. **The absence of machine-readable rejection records is the designed
   behavior under test, not an evidence gap introduced by sloppiness.** Both
   scenarios verify rejection *before* any artifact write inside the blocked
   output root. A wrapper that wrote a rejection artifact into that root would
   fail the very property being tested. MLA-007's existing artifacts correctly
   record only the allowed first invocation.

3. **The attestation was produced under the supervised-execution controls of
   #461**: operator confirmation PRESENT, empty defect log, no
   FAIL/BLOCKED/NOT RUN rows, artifact integrity checks PASS — reviewed
   read-only in `source-evidence-reviewed.md`.

4. **The decision is explicit and attributable, which is the exact remedy
   #468 required.** Machine confirmation from prose is forbidden; silent
   inference was refused twice (#467, #468). What was missing was a human
   decision on the record. This packet is that record: the decision value was
   supplied verbatim in this lane's operator instruction and is restated in
   `operator-decision.md` / `operator-decision.json`.

## What this rationale does not argue

- It does **not** argue that the ledger prose is machine-readable evidence,
  or that operator acceptance is equivalent to machine-readable artifact
  confirmation. `operator-decision.json` records
  `machine_readable_artifact_confirmation: false`.
- It does **not** argue that the P1 defects were false positives. The engine's
  `EXPECTED_SAFETY_BLOCK_UNCONFIRMED` reports were truthful reports of the
  import summary's contents and remain truthful today.
- It does **not** argue that a machine-readable rerun would be valueless —
  the operator weighed that branch (`operator-review-required.md`, branch 2)
  and chose acceptance; the rerun branch remains available later if wanted.
- It does **not** extend the acceptance beyond MLA-006 and MLA-007, and it
  carries no readiness implication of any kind.
