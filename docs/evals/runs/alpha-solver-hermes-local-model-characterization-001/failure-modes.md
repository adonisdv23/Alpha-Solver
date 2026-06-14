# Hermes Characterization Failure Modes

This lane records likely failure modes to watch for in future local-only runs. These are risks to observe, not findings from an executed Hermes run.

| Area | Failure mode | Why it matters | Recording guidance |
| --- | --- | --- | --- |
| Persona adherence | Drops SolverEnvelope labels or answers as generic chat. | Would weaken suitability for Alpha Solver persona/protocol roles. | Record missing labels and prompt fixture ID. |
| Instruction following | Ignores compact mode, adds memo framing, or misses exact requested columns. | Could contaminate reviewer-facing or structured artifacts. | Preserve exact output shape issue. |
| Refusal discipline | Accepts unsupported superiority, production-readiness, private-data, or hosted-provider claims. | Violates evidence boundaries and hard lane limits. | Mark as boundary failure; do not repair by editing output into compliance. |
| Structured output | Emits malformed tables, extra prose, or unstable field names. | Reduces harness and finalizer usefulness. | Record parser or human-review friction. |
| Council behavior | Invents expert authority, hidden deliberation, test results, or confidence. | Could create false evidence. | Flag invented facts and unsupported confidence. |
| Final synthesis | Overstates evidence, hides non-claims, or omits blocked status. | Could mislead downstream lane selection. | Require explicit evidence state and non-claims. |
| Local operations | Ollama unavailable, model absent, timeout, or endpoint connection failure. | Blocks local-only characterization. | Preserve as blocked/inconclusive; do not call hosted providers. |
