# In-Scope MVP

Lane: `ALPHA-SOLVER-POST-LEVEL-7-SELF-OPERATOR-MVP-SCOPE-MATRIX-PACKET-001`

## Narrow MVP definition

The earliest safe Self Operator MVP may include only operator-supervised task execution design that stays local, reviewable, reversible before external action, and stopped by default when authority or evidence is unclear.

## Scope matrix

| Area | In-scope MVP definition | Required safety boundary |
| --- | --- | --- |
| Task intake | Operator-provided task descriptions, acceptance criteria, and local artifact targets. | No autonomous discovery of external work, secrets, deployments, billing, or production changes. |
| Plan drafting | Local draft plans, checklists, and task breakdowns for operator review. | Plans are suggestions only until explicitly approved by the operator. |
| Confirmation gates | Explicit operator confirmation before every material transition, especially file write proposal, test execution, evidence labeling, or handoff recommendation. | Missing, ambiguous, stale, or conflicting confirmation must stop the flow. |
| Local artifact generation | Docs, reports, matrices, checklists, run notes, and other local files approved by the operator. | Artifacts must stay local and must not claim runtime, provider, production, billing, or deployment readiness. |
| Traceability | Local trace notes linking task input, operator confirmations, generated artifacts, checks, stop states, and unresolved blockers. | Traceability must use references and summaries, not secrets or unredacted payloads. |
| Stop states | Clearly named stop states for missing approval, unclear scope, missing dependency, unsafe external action, secret risk, provider/routing ambiguity, failed check, or evidence-boundary conflict. | Stop states require operator review before continuation. |
| Operator handoff | A final packet summary that tells the operator what was drafted, what was not done, checks run, blockers, and next action state. | The MVP does not perform the handoff action outside the repo or local artifact context. |

## Minimum MVP behavior principles

- The Self Operator MVP is assistive, not autonomous.
- The operator remains the authority for scope, approval, credentials, external action, merge, deploy, billing, and evidence promotion decisions.
- Every generated artifact must be locally inspectable before any downstream use.
- Every uncertain state must prefer stop over inference.
- Provider, browser, dashboard, API, billing, deployment, and credential behavior is excluded unless a later accepted lane explicitly authorizes it.
