# Forbidden claims

The following phrases remain blocked as project status claims for the Self
Operator path. They appear in this packet only as documentation of what is
blocked (this list, the blocked-claim guardrail tests, and the scan record),
never as status assertions:

- MVP ready
- release ready
- production ready
- runtime ready
- provider ready
- hosted ready
- benchmark validated
- benchmark superior
- autonomous ready
- broad user ready

Also blocked, regardless of wording:

- any claim that the Self Operator path may run providers, hosted or local
  models, external APIs, browser automation, `/v1/solve` or dashboard
  routes, deployment, billing, or credential/secret access;
- any claim that operator ledger-level acceptance is machine-readable
  artifact confirmation;
- any claim that acceptance "passed" constitutes final release evidence;
- any readiness claim conditioned on evidence that does not exist.

The guardrail suite (`tests/test_self_operator_closeout_guardrails.py`)
fails if any of the phrase-form claims above appears in this packet outside
forbidden-claim documentation files.
