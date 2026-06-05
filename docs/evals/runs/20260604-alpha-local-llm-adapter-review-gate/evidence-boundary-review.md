# Evidence Boundary Review

## Allowed use

This docs-only gate may be cited only for adapter-wiring review. Specifically,
it may support the statement that the PR #290 seam was reviewed for portable
contract loading, prompt-source metadata preservation, user/system separation,
injected-backend isolation, non-evidence labeling, mode separation, fail-closed
handling, and fallback exclusion.

## Disallowed use

This gate must not be cited as evidence for:

- local LLM behavior;
- Ollama behavior;
- hosted-provider execution;
- `/v1/solve` readiness;
- dashboard preview readiness;
- runtime readiness;
- MVP validation;
- production readiness;
- Alpha quality;
- Alpha comparative-superiority;
- broad plain-provider inferiority;
- Batch C readiness;
- benchmark success;
- exact billing evidence;
- provider orchestration.

## Safe wording

Use wording such as:

- "The PR #290 seam remains adapter-wiring review only."
- "The reviewed tests use injected stub/fake backends and produce non-evidence
  wiring results."
- "The next lane may plan provider integration requirements, but must not
  execute a provider."

## Unsafe wording

Avoid wording that implies model execution, runtime readiness, benchmark
success, provider orchestration, provider comparison, Alpha quality, or operator
outcome interpretation.
