# Evidence Boundary

## Allowed evidence

This lane may be cited only as evidence that a documentation catalog of local Ollama model family candidates was captured against the existing default-off local LLM adapter context.

## Required evidence before behavior use

Before any model family can be used as behavior evidence, a future lane must capture at minimum:

1. exact model identifier and, when available, model digest;
2. local endpoint URL after loopback validation;
3. timeout and host resource class;
4. prompt set and expected non-secret input boundaries;
5. raw response artifact or normalized response artifact;
6. fail-closed reason codes for blocked or failed calls;
7. statement that no hosted-provider token or fallback was used;
8. repeatability notes and operator environment constraints;
9. review criteria for each role such as coder, critic, judge, router, summarizer, or boundary checker.

## Non-claims

This lane does not claim local model behavior, local routing works, production readiness, provider readiness, benchmark validation, value evidence, Alpha superiority, paid-provider parity, hosted-provider fallback, dashboard readiness, `/v1/solve` readiness, or safety validation.

## Allowed verdict

`LOCAL_MODEL_CATALOG_CAPTURED`
