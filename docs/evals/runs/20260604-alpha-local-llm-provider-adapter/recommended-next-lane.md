# Recommended Next Lane

Recommended next lane: `ALPHA-LOCAL-LLM-ADAPTER-REVIEW-GATE-001`.

## Purpose

Review the provider-adapter seam before any real local-provider integration is
considered. The review should verify that prompt-source preservation, failure
normalization, mode labeling, and evidence boundaries remain intact.

## Suggested review questions

1. Does the adapter keep `alpha_solver_portable.py` as the system/contract
   source and preserve SHA-256 metadata?
2. Does the adapter keep user prompt content separate from contract content?
3. Does `MODEL_PROVIDER=local` remain smoke-only?
4. Do tests avoid network, local model servers, Ollama, and provider keys?
5. Do docs avoid behavior, readiness, validation, superiority, benchmark,
   billing, Batch C, and orchestration claims?

## Not recommended in the next lane

Do not begin real Ollama calls, hosted-provider calls, `/v1/solve` integration,
dashboard preview integration, operator-test interpretation, imported evidence
modification, or Batch C work in the review gate.
