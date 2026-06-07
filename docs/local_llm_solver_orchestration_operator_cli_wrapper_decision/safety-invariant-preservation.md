# Safety Invariant Preservation

## Invariants preserved by the selected decision

The selected `ADD_STABLE_CLI_WRAPPER` decision preserves the Level 2 local LLM solver orchestration safety invariants by requiring any future wrapper to remain a thin local operator surface over the existing module entry point.

The selected path preserves:

- optional local LLM use;
- default-off behavior;
- explicit operator opt-in;
- localhost or loopback endpoint acceptance only;
- finite timeout use;
- no provider keys required or accepted for local mode;
- hosted-provider-key CLI flags disallowed;
- hosted-provider-key environment variables must not affect local wrapper behavior except through existing fail-closed rejection semantics;
- existing fail-closed provider-key rejection behavior must be preserved where applicable;
- no hosted fallback;
- no provider fallback;
- local failure visibility as fail-closed local failure;
- `behavior_evidence=false`;
- `no_hosted_fallback=true`;
- `no_provider_keys_required=true`;
- no production `/v1/solve` exposure;
- no dashboard exposure;
- no evidence-model promotion.

## Decision-safety reasoning

The future wrapper is permitted only as an invocation wrapper. It must not become a new solver implementation, a production route, a dashboard feature, a hosted provider path, a provider orchestration path, or an evidence promotion path.

The safest implementation direction is to keep validation and orchestration semantics in the existing `LocalLLMRuntimeConfig`, provider adapter, and `run_local_llm_solver_orchestration` call path, then add only enough CLI code to collect explicit operator input and print normalized JSON.
