# Evidence Boundary

## Allowed evidence

This lane may be cited only as evidence that the local LLM provider-adapter seam
can build and hand off a request in offline stub tests while preserving prompt
source metadata.

## Non-claims

This lane must not be cited as evidence of:

- local LLM behavior;
- Ollama behavior;
- hosted provider behavior;
- `/v1/solve` readiness;
- dashboard preview readiness;
- runtime readiness;
- MVP validation;
- production readiness;
- Alpha quality;
- Alpha superiority;
- broad plain-provider inferiority;
- Batch C readiness;
- benchmark success;
- exact billing accuracy;
- provider orchestration.

## Boundary wording

Safe wording: "The lane proves adapter wiring only with an offline stub backend."

Unsafe wording: any statement that treats stub output as model behavior,
readiness, validation, or provider execution evidence.
