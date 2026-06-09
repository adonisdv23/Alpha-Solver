# Readiness Implication Contract

Allowed readiness implications are only:
- `blocked`
- `needs_review`
- `eligible_for_later_release_review`

`blocked` is emitted for any `P0` or `P1` defect, malformed or missing required artifacts, redaction failure, non-execution failure, evidence-boundary failure, source mutation concern, unexpected ready unsafe tasks, or unexpected failures of expected safe tasks.

`eligible_for_later_release_review` may be emitted only when `MLA-001` through `MLA-010` are present, expected safe tasks are import-ready, expected safety-blocked tasks are blocked as expected, no `P0`/`P1`/`P2`/`P3` defects exist, non-execution proof exists, evidence boundary is preserved, and redaction is safe.

This status does not claim MVP readiness.
