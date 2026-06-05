# Post-Execution Import Instructions

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001`

No smoke result is imported in this packet-preparation PR.

## Future import lane requirement

After authorized execution, results must be imported in a future docs-only import lane. The future import lane must:

1. Reference `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-001` as the execution lane.
2. Reference this packet lane as source instructions.
3. Reference the review gate artifact that explicitly authorized smoke.
4. Preserve raw artifact references without overwriting raw artifacts.
5. Include a sanitized result using `sanitized-artifact-template.md`.
6. Include raw stdout, stderr, command, exit code, config summary, and sanitized result references.
7. Preserve `behavior_evidence=false`.
8. State whether the outcome was `non_evidence` or `failed_closed`.
9. Avoid readiness, validation, superiority, benchmark, production, MVP, runtime, billing, provider-orchestration, hosted-provider, local-model-quality, `/v1/solve`, or dashboard-preview claims.

## Import block conditions

Do not import results if:

- the review gate did not explicitly authorize smoke;
- raw artifacts are missing;
- command or exit code is missing;
- stdout or stderr capture is missing;
- config summary is missing;
- sanitization cannot be performed safely;
- hosted fallback or provider-key use is suspected and not clearly classified.
