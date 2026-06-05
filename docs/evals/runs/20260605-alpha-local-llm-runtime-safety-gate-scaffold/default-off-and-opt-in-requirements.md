# Default-Off and Opt-In Requirements

Lane: `ALPHA-LOCAL-LLM-RUNTIME-SAFETY-GATE-SCAFFOLD-001`

This is a scaffold only. Local LLM runtime integration is not implemented here.

## Default-off requirement

Local LLM runtime use must be default-off. No future implementation may enable local LLM runtime routing implicitly, by detection alone, or as a side effect of installing local model software.

## Explicit opt-in requirement

Future implementation must require explicit operator configuration before local LLM mode can be considered. The opt-in must be distinguishable from hosted provider configuration and must not reuse provider-key presence as an enablement signal.

## Provider-key isolation

Local LLM mode must not require, load, expose, or depend on hosted provider keys. Provider keys must not be used as fallback credentials for local LLM mode.
