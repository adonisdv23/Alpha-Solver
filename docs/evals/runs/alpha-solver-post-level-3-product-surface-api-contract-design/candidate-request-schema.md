# Candidate Request Schema

This file defines candidate `/v1/solve` request fields without implementing them. Field names, types, and requirements are design candidates only and must be reviewed by Level 6 and a later implementation spec before any route exists.

## Candidate top-level fields

| Field | Candidate type | Candidate requirement | Contract requirement |
| --- | --- | --- | --- |
| `input` | object | Required | Contains the problem or task to solve. Must support validation without executing a solver. |
| `input.prompt` | string | Required | User-visible problem statement. Must be non-empty after trimming and must respect length limits. |
| `input.context` | array of objects | Optional | User-provided context documents or snippets. Must distinguish user-provided context from accepted repository evidence. |
| `input.attachments` | array of objects | Optional | Metadata-only references to attachments. Raw attachment ingestion is out of scope unless separately approved. |
| `mode` | string enum | Required | Candidate values may include `draft`, `bounded_answer`, or `analysis_only`; exact values require later approval. |
| `solver_profile` | string enum | Optional | Identifies an approved solver configuration. Must not directly select unsafe provider behavior. |
| `evidence_policy` | object | Required | States whether external evidence is allowed, required, or forbidden for the request. |
| `evidence_policy.required` | boolean | Optional | If true, response must fail or safe-out when evidence is missing. |
| `evidence_policy.allowed_sources` | array of strings | Optional | Candidate allowlist labels, not URLs to fetch automatically without a later browsing/provider spec. |
| `claim_policy` | object | Required | Declares claim boundaries such as whether readiness, quality, or benchmark claims are forbidden. |
| `trace` | object | Optional | Caller-supplied trace metadata that must be sanitized before logging. |
| `trace.client_request_id` | string | Optional | Client-provided idempotency or correlation key; must be validated and bounded. |
| `options` | object | Optional | Explicit, bounded execution options such as timeout preference or verbosity. |

## Candidate validation rules

- `input.prompt` must be present, must be a string, and must not be blank after trimming.
- Request size must have a documented maximum before implementation.
- Context item count, context item size, and total context size must have documented maximums before implementation.
- Unknown fields should either be rejected or collected under a documented extension policy; silent acceptance is not allowed.
- `mode`, `solver_profile`, and `evidence_policy` values must be allowlisted.
- A future implementation must validate before provider selection, route execution, solver execution, billing attribution, or evidence loading.
- A future implementation must not use request fields to bypass SAFE-OUT, budget guard, privacy guard, claim-boundary guard, or blocked-execution guardrails.

## Candidate non-fields

The request schema should not include raw secrets, provider API keys, billing credentials, local filesystem paths, unrestricted URLs, direct model prompts, direct chain-of-thought requests, or flags that force hidden reasoning disclosure.
