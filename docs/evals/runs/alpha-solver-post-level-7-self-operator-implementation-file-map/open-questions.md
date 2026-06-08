# Open questions for future Self Operator MVP work

1. What exact Self Operator MVP behavior is authorized: command generation, local orchestration execution, packet creation assistance, guardrail running, artifact preservation, or another operator workflow?
2. Should the future surface be a new CLI, an extension of `alpha/local_llm/operator_cli.py`, an extension of existing repo CLI commands, or documentation-only operator workflow guidance?
3. Is Self Operator constrained to local-only non-production execution, or does any future lane require explicit hosted-provider integration?
4. What evidence model applies to Self Operator outputs, and must `behavior_evidence=false` remain mandatory?
5. Which artifact/output directories may Self Operator create, and what naming, redaction, and retention rules apply?
6. What stop conditions are required for credentials, remote endpoints, live provider calls, dashboard/API routes, and deployment surfaces?
7. Should the existing local LLM guardrail scripts be extended for Self Operator packets, or should a separate Self Operator guardrail script be created?
8. What minimal tests prove safe operator behavior without claiming model quality, production readiness, MVP readiness, or Alpha superiority?
9. Does CI need a new static guardrail target, or should future work reuse `check-local-llm-orchestration-guardrails`?
10. Are there any external backlog ledgers that must be updated outside the repo after implementation, and who owns those updates?
