# Adapter Merge Blockers

These blockers must prevent any future local-provider integration lane from
proceeding past planning/review.

## Hard blockers

1. Any code change that wires the adapter into `/v1/solve`, dashboard preview,
   routing, runtime provider selection, or `MODEL_PROVIDER=local` without a
   separate approved implementation spec.
2. Any real provider call, including local model execution, Ollama execution,
   hosted-provider execution, or provider-key use.
3. Any path that treats stub/fake output as model-quality evidence, readiness
   evidence, benchmark evidence, billing evidence, orchestration evidence, or
   Alpha quality evidence.
4. Any loss of prompt-source path, SHA-256 fingerprint, SHA-256 alias, or
   fingerprint algorithm metadata.
5. Any merging of user prompt content into the portable contract/system content.
6. Any acceptance of `provider_mode="local"` as a substitute for the distinct
   `local_llm` adapter mode.
7. Any default backend that performs I/O or reaches a model server.
8. Any removal of injected-backend control from tests.
9. Any weakening of fail-closed handling for empty output, prompt echo, backend
   error, missing contract, empty contract, fingerprint mismatch, or empty user
   prompt.
10. Any use of v91 `_tree_of_thought` fallback as a substitute provider path.
11. Any modification of PR #288 or PR #289 evidence in the same lane.
12. Any Batch C, operator-test interpretation, benchmark-success, readiness, or
   superiority claim in the same lane.

## Current blocker status for this docs-only gate

No blockers were found for opening the next planning/review lane. This finding
is limited to adapter-wiring review and does not authorize provider execution.
