# Proof Review Checklist

Use this checklist when reviewing the future
`ALPHA-LOCAL-LLM-CONTRACT-CONSUMPTION-PROOF-001` PR.

## Required Proof Shape

- [ ] The proof loads `alpha_solver_portable.py` as the prompt source.
- [ ] The proof records the prompt source path in explicit metadata.
- [ ] The proof records a deterministic prompt fingerprint in explicit metadata.
- [ ] The proof verifies the fingerprint against the exact loaded prompt source.
- [ ] The proof constructs a fake-client local-LLM-style request.
- [ ] The proof keeps system or instruction content separate from the user prompt.
- [ ] The proof labels fake-client evidence as non-behavior evidence.
- [ ] The proof avoids generated model outputs and uses fake-client output only.

## Forbidden Execution Paths

- [ ] The proof does not call Ollama.
- [ ] The proof does not call hosted providers or provider adapters.
- [ ] The proof does not call `_tree_of_thought`.
- [ ] The proof does not use `alpha-solver-v91-python.py` for generation.
- [ ] The proof does not overload `MODEL_PROVIDER=local`; existing local-provider
      behavior remains smoke-only.
- [ ] The proof does not route through `/v1/solve` as runtime readiness evidence.

## Failure Behavior

- [ ] The proof fails closed on a missing portable contract.
- [ ] The proof fails closed on a hash or fingerprint mismatch.
- [ ] The proof fails closed on empty fake-client output.
- [ ] The proof fails closed on prompt echo.
- [ ] The proof fails closed on fake-client error.
- [ ] The proof does not silently fall back to v91, `_tree_of_thought`, Ollama,
      hosted providers, or any runtime generation path.

## Tests and Claims

- [ ] Focused tests prove portable contract loading, fingerprint preservation,
      fake-client request construction, separation of instruction content from
      user prompt, and fail-closed behavior.
- [ ] Test names clearly describe contract-consumption proof behavior.
- [ ] Docs and test assertions avoid runtime readiness claims.
- [ ] Docs and test assertions avoid Alpha quality, validation, superiority,
      product readiness, MVP, and production claims.
- [ ] No operator tests are executed or imported.
- [ ] No Batch C files or materials are changed.
