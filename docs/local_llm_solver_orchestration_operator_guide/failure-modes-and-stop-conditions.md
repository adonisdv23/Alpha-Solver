# Failure Modes and Stop Conditions

## Failure modes

- `clarify`: The prompt or Pass 1 result is too broad, too underspecified, or missing important context. Refine the prompt.
- `block`: The runner detected a high-risk or blocked condition and withheld an answer.
- `failed_closed`: The runner stopped rather than exposing unsafe, ambiguous, malformed, or boundary-violating output.
- Parse failure: Pass 1 or Pass 2 output could not be parsed safely, was empty, echoed prompt/system text, or had unsafe shape.
- `missing_information_too_broad`: The missing information or prompt scope is too broad for a safe bounded answer.
- Explicit high risk: The prompt or model risk flags indicate high-risk content, safety bypass, concealment, evasion, self-harm, weapons, explosives, credential theft, data exfiltration, malware, phishing, unauthorized access, or similar unsafe categories.
- Boundary failure: The prompt or output attempts to claim readiness, benchmarks, superiority, production use, provider orchestration evidence, evidence-model promotion, or other blocked claims.
- Unsafe field exposure: The result exposes raw prompt/model/diagnostic text where only bounded fields or redacted diagnostics are allowed.
- Local endpoint unavailable: Ollama or the loopback endpoint is not available.
- Timeout: The finite local timeout is reached.

## Stop conditions

Stop immediately if any of the following occurs:

- unsafe fields appear;
- raw `gate_trace` content appears;
- hosted provider fallback appears;
- `/v1/solve` or dashboard exposure appears;
- output is being used for readiness, model-quality, benchmark, provider orchestration, Alpha superiority, billing, broad runtime readiness, or evidence-model promotion claims;
- output contains positive readiness, benchmark, provider-orchestration, Alpha-superiority, `/v1/solve`, dashboard, billing, broad-runtime, model-quality, or evidence-model-promotion claims.

A stop condition means the operator should not keep retrying casually. Preserve the artifact only if review, import, final-decision, or follow-up planning requires it.
