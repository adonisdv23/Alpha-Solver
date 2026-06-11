# Evidence preservation rules

How source artifacts must be preserved, in this lane and in every future
operator-use lane, restating the canonical runbook (section 14).

## Rules

1. Source artifacts are consumed read-only. They are never mutated, moved,
   rewritten in place, renamed, or deleted by later lanes.
2. Earlier evidence is never recreated; a later lane that needs it re-reads
   it where it stands.
3. Evidence is never promoted by summarizing it: downstream lanes must
   re-read source packets, and packet summaries (including this packet) are
   not substitutes for the sources they cite.
4. Each lane writes only inside its own allowed file list; any change
   outside it is `blocked_out_of_scope_change` and stops the lane.
5. Every evidence packet records its boundary (`evidence-boundary.md`) and
   deliberate non-actions (`non-actions.md`).
6. Defects are recorded in the owning lane's defect register; prior evidence
   is never edited to make a defect disappear.
7. Raw output roots stay outside the repository; only copied, redacted
   artifacts enter packets, through lane review.

## Conformance of this prep lane

- Every source listed in `source-evidence-reviewed.md` was consumed
  read-only and left byte-identical.
- This lane created only new files inside
  `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-post-closeout-operator-use-prep/`.
- The closeout packet, the repair packet, the runbook, the release gate, all
  code, and all tests are unchanged, as verified by `git diff --name-only`
  in `checks-run.md`.
