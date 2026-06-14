# Task Category Map

These categories are routing labels for future local-only experiments. They are not performance claims and are not exhaustive product taxonomies.

| Task category | Local routing intent | Primary canonical role IDs | Typical signal | What correct routing should preserve |
| --- | --- | --- | --- | --- |
| Coding | Code explanation, patch planning, tests, or review. | `router`, `code_reviewer`, `first_pass_solver`, `critic`, `final_synthesizer` | File paths, stack traces, test commands, implementation constraints. | Repo instructions, scoped changes, testability, no broad refactors. |
| False premise | User asks from an inaccurate or unverifiable premise. | `router`, `critic`, `final_synthesizer` | Named facts that may not exist, contradicted dates, impossible source claims. | Calibrated correction, uncertainty, no fabricated details. |
| Hidden constraints | User request omits requirements that materially affect answer. | `router`, `planner`, `first_pass_solver`, `final_synthesizer` | Ambiguous audience, environment, scope, risk tolerance, missing data. | Clarifying questions or explicit assumptions. |
| Safety/boundary | Request may require refusal, limitation, privacy protection, or policy boundary. | `router`, `safety_boundary_reviewer`, `final_synthesizer` | Sensitive data, unsafe instructions, credential/API-token requests, private-data leakage risk. | Safe completion, refusal where needed, no unsafe operational details. |
| Summarization | Compress or restate existing content. | `router`, `first_pass_summarizer`, `critic`, `final_synthesizer` | Long source text, docs, run artifacts, transcripts. | Fidelity, no new claims, boundaries retained. |
| Strategy | High-level decision framing, roadmap, go/no-go analysis. | `router`, `first_pass_solver`, `critic`, `final_synthesizer` | Goals, tradeoffs, milestones, uncertainty, operator decisions. | Options and criteria without unsupported recommendations. |
| Evidence audit | Check whether claims are supported by artifacts. | `router`, `evidence_audit_critic`, `final_synthesizer` | Claims, citations, logs, verdicts, evidence packets. | Source-grounded findings, explicit gaps, no overclaiming. |
| Planning | Break work into steps before execution. | `router`, `planner`, `critic`, `final_synthesizer` | Requested lane, implementation scope, validation requirements. | Sequencing, dependencies, stop conditions. |
| Synthesis | Combine multiple artifacts into one coherent output. | `router`, `final_synthesizer`, `critic` | Several docs or result packets, need for final narrative. | Traceable claims, caveats, consistent terminology. |
| Classification | Label task, risk, route, status, or verdict. | `router`, `classifier`, `final_synthesizer` | Short prompt requiring categories or labels. | Deterministic label set, uncertainty when ambiguous. |
