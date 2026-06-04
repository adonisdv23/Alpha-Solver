# Selective Expert Engagement Plan

Status: planning memo only

Lane: `ALPHA-SELECTIVE-EXPERT-ENGAGEMENT-PLANNING-001`

This memo does not implement routing, runtime behavior, provider orchestration, `/v1/solve` changes, model configuration changes, feature flags, tool routing, live gates, new capture, rescoring, scoring-rubric changes, Google Sheet updates, or Batch C.

## 1. Purpose

This planning memo asks: when should Alpha apply expert/interrogation behavior, and when should it stay concise/plain-like?

The goal is to define candidate future engagement criteria from committed evaluation evidence. It is not to change the active standalone behavior contract, runtime routes, provider behavior, model configuration, or evaluator scoring.

## 2. Evidence basis

Committed source artifacts used:

- A3-1 score table: `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/score-table.csv`
- A3-1 defects: `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/defects.md`
- A3-1 run summary: `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/run-summary.md`
- Batch B blinded score sheet: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blinded-score-sheet.csv`
- Batch B blinding map: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blinding-map.csv`
- Batch B score table: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/score-table.csv`
- Batch B defects: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/defects.md`
- Batch B run summary: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/run-summary.md`
- Batch B interpretation review: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/interpretation-review.md`
- Post-interpretation decision: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/post-interpretation-decision.md`
- Lift decision rule: `docs/evals/LIFT_DECISION_RULE.md`
- Response quality rubric: `docs/evals/RESPONSE_QUALITY_RUBRIC.md`

The current behavior-contract files were inspected for context only. `alpha_solver_portable.py` is treated as the active standalone behavior contract; `alpha-solver-v91-python.py` is treated as an architecture reference entrypoint because it imports repo modules. This memo does not modify either file.

## 3. Current evidence summary

- A3-1 aggregate: Plain = 237, Alpha = 228, Alpha delta = -9. Plain won all four limited comparisons.
- Batch B aggregate: Plain = 405, Alpha = 455, Alpha delta = +50. Alpha wins = 8, Plain wins = 4, Ties = 0.
- Batch B lift cluster: Plain = 111, Alpha = 132, Alpha delta = +21.
- Batch B polish cluster: Plain = 87, Alpha = 86, Alpha delta = -1.
- Batch B brevity dimension `d12_brevity`: Plain = 26, Alpha = 16, Alpha delta = -10.
- Interpretation: Alpha appears conditionally useful, not globally superior. A3-1 favored plain in a limited four-comparison run, while Batch B favored Alpha in a limited 12-comparison pilot. The combined evidence suggests prompt-set-dependent behavior.

## 4. Core thesis

Alpha's value appears prompt-set-dependent. Expert/interrogation behavior should be treated as a conditional capability, not a universal default.

The immediate goal is to define future engagement criteria. It is not to implement a router, live gate, provider orchestrator, model selector, or `/v1/solve` change.

## 5. Candidate positive signals for expert engagement

Future engagement criteria may consider expert/interrogation behavior when one or more of these signals are present:

- claim-boundary risk;
- unsupported validation or superiority wording;
- safety or credential risk;
- private data or blinding risk;
- artifact preservation risk;
- source hierarchy conflict;
- hidden constraints;
- multi-step operator workflow;
- protocol/checklist requirements;
- evidence uncertainty;
- high cost of overclaiming;
- need for remediation path or stop condition.

These signals are candidates only. They do not create a runtime gate and do not authorize provider routing.

## 6. Candidate signals for staying concise/plain-like

Future engagement criteria may favor concise/plain-like behavior when one or more of these signals are present and no hidden high-risk condition is detected:

- user asks for a short reviewer note;
- user asks for yes/no first;
- user asks for under 120 words;
- user asks for a direct rewrite;
- task has low ambiguity;
- task asks for one sentence;
- task asks for a single next action;
- adding roles, timelines, commands, or protocols would be ungrounded;
- prompt does not need artifact/protocol risk handling;
- brevity is part of correctness.

## 7. Ambiguous or mixed signals

Mixed prompts should not be treated as a binary choice between full expert mode and plain brevity. Candidate mixed cases include:

- yes/no question with safety caveat;
- short rewrite involving claim-boundary risk;
- coding-agent instruction cleanup;
- public-facing wording involving evidence limits;
- artifact request with unknown preservation state;
- user asks for speed but the topic contains hidden risk.

For these cases, the candidate response pattern is answer-first plus compact caveats: give the requested direct answer or rewrite first, then add only the minimum caveat, stop condition, or remediation path needed to prevent unsafe or unsupported use.

## 8. Engagement matrix

The companion CSV `selective-expert-engagement-matrix.csv` contains one row for each A3-1 and Batch B comparison where a planning-level recommendation can be derived from committed artifacts. It records:

- comparison ID;
- prompt family;
- observed winner;
- candidate engagement decision;
- recommended response mode;
- why to engage or stay concise;
- confidence;
- future test need.

The matrix does not include raw outputs, provider metadata, raw provider payloads, request identifiers, response identifiers, credentials, or private capture material. Recommendations are planning hypotheses, not runtime decisions.

## 9. Proposed future decision policy, planning only

Candidate policy for a future operator-approved spec:

- If a high-risk claim, safety, artifact, evidence, or source hierarchy issue is detected, use compact expert engagement.
- If the user requests concise output and no hidden risk is detected, stay concise/plain-like.
- If both high-risk and concise-output signals are present, answer first, then add a minimal risk caveat.
- If the task asks for a protocol, checklist, or remediation path, expand enough to be executable.
- If the task asks for a reviewer comment or one-sentence statement, do not turn it into a full process memo.
- Never invent timelines, roles, file paths, metrics, commands, owners, or acceptance criteria unless provided or requested.

This policy is not implemented. It is a planning candidate for future review.

## 10. How this differs from routing

- This is not runtime routing.
- This is not provider orchestration.
- This is not tool routing.
- This is not a model-selection policy.
- This is a planning memo for future behavior criteria.
- Any future implementation requires a separate operator-approved spec and PR.

## 11. Relationship to `ALPHA-BREVITY-CONTROL-001`

Brevity control handles how much Alpha says. Selective engagement handles whether Alpha should engage deeper behavior at all.

These are related but not identical. Batch B's `d12_brevity` penalty shows that length matters, but the lift-versus-polish evidence suggests that simply capping length may also remove useful risk, evidence, and artifact handling. Future implementation should avoid solving engagement only with length caps.

## 12. Relationship to `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001`

Claim-boundary risk is one of the strongest engagement signals. Some prompts should trigger expert behavior because unsupported validation wording, causality wording, production-readiness language, superiority claims, or provider-orchestration claims are dangerous when not supported by committed evidence.

However, claim-boundary caveats must still be compact when the user asks for short output. A short claim-boundary rewrite should not become a full validation memo unless the user asks for that depth.

## 13. Relationship to `OUTPUT-DIFF-LIFT-VS-POLISH-DIAGNOSTIC-001`

Diagnostics should test whether engagement decisions preserve substantive lift while reducing polish/verbosity effects. The engagement matrix should inform prompt-family splits and retrospective gate simulation.

The diagnostic work should ask whether a compact-engagement mode can preserve improvements in hidden constraints, risk/failure handling, evidence uncertainty, and comparative value while reducing the brevity penalty on concise/operator-facing prompts.

## 14. Candidate acceptance criteria for future implementation

A future implementation, if separately approved, should meet criteria such as:

- The system identifies high-risk prompt families where expert engagement is warranted.
- It stays concise on low-risk, concise-output prompts.
- It preserves `d08_evidence_uncertainty`, `d05_hidden_constraints`, `d06_risk_failure`, and `d14_comparative_value`.
- It improves or does not worsen `d12_brevity` on concise/operator-facing prompts.
- It does not introduce unsupported details, timelines, roles, metrics, commands, owners, or file paths.
- It does not make broad validation or superiority claims.
- It is evaluated separately before any production-readiness claim.

These are candidate acceptance criteria only and do not authorize implementation.

## 15. Risks and mitigations

| Risk | Mitigation candidate |
| --- | --- |
| False negatives: expert behavior skipped when needed. | Require high-risk claim, safety, artifact, evidence, and source-hierarchy signals to override pure brevity. |
| False positives: expert behavior triggered on simple prompts. | Add concise-output and low-ambiguity signals before expanding. |
| Over-compression of safety/evidence caveats. | Preserve a minimum caveat for safety, claims, artifact preservation, and source hierarchy. |
| Overfitting to Batch B. | Test against A3-1, Batch B, and holdout prompt families before implementation claims. |
| Turning planning into runtime changes prematurely. | Keep this memo docs-only; require a separate operator-approved spec and PR. |
| Confusing selective engagement with provider orchestration. | State that this is behavior-criteria planning only, not provider or tool routing. |
| Creating a hidden router before evidence supports it. | Avoid feature flags, route tables, runtime gates, model selectors, or provider changes in this lane. |

## 16. Future evaluation ideas, not authorized now

Potential evaluation ideas for later operator approval:

- retrospective gate simulation on A3-1 and Batch B;
- forced-concise Alpha comparison;
- prompt-family holdout;
- low-headroom versus high-headroom comparison set;
- length-strip re-score;
- multi-judge review of gate decisions.

These ideas are not authorized now. They do not start Batch C, new capture, rescoring, live provider calls, or implementation work.

## 17. Not authorized

This lane does not authorize:

- routing;
- provider orchestration;
- runtime gate implementation;
- tool routing;
- model/provider changes;
- live capture;
- Batch C;
- scoring-rubric changes;
- Google Sheet updates;
- production readiness;
- public validation claims.

## 18. Recommended next operator decision

Review this planning memo after `ALPHA-BREVITY-CONTROL-001` and `OUTPUT-DIFF-LIFT-VS-POLISH-DIAGNOSTIC-001`.

Decide whether to promote selective expert engagement into a formal spec after brevity and diagnostic plans are merged. Recommended default: keep this as planning until brevity-control and diagnostic work clarify implementation criteria.

## 19. Non-claims

This memo makes the following explicit non-claims:

- no MVP validation;
- no Alpha Solver superiority generally;
- no broad plain-provider inferiority;
- no answer-quality superiority generally;
- no production readiness;
- no broad runtime readiness;
- no benchmark success;
- no exact billing accuracy;
- no provider reasoning orchestration.
