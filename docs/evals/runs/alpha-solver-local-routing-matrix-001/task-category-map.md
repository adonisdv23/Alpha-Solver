# Task Category Map

These categories are routing labels for future local-only experiments. They are not performance claims and are not exhaustive product taxonomies.

| Task category | Local routing intent | Typical signal | What correct routing should preserve |
| --- | --- | --- | --- |
| Coding | Code explanation, patch planning, tests, or review. | File paths, stack traces, test commands, implementation constraints. | Repo instructions, scoped changes, testability, no broad refactors. |
| False premise | User asks from an inaccurate or unverifiable premise. | Named facts that may not exist, contradicted dates, impossible source claims. | Calibrated correction, uncertainty, no fabricated details. |
| Hidden constraints | User request omits requirements that materially affect answer. | Ambiguous audience, environment, scope, risk tolerance, missing data. | Clarifying questions or explicit assumptions. |
| Safety/boundary | Request may require refusal, limitation, privacy protection, or policy boundary. | Sensitive data, unsafe instructions, credential/API-token requests, private-data leakage risk. | Safe completion, refusal where needed, no unsafe operational details. |
| Summarization | Compress or restate existing content. | Long source text, docs, run artifacts, transcripts. | Fidelity, no new claims, boundaries retained. |
| Strategy | High-level decision framing, roadmap, go/no-go analysis. | Goals, tradeoffs, milestones, uncertainty, operator decisions. | Options and criteria without unsupported recommendations. |
| Evidence audit | Check whether claims are supported by artifacts. | Claims, citations, logs, verdicts, evidence packets. | Source-grounded findings, explicit gaps, no overclaiming. |
| Planning | Break work into steps before execution. | Requested lane, implementation scope, validation requirements. | Sequencing, dependencies, stop conditions. |
| Synthesis | Combine multiple artifacts into one coherent output. | Several docs or result packets, need for final narrative. | Traceable claims, caveats, consistent terminology. |
| Classification | Label task, risk, route, status, or verdict. | Short prompt requiring categories or labels. | Deterministic label set, uncertainty when ambiguous. |
