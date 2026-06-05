# Implementation Preservation Checklist

- [x] Canonical spec `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md` was inspected.
- [x] `.specs/INDEX.md` includes the canonical spec.
- [x] Local LLM runtime mode remains optional and default-off.
- [x] Explicit operator opt-in is required.
- [x] Only localhost / loopback endpoints are accepted.
- [x] Exact local model name is required.
- [x] Finite timeout is required.
- [x] Provider keys are rejected for local LLM runtime mode.
- [x] No hosted-provider fallback is implemented.
- [x] Provenance distinguishes local LLM runtime output from hosted output.
- [x] `behavior_evidence=false` is preserved.
- [x] Existing default runtime behavior remains unchanged when local LLM mode is not configured.
- [x] `/v1/solve` remains blocked from local LLM runtime mode.
- [x] Dashboard preview remains blocked from local LLM runtime mode.
- [x] Tests use mocked/injected transports only.
