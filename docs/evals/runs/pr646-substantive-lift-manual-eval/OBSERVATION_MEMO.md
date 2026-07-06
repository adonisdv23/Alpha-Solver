# PR646 Substantive Lift Manual Eval Observation Memo

Lane: `PR646-SUBSTANTIVE-LIFT-MANUAL-EVAL-PREP-001`

## Source and merge-state note

Local repository history shows the prerequisite PR commits present on this branch:

- PR #646: `portable: add substantive lift answer contract`.
- PR #647: `tot: bound non-substantive local template outputs`.
- PR #648: `Cap unsupported SAFE-OUT confidence`.
- PR #649: `eval: add PR646 manual substantive-lift eval prep packet and runbook`.

This memo is based on the operator-provided issue-comment summary of two final
ChatGPT ghost-chat exports. The raw ghost-chat export files are not present in
this repository, so this memo does not claim direct access to raw exports.

## Observation boundary

This is a qualitative observation memo only. It does not score the outputs,
rank the outputs, pick a winner, claim Alpha superiority, claim benchmark
status, claim readiness, or treat the ghost-chat test as proof.

The test has a material caveat: the Alpha `.py` thread appeared more repo-aware
than the baseline thread. That makes the result operator signal from an
as-run ghost-chat comparison, not a clean controlled proof of the PR #646 answer
contract or of Alpha Solver superiority.

## Qualitative operator signal

The issue-comment summary indicates the Alpha-thread output more consistently
presented the answer as an operator-actionable memo: it made the intent of the
question explicit, called out hidden assumptions, named a dominant tradeoff,
committed to a bounded recommendation, and preserved a concrete failure
condition or next action.

The same summary indicates the baseline-thread output was usable as general
analysis, but appeared less anchored to the repo-specific contract and less
consistent about separating observation, caveat, and next diagnostic action.
Because the baseline thread may have had less effective repo context, this is
not interpretable as a controlled treatment effect.

## Diagnostic follow-up from the run

The operator signal raised a possible diagnostic-surface parity issue in
`alpha_solver_portable.py`: user-visible portable SAFE-OUT honesty fields were
being adjusted, while the exported `diagnostics.tot` surface did not expose the
same confidence and unsupported-synthesis markers. That issue is narrow and
mechanical rather than an answer-quality claim.

The follow-up implementation should therefore stay limited to parity of
portable diagnostic fields and a focused regression test. It should not broaden
runtime behavior, route/persona behavior, provider execution, scoring, or eval
claims.

## Allowed use

This memo may be cited only as preservation of operator-observed qualitative
signal and as justification for the narrow diagnostic-surface parity check. It
must not be cited as benchmark evidence, production-readiness evidence, a clean
A/B comparison, or proof that Alpha Solver outperforms a baseline.
