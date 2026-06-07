# Non-Actions and Blocked Uses

This docs-only guardrail runbook does not authorize or perform any of the following actions:

- local model inference;
- Ollama execution;
- smoke execution;
- hosted provider calls;
- `/v1/solve` exposure or calls;
- dashboard route exposure or calls;
- local LLM provider adapter behavior changes;
- operator CLI behavior changes;
- provider fallback;
- hosted fallback;
- benchmark execution;
- billing work;
- evidence promotion;
- Google Sheets updates;
- backlog workbook updates; or
- the roadmap-selected release-readiness ladder track.

## Blocked claim boundary

The following terms remain blocked non-claims in this runbook: production readiness, MVP readiness, benchmark evidence, local model quality evidence, provider-orchestration evidence, provider orchestration evidence, Alpha superiority, billing evidence, dashboard readiness, `/v1/solve` readiness, broad runtime readiness, evidence-model promotion, provider fallback readiness, and hosted fallback readiness.

Do not fix checker failures by moving claims into logs or `checks-run.md`. Do not infer missing packet fields from memory. Do not weaken checker scripts or tests to make this runbook pass.
