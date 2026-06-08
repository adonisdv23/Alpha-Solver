# Stop Conditions

Lane: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-7-PROVIDER-ORCHESTRATION-DESIGN-PACKET-001`

Stop and use the blocker fallback lane if any of the following occurs:

- The accepted Level 6 product-surface design packet is missing.
- This packet modifies files outside `docs/evals/runs/alpha-solver-post-level-3-level-7-provider-orchestration-design/`.
- Runtime code, provider adapters, API files, dashboard files, CLI behavior, checker scripts, tests, `Makefile`, workflows, or source-artifact files would change.
- The packet claims that Level 6 support references are accepted evidence without citing a specific accepted decision file.
- The packet enables provider routing, provider fallback, hosted fallback, credential configuration, provider calls, `/v1/solve`, dashboard routes, local model inference, hosted model inference, Ollama, benchmarks, billing, external ledger updates, or evidence promotion.
- More than one next lane is selected.
- Level 8 is described as started rather than deferred.
