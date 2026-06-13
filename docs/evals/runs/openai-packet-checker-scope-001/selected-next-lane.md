# Selected Next Lane

Selected next lane: `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-001`

Rationale: checker scope is extended to include OpenAI evidence packets, so the next provider-smoke lane should use the retry lane rather than the original `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001`, which already recorded a blocked missing-attestation attempt.
