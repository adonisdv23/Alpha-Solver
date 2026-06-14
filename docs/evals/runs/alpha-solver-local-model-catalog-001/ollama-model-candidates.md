# Ollama Model Candidates

These entries are operator guidance examples for future local testing. Install commands are examples only and are not evidence that the model exists in the local environment, has been pulled, can run on the operator machine, or performs well. Operators should check the current Ollama library and local hardware before use.

| Family | Example Ollama names or pulls | Likely role candidates | Resource class | Notes |
| --- | --- | --- | --- | --- |
| Llama | `ollama pull llama3.2`, `ollama pull llama3.1`, `ollama pull llama3` | generalist, summarizer, critic, router candidate | small laptop to desktop/GPU depending on size | Useful baseline family for broad instruction following; behavior evidence requires controlled prompts and logged outputs. |
| Qwen | `ollama pull qwen2.5`, `ollama pull qwen3` | generalist, summarizer, critic, router candidate | small laptop to desktop/GPU depending on size | Candidate for multilingual/general reasoning trials; no performance claim in this packet. |
| Qwen Coder | `ollama pull qwen2.5-coder`, `ollama pull qwen3-coder` | coder, code critic, implementation reviewer | stronger laptop to desktop/GPU depending on size | Candidate for code-focused local smoke tasks; evidence requires scoped code prompts and deterministic logs. |
| DeepSeek-R1 related | `ollama pull deepseek-r1` | reasoning candidate, critic, judge candidate | stronger laptop to desktop/GPU; unknown for larger variants | Candidate for reasoning-style local comparison; outputs may require special parsing boundaries. |
| Gemma | `ollama pull gemma3`, `ollama pull gemma2` | generalist, summarizer, safety/boundary checker candidate | small laptop to desktop/GPU depending on size | Candidate for lightweight local checks; must not be treated as safety validation without test evidence. |
| Mistral / Nemo | `ollama pull mistral`, `ollama pull mistral-nemo` | generalist, summarizer, router candidate | stronger laptop to desktop/GPU depending on size | Candidate for concise local instruction following; availability varies by operator environment. |
| Hermes | `ollama pull hermes3`, `ollama pull nous-hermes2` | generalist, critic, judge candidate | stronger laptop to desktop/GPU depending on size | Candidate for instruction-tuned local review roles; no judge reliability is claimed. |
| Embedding models | `ollama pull nomic-embed-text`, `ollama pull mxbai-embed-large` | embedding/retrieval support | small laptop to stronger laptop depending on model | Future retrieval/routing support only; current adapter is chat-shaped and does not provide retrieval routing evidence. |
