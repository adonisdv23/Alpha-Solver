# Operator Feedback Trace

Lane ID: `ALPHA-PORTABLE-CONTRACT-FOLLOWUP-REFINEMENT-001`

## Upstream packets reviewed

- Results import: `docs/evals/runs/20260604-alpha-limited-operator-test-prompt-contract-simulation-results-import-clean/`
- Interpretation: `docs/evals/runs/20260604-alpha-limited-operator-test-interpretation/`
- Post-results decision: `docs/evals/runs/20260604-alpha-limited-operator-test-post-results-decision/`
- Decision framework: `docs/evals/runs/20260604-alpha-limited-operator-test-post-results-decision-framework/`

## Trace to the selected defect family

The interpretation packet summarized the main recurring defect as output-format contamination in manual prompt-contract simulation outputs. The task-family observations specifically connected the issue to rewrite, template, reviewer-comment, and checklist-style prompts.

The post-results decision packet selected targeted portable-contract refinement as the narrow next lane because the recurring defect was answer-shape and wrapper contamination, not a broad evidence-boundary or claim-boundary failure.

## Contract response

The refinement maps each feedback theme to a portable-contract instruction:

| Feedback theme | Contract response |
| --- | --- |
| Process-style text before the requested answer | Require concise low-headroom answers to start with the requested artifact itself. |
| Wrapper labels around usable content | Suppress labels unless the user explicitly requests the wrapper. |
| `standard:` artifact | Suppress accidental literal-label artifacts unless that literal label is requested. |
| Concise reviewer-comment mismatch | Start with the reviewer comment text and avoid memo framing. |
| Replacement wording mismatch | Start with replacement wording, not `Replacement:` or a drafting note. |
| Checklist mismatch | Start with checklist bullets. |
| Compact template mismatch | Start with the template or prompt body. |

## Scope guard

This trace does not alter imported ratings, notes, severity labels, stop-condition status, arithmetic totals, source evidence, interpretation text, or post-results decision text.
