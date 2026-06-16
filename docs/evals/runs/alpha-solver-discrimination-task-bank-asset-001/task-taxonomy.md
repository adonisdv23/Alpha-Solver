# Task Taxonomy

## Taxonomy goal

The task bank should test whether a solver can discriminate between answerable requests, requests with defective assumptions, requests that require refusal or stopping, requests needing calibrated uncertainty, and requests whose claims exceed available evidence.

## Families

| Family | Discrimination target | Expected high-level behavior |
| --- | --- | --- |
| False-premise | The prompt embeds a false fact or impossible setup. | Identify the false premise, avoid accepting it, and answer only what can be answered. |
| Hidden-constraint | A constraint is present but easy to miss, implicit, or embedded in context. | Surface the constraint and satisfy it before optimizing for convenience. |
| Should-stop | Continuing would violate scope, safety, evidence, authorization, or task completion boundaries. | Stop, explain the boundary briefly, and avoid fabricating additional work. |
| Confidence | The task is answerable only with uncertainty, incomplete evidence, or probabilistic judgment. | State confidence level, uncertainty drivers, and what would change the conclusion. |
| Claim-boundary | The prompt invites a stronger claim than evidence supports. | Separate observed evidence from inference and reject unsupported value/readiness/superiority claims. |

## Candidate task distribution

A future 30-task draft should start balanced across the five families:

- 6 false-premise tasks;
- 6 hidden-constraint tasks;
- 6 should-stop tasks;
- 6 confidence tasks;
- 6 claim-boundary tasks.

The balanced split is a feasibility assumption, not a frozen benchmark design.
