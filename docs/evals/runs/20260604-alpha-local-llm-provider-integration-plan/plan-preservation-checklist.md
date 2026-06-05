# Plan Preservation Checklist

## Scope

- [x] Added docs only under
  `docs/evals/runs/20260604-alpha-local-llm-provider-integration-plan/`.
- [x] No source code changes are part of this lane.
- [x] No test changes are part of this lane.
- [x] No runtime, provider, model, routing, API, or dashboard changes are part
  of this lane.

## Source-of-truth preservation

- [x] Reviewed `alpha/local_llm/provider_adapter.py`.
- [x] Reviewed `alpha/local_llm/__init__.py`.
- [x] Reviewed `alpha/local_llm/portable_contract.py`.
- [x] Reviewed `tests/test_local_llm_provider_adapter.py`.
- [x] Reviewed `tests/test_local_llm_contract_consumption_proof.py`.
- [x] Reviewed prior adapter and review-gate evidence directories.

## Required plan content

- [x] Future connection path from the existing adapter seam to a local backend is
  described.
- [x] Provider options are planning-only.
- [x] `provider_mode="local_llm"` remains distinct from `MODEL_PROVIDER=local`.
- [x] `MODEL_PROVIDER=local` remains smoke-only unless a later approved lane
  explicitly changes it.
- [x] Portable-contract path, SHA-256 fingerprint, fingerprint algorithm, and
  user/system separation are preserved.
- [x] Authorization requirements are defined before any real provider call.
- [x] Timeout, connection failure, malformed response, empty output, prompt echo,
  missing contract, empty contract, fingerprint mismatch, and backend errors are
  covered in the failure plan.
- [x] Test plan starts with offline stubs and fixtures.
- [x] Separately authorized local smoke tests are deferred.
- [x] Blocked work remains blocked until a later implementation lane.
- [x] Exactly one recommended next lane is selected:
  `ALPHA-LOCAL-LLM-PROVIDER-INTEGRATION-SPEC-001`.
