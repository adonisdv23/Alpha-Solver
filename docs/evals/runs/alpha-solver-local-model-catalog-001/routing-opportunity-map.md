# Routing Opportunity Map

## Opportunities

| Opportunity | Candidate families | What a future harness should test | Evidence needed before use |
| --- | --- | --- | --- |
| General answer path | Llama, Qwen, Gemma, Mistral/Nemo, Hermes | Single prompt, normalized output, failure handling. | Prompt transcript, model identifier, endpoint validation, timeout, output capture, non-echo checks. |
| Code-focused path | Qwen Coder, Llama, DeepSeek-R1 related | Code explanation or patch-planning prompts only. | Reproducible local logs and reviewer assessment criteria. |
| Critic/reviewer path | DeepSeek-R1 related, Hermes, Qwen Coder, Llama | Second-pass critique of another local output. | Paired input/output logs and documented disagreement handling. |
| Boundary-check path | Gemma, Llama, Qwen | Classify blocked claims or unsafe requests. | Gold prompts and expected labels; model output alone is not safety validation. |
| Summarizer path | Llama, Qwen, Gemma, Mistral/Nemo | Compress operator artifacts without changing claims. | Diffable summaries and boundary-preservation checks. |
| Judge candidate path | DeepSeek-R1 related, Hermes, Qwen | Rank or label outputs for local-only experiments. | Calibration set, blind labels, tie handling, and audit logs. |
| Router candidate path | Llama, Qwen, Mistral/Nemo | Choose a model family based on prompt type. | Ground-truth routing set and explicit misroute handling. |
| Retrieval support | nomic-embed-text, mxbai-embed-large | Local embedding generation and retrieval lookup. | Separate embedding endpoint support, corpus version, retrieval metrics, and privacy boundary review. |

## Not yet implemented

This packet recommends a future local multi-model smoke harness. It does not implement routing, retrieval, model selection, dashboard exposure, or `/v1/solve` exposure.
