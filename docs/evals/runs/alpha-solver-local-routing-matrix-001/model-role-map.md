# Model Role Map

Candidate roles are local-only experiment roles. Families are mapped as candidates from the prior catalog without claiming performance, reliability, safety, or superiority.

| Role | Purpose | Candidate model families | Rejected or secondary families | Evidence needed before behavior use | Non-claim |
| --- | --- | --- | --- | --- | --- |
| Router | Classify task category and choose a route with explanations. | Llama, Qwen, Mistral/Nemo | Embedding models alone; coder-only variants as default router | Frozen routing task bank, expected route labels, rejected-route rationale, misroute log. | Does not prove routing works. |
| First-pass solver | Produce an initial answer or plan for non-blocked tasks. | Llama, Qwen, Gemma, Mistral/Nemo, Hermes | Embedding models; judge-only use of reasoning models | Prompt/output logs, category fit, non-echo checks, task-specific rubric. | Does not prove answer quality. |
| Critic | Identify gaps, contradictions, hallucination risk, or weak reasoning. | DeepSeek-R1 related, Hermes, Qwen, Qwen Coder | Embedding models; lightweight summarizers as sole critic | Paired first-pass/critique artifacts, calibrated flags, human-reviewed samples. | Does not prove judge reliability. |
| Safety reviewer | Check boundary, privacy, refusal, and evidence-overclaim risks. | Gemma, Llama, Qwen | Embedding models; coder-only route as primary safety reviewer | Gold boundary prompts, expected labels, fail-closed handling. | Does not validate safety. |
| Code reviewer | Inspect code-oriented outputs for repo-fit and testability. | Qwen Coder, Qwen, DeepSeek-R1 related, Llama | General summarizer-only role | Code task prompts, patch plans, test expectations, human code review. | Does not prove code correctness. |
| Judge candidate | Score or compare local-only outputs under a rubric. | DeepSeek-R1 related, Hermes, Qwen | Same family as tested output when avoidable; embedding models | Blind calibration set, tie rules, human adjudication, bias checks. | Does not establish benchmark validity. |
| Final synthesizer | Merge solver, critic, safety, and evidence notes into user-facing output. | Llama, Qwen, Gemma, Mistral/Nemo, Hermes | Embedding models; narrow coder model for non-code synthesis | Source-linked synthesis checks, claim-preservation review, final non-claims. | Does not prove final-answer superiority. |
