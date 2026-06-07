# Output Interpretation Guide

The local orchestration runner returns a normalized Alpha-style result. Treat the result as Level 2 local operator output only.

## Top-level fields

- `status`: The outcome category. Common values include `ok`, `clarify`, `blocked`, and `failed_closed`.
- `mode`: The selected gate mode. Expected modes are `direct`, `clarify`, `answer_with_assumptions`, or `block`.
- `answer`: The answer text exposed when the runner reaches a safe answer path. It may be empty for blocked or failed-closed outcomes.
- `final_answer`: The final operator-facing answer, clarification request, or empty blocked answer depending on outcome.
- `considerations`: Bounded Pass 1 considerations parsed from the local model output when safe to expose.
- `assumptions`: Bounded Pass 1 assumptions parsed from the local model output when safe to expose.
- `confidence`: Parsed bounded confidence when available. Missing, low, or unsafe confidence can lead to `clarify`, `block`, or `failed_closed`.
- `metadata`: Runtime and diagnostic metadata, including local provenance and `gate_trace`.

## Required boundary indicators

Every accepted local orchestration output must preserve:

- `behavior_evidence=false`: The output is not behavior evidence for promotion, readiness, benchmarks, or model quality.
- `no_hosted_fallback=true`: The local path did not silently substitute hosted-provider output.
- `no_provider_keys_required=true`: The local path does not require hosted provider keys.

## How to read outcomes

- `ok` with `direct` or `answer_with_assumptions`: A bounded local answer was produced. This is still non-production, non-benchmark, non-readiness output.
- `clarify`: The runner determined that missing or broad information prevents a safe direct answer. The operator should refine the prompt rather than force a result.
- `blocked`: The runner identified high-risk or policy/boundary conditions and intentionally withheld an answer.
- `failed_closed`: The runner stopped due to parsing, runtime, boundary, or safety failure. Treat the result as a protective stop, not as an answer.
