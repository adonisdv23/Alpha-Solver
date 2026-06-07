# Quick Start

## Minimal local prerequisites

- A local Mac or local developer machine.
- Ollama installed and running on a loopback endpoint such as `http://127.0.0.1:11434/api/chat`.
- A local model available, for example `qwen2.5:3b`.
- No hosted provider keys configured for this path.
- An explicit finite timeout.

## High-level sequence

1. Ensure Ollama is running locally.
2. Confirm the intended model exists locally.
3. Run a local orchestration command through the current Python/module entry point, because a stable operator-facing CLI wrapper is not yet provided.
4. Inspect result fields: `status`, `mode`, `answer`, `final_answer`, `considerations`, `assumptions`, `confidence`, `metadata`, `metadata.gate_trace`, `behavior_evidence=false`, `no_hosted_fallback=true`, and `no_provider_keys_required=true`.
5. Do not treat any output as production output, benchmark evidence, readiness evidence, local model quality evidence, provider orchestration evidence, Alpha superiority evidence, or evidence-model promotion.

Do not use this guide to expose local orchestration through production API or dashboard surfaces. This guide intentionally contains no production API or dashboard command path.
