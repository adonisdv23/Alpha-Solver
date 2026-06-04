# Contract Consumption Proof

Lane ID: `ALPHA-LOCAL-LLM-CONTRACT-CONSUMPTION-PROOF-001`

## How `alpha_solver_portable.py` is loaded

The proof helper reads `alpha_solver_portable.py` from the repository root as
UTF-8 text. It treats the file contents as the prompt source rather than
importing runtime functions from the file. This preserves the intended portable
behavior contract as auditable prompt text.

The loader fails closed if the file is missing, cannot be read, is empty, or
does not match a caller-supplied expected SHA-256 fingerprint.

## Metadata preserved

The loaded contract records safe metadata:

- `prompt_source_path`: `alpha_solver_portable.py`
- `prompt_source_fingerprint`: the SHA-256 digest of the loaded file text
- `prompt_source_sha256`: the same SHA-256 digest, named explicitly
- `prompt_source_fingerprint_algorithm`: `sha256`

The fake request also records:

- `provider_mode`: `local_llm`
- `backend_class`: `fake-local-llm-proof`
- `no_real_provider_call`: `true`
- `behavior_evidence`: `false`
- `evidence_label`: `non_evidence_fake_client_contract_consumption_proof`

## How v91 / `_tree_of_thought` fallback is avoided

The proof seam lives in `alpha/local_llm/portable_contract.py` and is not wired
into `service.app.solve()`, `/v1/solve`, or `/dashboard/expert-preview`. It does
not import `alpha_solver_entry.py` and does not load `alpha-solver-v91-python.py`.
Its fake-client tests guard those imports and verify the proof path completes
without them.

The helper requires the distinct proof mode label `local_llm`. Passing `local`
is rejected so that the existing `MODEL_PROVIDER=local` smoke/offline path is not
overloaded or confused with local LLM behavior.

## Why no model behavior is claimed

The fake client records the constructed request and returns controlled fake text.
It never calls Ollama, OpenAI, Anthropic, or any provider. The proof result always
sets `behavior_evidence=false`; successful fake output is labeled only as a
request-construction and prompt-source-consumption proof. Empty output, prompt
echo, and fake-client failure fail closed as non-evidence conditions.
