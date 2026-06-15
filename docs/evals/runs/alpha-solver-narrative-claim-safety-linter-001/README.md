# Narrative Claim-Safety Linter Evidence Packet

Lane: `ALPHA-SOLVER-NARRATIVE-CLAIM-SAFETY-LINTER-001`

## Evidence summary

This packet records an offline static documentation guard for narrative claim
safety. Claim boundaries: it does not rewrite prior evidence, delete evidence
packets, call providers, or update Google Sheets. It is out of scope to validate
readiness, prove benchmark outcomes, prove superiority, confirm public exposure
safety, or validate security/privacy.

## Rules added

The checker covers unsupported readiness, validation, benchmark, superiority,
provider, public exposure, and security/privacy claim families. Each finding
includes a bounded alternative so the false positive is actionable rather than a
bare regex failure.

## Fixture coverage

- Synthetic founder-style memo: readiness, validation, superiority, and
  security/privacy overclaims.
- Synthetic demo-style artifact: benchmark, provider, and public exposure
  overclaims.
- Boundary-context fixture: explicit claim-boundary wording remains allowed.
- Suppression fixtures: bare suppressions fail; suppressions with an explicit
  rationale pass for the local line only.

## Residual risks

- This is not a completeness claim; static matching can miss paraphrases and
  context-dependent overclaims.
- Human review is still required for evidence adequacy and for final narrative
  approval.
- Suppression rationales are checked for presence and minimum length, not for
  truth.
- Images, binary artifacts, private docs, Google Sheets, live endpoints, and
  provider systems are out of scope.

## Checks

- `python -m pytest tests/test_narrative_claim_safety.py -q`
- `git diff --check`
