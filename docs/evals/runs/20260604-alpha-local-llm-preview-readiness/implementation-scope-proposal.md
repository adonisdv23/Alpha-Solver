# Future Implementation Scope Proposal

Lane ID: `ALPHA-LOCAL-LLM-PREVIEW-READINESS-001`

Status: proposal only; not implemented.

## Recommended future lane name

Recommended lane: `ALPHA-LOCAL-LLM-PROVIDER-ADAPTER-001`.

This name is preferred over `ALPHA-LOCAL-LLM-PREVIEW-IMPLEMENTATION-001` because the first missing capability is not the UI preview itself; it is a clean local LLM provider/adapter seam that consumes the portable contract without overloading `MODEL_PROVIDER=local`. It is also more specific than `ALPHA-LIMITED-OPERATOR-TEST-SURFACE-FIX-001`, which is broader and should remain optional for product/runtime operator evidence.

## Files likely to touch in that future lane

A future implementation lane might need to modify or add files in these areas:

- provider contract/client files under `alpha/providers/`;
- provider selection in `service/app.py`;
- model-set/config validation in `service/models/modelset_registry.py` and `service/config/model_sets.yaml`;
- environment examples/checks such as `.env.example` and `scripts/check_env.py` if local LLM config becomes supported;
- a new portable-contract loader/wrapper module;
- focused tests under `tests/` for provider selection, contract loading, fake local LLM execution, failure modes, and smoke isolation;
- possibly `alpha/webapp/routes/expert_preview.py` only if the approved surface is the dashboard preview.

This readiness spike did not modify any of those files.

## Tests likely needed

- Unit test for portable-contract loader and hash/fingerprint metadata.
- Unit test for local LLM provider request/response parsing using a fake client or fake transport.
- Test that `MODEL_PROVIDER=local_llm` does not call `_tree_of_thought`.
- Test that `MODEL_PROVIDER=local` remains deterministic smoke/offline behavior and does not call the local LLM client.
- Test that missing local backend/model/contract produces safe failure and no behavior evidence label.
- Test that prompt echo or empty output is rejected or labeled non-evidence.
- Test that `/dashboard/expert-preview`, if included, clearly labels backend/model/prompt source and preserves local smoke behavior separately.
- Test that `/v1/solve`, if included, records safe metadata and does not expose raw provider payloads.

## Stop conditions

Stop the future lane if:

- the implementation cannot prove `alpha_solver_portable.py` or an approved transformed portable contract is consumed;
- `MODEL_PROVIDER=local` would need to be overloaded or broken;
- local LLM requests could silently fall back to v91 `_tree_of_thought`;
- provider/base URL config permits accidental non-local calls when local-only mode is required;
- raw provider payloads, secrets, or private environment details would be exposed;
- prompt echoes, empty answers, or parse failures cannot be failed closed or labeled non-evidence;
- tests require real Ollama, OpenAI, Anthropic, or other provider calls.

## Rollout guardrails

- Feature flag the local LLM path separately from `MODEL_PROVIDER=local`.
- Default to disabled.
- Require explicit local-only endpoint validation.
- Preserve backend/model/config/prompt-source metadata.
- Keep dashboard output labels evidence-bounded.
- Do not enable operator tests, Batch C, scoring, or product-readiness claims as part of the adapter lane.

## Minimum viable behavior

The minimum viable future behavior is a fake-client-tested path where an explicit local LLM provider value builds a request containing the portable contract as the system prompt or approved equivalent, sends it only through the local LLM adapter seam, returns a safe response shape, records safe metadata, and fails closed on missing contract/backend/empty output/prompt echo. Real Ollama execution can remain manual or deferred until explicitly authorized.

## Explicit non-goals

- No Alpha validation or superiority claims.
- No production readiness or broad runtime readiness claims.
- No Batch C work.
- No operator-test execution.
- No OpenAI/Anthropic provider calls.
- No exact billing claims.
- No provider orchestration claims.
- No replacement of the manual portable-contract simulation track.
