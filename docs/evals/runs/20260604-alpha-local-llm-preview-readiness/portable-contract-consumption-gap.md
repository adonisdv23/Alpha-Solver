# Portable Contract Consumption Gap

Lane ID: `ALPHA-LOCAL-LLM-PREVIEW-READINESS-001`

Status: gap analysis only; no runtime execution performed.

## Current consumption status

Current runtime and preview paths do not prove consumption of `alpha_solver_portable.py`.

- `/dashboard/expert-preview` calls `service.app.solve()` for both panes.
- `/v1/solve` calls either the OpenAI provider path or the deterministic local/offline path.
- The deterministic local/offline path calls `_tree_of_thought()` from `alpha_solver_entry.py`, which loads `alpha-solver-v91-python.py`.
- The OpenAI provider path can accept a request `system` field, but no reviewed wiring automatically loads `alpha_solver_portable.py` into that field.

Therefore current product/runtime outputs should not be trusted as portable-contract evidence.

## Gap preventing product/runtime trust

The gap is not merely that a model is missing. The gap is that there is no proved source-to-runtime binding between the intended portable behavior contract and the prompt/runtime path. A future product/runtime result would need to show that:

1. the exact portable contract source was selected intentionally;
2. the contract content or approved transformation was injected into the local LLM request;
3. the request did not silently fall back to v91 `_tree_of_thought`, `react_lite`, or smoke-only local behavior;
4. the result metadata preserved prompt source, prompt version/hash, backend, model, route, and environment;
5. failure modes fail closed instead of returning prompt echoes as behavior evidence.

## Where the contract should be loaded

The cleanest future design is a small contract-loader/wrapper that reads `alpha_solver_portable.py` as the source-of-truth prompt artifact, extracts or preserves the intended system-prompt content, computes a stable fingerprint, and passes that prompt through `ProviderRequest.system` or an equivalent local-LLM request field. The wrapper should be used only by the explicit local LLM path, not by the existing `MODEL_PROVIDER=local` smoke path.

Importing runtime functions from `alpha_solver_portable.py` is less desirable for this preview use case because the stated contract is that the file is a portable prompt/spec monolith. Direct file-content consumption with a hash is easier to audit than importing constants unless the repo later creates a dedicated exported constant for the portable prompt.

## Drift prevention

A future lane should prevent silent drift back to v91 or deterministic paths by:

- using a distinct provider value such as `MODEL_PROVIDER=local_llm`;
- requiring tests that monkeypatch `_tree_of_thought` to fail if called during local LLM provider requests;
- requiring tests that monkeypatch the local LLM client to assert the exact system prompt or prompt hash;
- recording prompt source path and hash in safe metadata;
- failing closed if the portable contract cannot be read;
- preserving `MODEL_PROVIDER=local` as smoke-only deterministic behavior.

## Tests that would prove the gap is closed

A future implementation lane should add focused tests such as:

- **Contract load test:** verifies the local LLM path reads `alpha_solver_portable.py` and computes a stable prompt-source hash.
- **Request injection test:** uses a fake local LLM client and asserts the system prompt includes the portable activation/protocol content or approved transformed equivalent.
- **No-v91 fallback test:** monkeypatches `service.app._tree_of_thought` to raise and verifies `MODEL_PROVIDER=local_llm` does not call it.
- **Smoke isolation test:** verifies `MODEL_PROVIDER=local` still uses the deterministic local/offline smoke path and does not call the local LLM client.
- **Metadata test:** verifies safe response metadata includes provider/backend, model, prompt source, prompt hash, route, and local-only configuration label.
- **Failure test:** verifies missing local backend, timeout, empty answer, missing contract, or prompt-echo detection produces a SAFE-OUT-like failure or explicit non-evidence label rather than behavior evidence.
