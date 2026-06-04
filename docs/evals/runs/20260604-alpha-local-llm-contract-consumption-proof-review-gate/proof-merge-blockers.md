# Proof Merge Blockers

Any item below blocks merge of the future
`ALPHA-LOCAL-LLM-CONTRACT-CONSUMPTION-PROOF-001` PR.

- The PR makes real model calls.
- The PR calls Ollama.
- The PR calls hosted providers or provider adapters.
- The PR implements a full Ollama adapter.
- The PR overloads `MODEL_PROVIDER=local` beyond its existing smoke-only role.
- The PR silently falls back to `alpha-solver-v91-python.py`.
- The PR silently falls back to `_tree_of_thought`.
- The PR omits the prompt source path.
- The PR omits the prompt fingerprint.
- The PR records a fingerprint that is not checked against the loaded portable
  contract.
- The PR lacks tests proving portable contract consumption.
- The PR lacks tests for fail-closed behavior.
- The PR makes behavior, evaluation, validation, quality, superiority, or
  readiness claims based on fake-client evidence.
- The PR executes operator tests.
- The PR imports operator-test results.
- The PR starts or modifies Batch C materials.
- The PR makes `/v1/solve` readiness claims.
- The PR makes production, MVP, product-readiness, or Alpha-quality claims.
