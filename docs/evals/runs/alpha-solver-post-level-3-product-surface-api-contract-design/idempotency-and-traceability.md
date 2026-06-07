# Idempotency and Traceability

## Required future identifiers

A future `/v1/solve` implementation must define these identifiers before any route exists:

- `request_id`: server-assigned identifier for the received request.
- `client_request_id`: optional caller-supplied idempotency or correlation key, validated and bounded.
- `run_id`: server-assigned identifier for an execution attempt after validation passes.
- `decision_log_id`: identifier for the validation, routing, safety, evidence, and stop-condition decision log.
- `evidence_reference_id`: identifier for each approved evidence artifact referenced by the response.

## Candidate idempotency requirements

- Idempotency must be defined before any billing, provider call, or retry behavior exists.
- Replayed requests with the same `client_request_id` must have documented behavior for same payload, different payload, expired key, partial execution, timeout, and provider failure cases.
- Idempotency records must not store raw secrets, raw private payloads, or hidden reasoning.
- Idempotency must not be used to bypass validation, evidence checks, privacy gates, claim checks, provider gates, or blocked-execution gates.

## Decision log requirements

A future decision log should record, in redacted form:

1. schema validation result;
2. route and feature-gate result;
3. privacy and redaction result;
4. evidence-policy result;
5. claim-policy result;
6. provider availability result;
7. timeout and execution-budget decision;
8. blocked-execution decision;
9. final status and error category, if any;
10. evidence references used or missing.

Decision logs are audit metadata, not public proof of answer quality. They must not promote evidence, benchmark claims, MVP readiness, production readiness, or Alpha superiority.
