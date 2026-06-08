# Stop conditions

Fallback review or execution must stop when:

- the accepted Level 7 provider orchestration design packet is missing;
- the requested change would add fallback behavior in this docs-only packet;
- the requested change would enable hosted fallback;
- the requested change would call providers;
- the requested change would configure credentials or secrets;
- the requested change would modify runtime, provider, API, dashboard, CLI, checker-script, workflow, test, Makefile, or source-artifact files;
- the requested change would expose or call `/v1/solve`;
- the requested change would run local models, hosted models, Ollama, benchmarks, or billing work;
- fallback authorization is ambiguous or outside the future authorized lane;
- required provenance, credential, cost, safety, or audit boundaries are missing;
- local-vs-hosted state is unclear;
- evidence is stale or promotional.

When a stop condition is met, the safe result is no fallback and fail-closed operator review.
