# Evidence chain summary

Full table: [`docs/EVIDENCE_INDEX.md`](../../../EVIDENCE_INDEX.md).

The merged chain #497→#509 is two sub-chains:

- **Local Self Operator execution evidence** (#497, #499, #500, #501): offline,
  provider-free; suite + release-gate pass; operator approval captured; local
  safety gate exercised. DEF-001 advanced (local-only), not fully retired.
- **OpenAI pre-smoke governance** (#502–#508) then **blocked smoke retry**
  (#509): plan → DEF-002/003 boundary → data-sharing verification → smoke
  capture (blocked: attestation missing) → synthetic fixture → operator
  attestation → checker scope → retry (blocked: project/billing not verified).

**Controlling head:** PR #509 (`local-openai-token-smoke-capture-retry-001`),
verdict `BLOCKED_OPENAI_PROJECT_OR_BILLING_NOT_VERIFIED`. No provider call has
been made anywhere in this chain.
