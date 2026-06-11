# Council seat matrix

| Seat | Prompt file | Primary focus |
| --- | --- | --- |
| Evidence Boundary Auditor | `prompts/01-evidence-boundary-auditor.md` | Audit claim boundaries and unsupported inference risks. |
| Repo Lineage Auditor | `prompts/02-repo-lineage-auditor.md` | Audit PR chain, lane continuity, and source evidence lineage. |
| Execution Integrity Auditor | `prompts/03-execution-integrity-auditor.md` | Audit command integrity, repeatability evidence, stop-state handling, and non-execution claims. |
| Security and Privacy Auditor | `prompts/04-security-privacy-auditor.md` | Audit secrets, redaction, private-path, billing, provider, and exposure boundaries. |
| Operator UX Auditor | `prompts/05-operator-ux-auditor.md` | Audit whether manual operator review would be usable and unambiguous. |
| Red Team Failure Mode Auditor | `prompts/06-red-team-failure-mode-auditor.md` | Audit hidden failure modes and ways evidence could be over-interpreted. |
| Product Value Auditor | `prompts/07-product-value-auditor.md` | Audit narrow operator value evidence without broad market or benchmark inferences. |
| Synthesis Judge | `prompts/08-synthesis-judge.md` | Consolidate findings after all seat outputs exist. |

All seats must use the common instructions in `prompts/00-common-instructions.md`.
