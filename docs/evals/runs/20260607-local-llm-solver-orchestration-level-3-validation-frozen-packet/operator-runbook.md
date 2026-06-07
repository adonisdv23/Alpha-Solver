# Operator Runbook for a Future Execution Lane

## Preconditions

A future operator must confirm all of the following before any validation execution:

1. A later authorization lane has been selected and merged.
2. A later, separate execution lane has been selected and merged after authorization.
3. The execution lane explicitly permits local model inference.
4. The endpoint is loopback-only.
5. The timeout is finite and positive.
6. No hosted provider keys are present, required, accepted, used, or exposed.
7. No provider fallback and no hosted fallback are configured.
8. `/v1/solve` and dashboard surfaces are not exposed or called.
9. The preserved source artifact and Level 2 closeout/import/design packet files remain unmodified.

## Future execution sequence

For each frozen test case:

1. Record the exact repo HEAD.
2. Copy the prompt text from `frozen-test-set.md` without editing it.
3. Expand the command template from `frozen-invocation-template.md` using the test-case prompt.
4. Record the fully expanded command before execution.
5. Execute only if a later merged execution lane authorizes execution.
6. Capture stdout, stderr, exit code, endpoint locality metadata, timeout value, safety flags, and operator/environment notes.
7. Parse stdout as normalized JSON.
8. Record the normalized JSON `status` and required safety flag values.
9. Apply the redaction policy.
10. Apply stop conditions before any review conclusion.
11. Review only the rubric dimensions; do not make model-quality, benchmark, production, MVP, provider-orchestration, Alpha superiority, billing, dashboard, `/v1/solve`, broad runtime, or evidence-model-promotion claims.

## Non-action statement

This runbook is future-only. This packet does not start the selected next lane and does not execute validation.
