# Validation and Errors

## Validation sequence

A future implementation must validate in this order before any solver or provider execution:

1. route availability and feature gate;
2. request method and content type;
3. request size and schema;
4. required fields and enum allowlists;
5. privacy and secret-detection checks;
6. evidence policy and evidence availability checks;
7. claim-policy checks;
8. provider, timeout, and execution budget availability checks;
9. blocked-execution checks;
10. final decision to execute, safe-out, block, or fail.

## Candidate error categories

| Category | Candidate use | Required behavior |
| --- | --- | --- |
| `invalid_input` | Malformed JSON, missing required fields, invalid enum values, oversize request, unsupported field combinations. | Return structured validation errors before execution. |
| `missing_evidence` | Required evidence is unavailable, insufficient, stale, or outside accepted boundaries. | Safe-out or fail without inventing evidence. |
| `unsupported_route` | `/v1/solve` is unavailable, disabled, or not exposed in the current environment. | Return a clear unsupported route or disabled feature response without executing solver logic. |
| `unsafe_claim` | Request asks for quality, readiness, benchmark, legal, medical, financial, or unsupported product claims outside accepted evidence. | Block or safe-out and explain the claim boundary. |
| `provider_unavailable` | Required provider is disabled, unreachable, missing credentials, rate-limited, or otherwise unavailable. | Do not silently fall back unless an approved fallback spec exists and actually executes. |
| `timeout` | Validation, evidence preparation, provider call, or solver execution exceeds configured limits. | Stop execution and return a bounded timeout error with trace IDs. |
| `blocked_execution` | Feature gate, policy gate, budget gate, safety gate, privacy gate, or operator gate prevents execution. | Return blocked status with safe reason and no provider call. |

## Error-code requirements

- Error codes must be stable, documented, and test-covered before route exposure.
- Error messages must be safe for callers and must not leak secrets or hidden reasoning.
- Retry guidance must be explicit and conservative.
- Provider and timeout errors must not imply local fallback execution unless fallback actually occurred under an approved design.
- Missing evidence and unsafe claim errors must preserve the accepted evidence boundary rather than fabricating confidence.
