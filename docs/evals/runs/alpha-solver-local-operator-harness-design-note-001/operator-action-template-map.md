# Operator Action Template Map

This is a paper-only map from repo prompt packets to possible named local operator actions. It defines names and review intent only. It does not create executable automation.

| Example local action name | Prompt/source packet | Intended operator use | Required boundary before use |
| --- | --- | --- | --- |
| `open-current-state-context` | `docs/CURRENT_STATE.md` | Review the current selected lane, blocked activities, and non-claims. | Inspect-only docs review. |
| `open-lane-registry-context` | `docs/LANE_REGISTRY.md` | Confirm lifecycle status and avoid reopening superseded or blocked lanes. | Inspect-only docs review. |
| `open-evidence-ledger-context` | `docs/EVIDENCE_INDEX.md` | Check what existing artifacts can and cannot support. | Inspect-only docs review. |
| `review-pi-patterns-only-note` | `docs/evals/runs/alpha-solver-pi-dev-harness-feasibility-018/README.md` | Extract safe high-level patterns without integration. | No Pi.dev install, run, dependency, or code copy. |
| `record-local-harness-design-note` | This packet | Draft Alpha-native design artifacts and boundaries. | Docs-only writing; no runtime change. |
| `prepare-value-read-authorization-return` | `docs/evals/runs/alpha-solver-value-read-simulation-packet-refresh-post-565-001/manual-run-artifact-2026-06-15.md` | Return to Value Read authorization only if the operator wants value evidence next. | Separate explicit execution authorization required. |
| `review-local-ollama-blocked-attempt` | `docs/evals/runs/alpha-solver-local-model-lab-ollama-singlepath-001/local-run-artifact-2026-06-15.md` | Preserve failed-closed local-run lessons without rerunning or changing model behavior. | No model call, pull, install, timeout extension, or rerun unless separately authorized. |
| `draft-message-card` | `.specs/ALPHA-SOLVER-CALIBRATED-CONFIDENCE-OUTPUT-CONTRACT-001.md` and this packet | Sketch an evidence card with answerability, confidence, assumptions, and non-claims. | Paper-only UI/spec; no runtime UI. |
| `apply-needs-human-boundary` | `.specs/ALPHA-SOLVER-ESCALATION-NEEDS-HUMAN-PROTOCOL-001.md` | Mark a task as needs-human when scope or risk requires escalation. | No autonomous continuation past escalation. |
| `lint-narrative-claims` | `scripts/check_narrative_claim_safety.py` | Run static claim-safety lint on docs artifacts. | Static lint only; not completeness or readiness evidence. |

## Naming convention

Future local action names should be short imperative labels:

- start with a verb: `open`, `review`, `record`, `prepare`, `draft`, `apply`, `lint`;
- name the evidence source or decision boundary;
- avoid names that imply execution unless execution is separately authorized;
- avoid names that imply provider/model/runtime behavior.

## Explicit non-automation boundary

This map does not add commands, scripts, configs, packages, routes, dashboard components, model calls, provider calls, or MCP tools. It is a vocabulary for future human/operator review only.
