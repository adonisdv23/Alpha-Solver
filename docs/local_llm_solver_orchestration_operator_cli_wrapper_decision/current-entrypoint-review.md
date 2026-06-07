# Current Entrypoint Review

## Current local orchestration entry point

The current Level 2 local LLM solver orchestration entry point is the Python/module function:

```text
alpha.local_llm.orchestration_runner.run_local_llm_solver_orchestration
```

The runner module describes itself as non-production and internal/CLI-callable only. It states that it is not imported by `/v1/solve` or dashboard preview routes, reuses the approved local LLM runtime config/backend path, performs a bounded two-pass local expert flow, and preserves the non-evidence local runtime boundary.

## Current behavior shape

The function accepts a user prompt and optional local runtime configuration/testing seams, then calls `run_configured_local_llm_runtime` as its only runtime call path. With no explicit local opt-in, non-loopback endpoints, provider keys, or invalid timeouts, the function fails closed before exposing an answer.

The normalized result includes local-only metadata and top-level safety flags including `behavior_evidence=false`, `no_hosted_fallback=true`, and `no_provider_keys_required=true`.

## Existing operator guidance surface

The current operator guide documents a heredoc-based Python template that imports `run_local_llm_solver_orchestration` and prints JSON. The guide explicitly says not to invent a CLI name for this path because a stable operator-facing CLI wrapper is not yet provided.

## Existing general CLI/script surfaces

The repository contains other CLI surfaces, including portable/reference entry points and general Alpha CLI modules. Those surfaces are not current authorization to expose this local solver orchestration path. This decision packet does not repurpose existing production, dashboard, portable, reference, or general solver CLI paths.

## Current status conclusion

Current entrypoint status: `MODULE_ENTRYPOINT_ONLY`.

The current Python/module entry point is sufficient for tests and advanced developer inspection, but it is not a stable operator-facing CLI. A future wrapper can be justified if it remains narrow, local-only, default-off, and mechanically bound to the same safety invariants already enforced by the module path.
