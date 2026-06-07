# Candidate Response Schema

This file defines candidate `/v1/solve` response envelope fields without implementing them. The response schema is a design candidate only and must not be treated as an active API contract.

## Candidate response envelope

| Field | Candidate type | Candidate requirement | Contract requirement |
| --- | --- | --- | --- |
| `status` | string enum | Required | Candidate values may include `completed`, `safe_out`, `blocked`, `failed`, or `timed_out`. |
| `request_id` | string | Required | Server-assigned request identifier for traceability. |
| `run_id` | string | Conditional | Assigned when execution begins; absent or null if validation fails before execution. |
| `answer` | object or null | Conditional | Present only when an answer is safely produced. Must not include unsupported claims. |
| `answer.summary` | string | Conditional | User-visible bounded answer. Must be redacted and evidence-aware. |
| `answer.assumptions` | array of strings | Optional | Explicit assumptions used to bound the answer. |
| `evidence` | object | Required | Describes evidence references, missing evidence, and evidence boundary. |
| `evidence.references` | array of objects | Required | References to approved evidence artifacts, not raw secret-bearing payloads. |
| `evidence.missing` | array of strings | Optional | Required evidence that was unavailable or insufficient. |
| `decision_log` | object | Required | Summarizes validation, routing, safety, evidence, and stop-condition decisions. |
| `errors` | array of objects | Required | Empty on success; populated for validation, safety, provider, timeout, or blocked states. |
| `usage` | object | Optional | Bounded accounting metadata only if approved by billing and provider specs. |
| `redactions` | array of objects | Optional | Describes classes of data redacted without disclosing the data itself. |
| `metadata` | object | Optional | Version, schema, runtime mode, and feature-gate metadata safe for callers. |

## Candidate error object

| Field | Candidate type | Candidate requirement |
| --- | --- | --- |
| `code` | string | Stable machine-readable error code. |
| `category` | string | One of the approved error categories. |
| `message` | string | Safe user-facing message. |
| `retryable` | boolean | Whether retry may be appropriate. |
| `details` | object | Redacted bounded diagnostic details. |
| `evidence_boundary` | string | Explanation when evidence limitations affect the outcome. |

## Response constraints

- A response must never expose provider secrets, hidden reasoning, raw chain-of-thought, raw private payloads, or unredacted sensitive inputs.
- A response must not claim quality, benchmark success, MVP readiness, production readiness, or Alpha superiority without later accepted evidence.
- A response must distinguish validation failure from solver failure, unsafe claim blocking, provider unavailability, timeout, and blocked execution.
- A response must preserve enough traceability to audit the outcome without requiring sensitive raw data exposure.
