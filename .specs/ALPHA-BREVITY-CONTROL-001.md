# ALPHA-BREVITY-CONTROL-001

Status: Proposed / Planning  
Phase: OUTPUT-DIFFERENTIATION-PHASE-001  
Type: planning/spec only

This spec is a planning artifact only. It includes no runtime implementation and does not change Alpha behavior in this PR.

## Goal

Define a narrow Alpha brevity-control plan that reduces over-answering, improves short-answer-first behavior, and preserves substantive lift. The target is not to make Alpha shorter everywhere; it is to deliver Alpha's observed lift with less unnecessary overhead when the user asks for concise, operator-facing, or format-constrained output.

## Motivation

Committed evaluation evidence supports targeted planning, not runtime changes:

- Batch B favored Alpha overall in a limited 12-comparison pilot: Plain 405, Alpha 455, Alpha delta +50, Alpha wins 8, Plain wins 4, ties 0.
- Batch B also showed Alpha's clearest negative dimension was `d12_brevity`: Plain 26, Alpha 16, Alpha delta -10.
- Plain wins clustered around concise operator communication, format fit, short-answer fit, and avoiding over-designed process.
- Alpha wins showed real value in claim-boundary discipline, evidence hygiene, unsafe instruction cleanup, protocol/framing discipline, and artifact preservation.
- A3-1 favored plain in a limited four-comparison run, while Batch B favored Alpha in a limited 12-comparison pilot. The combined evidence suggests prompt-set-dependent behavior rather than broad superiority by either surface.

The improvement target is therefore: deliver Alpha's lift with less unnecessary overhead.

## Non-goals

This spec does not authorize or include:

- runtime changes in this PR;
- `/v1/solve` changes;
- routing changes;
- provider or model changes;
- scoring rubric changes;
- Batch C;
- new capture;
- rescoring outputs;
- unblinding new material;
- Google Sheet updates;
- feature flags;
- provider orchestration;
- tool routing;
- quota, cost, or latency optimization work;
- claims of MVP validation or broad superiority;
- forced universal brevity that damages evidence discipline.

## Evidence summary

| Evidence item | Committed result | Planning implication |
| --- | --- | --- |
| A3-1 aggregate | Plain 237, Alpha 228, Alpha delta -9; plain won all four limited comparisons. | Treat the evidence as prompt-set-dependent and avoid broad claims. |
| Batch B aggregate | Plain 405, Alpha 455, Alpha delta +50; Alpha wins 8, Plain wins 4, ties 0. | Alpha showed value on this limited pilot, but only targeted planning is authorized. |
| Batch B lift cluster | Plain 111, Alpha 132, Alpha delta +21. | Preserve substantive lift while refining answer control. |
| Batch B polish cluster | Plain 87, Alpha 86, Alpha delta -1. | Polish did not explain the overall Alpha advantage; brevity/control needs focused improvement. |
| Batch B brevity dimension | `d12_brevity`: Plain 26, Alpha 16, Alpha delta -10. | Treat brevity as a first-order control dimension. |
| Relevant plain wins | `cmp-B1-CAND-003`, `cmp-B1-CAND-005`, `cmp-B1-CAND-015`, and `cmp-B1-CAND-017` favored cleaner source-hierarchy guidance, compact reviewer comments, brevity/control, and concise risk review. | Improve short-answer-first behavior, format fit, and restraint on process scaffolding. |
| Relevant Alpha wins | `cmp-B1-CAND-001`, `cmp-B1-CAND-007`, `cmp-B1-CAND-009`, `cmp-B1-CAND-011`, `cmp-B1-CAND-013`, `cmp-B1-CAND-020`, `cmp-B1-CAND-021`, and `cmp-B1-CAND-022` favored claim boundaries, unsafe instruction cleanup, artifact preservation, implementation prompt discipline, protocol checklist framing, truthful alternative wording, and raw payload preservation explanation. | Preserve evidence hygiene, safety, claim boundaries, and artifact discipline. |

## Problem statement

Alpha can create useful lift, but sometimes spends too many words, adds unnecessary process, introduces invented placeholders, roles, timelines, file paths, command examples, metrics, or acceptance criteria, and misses the requested compact format.

This hurts prompts asking for short reviewer notes, concise answers, direct rewrites, or operator-facing decisions. In those cases, extra process can make the answer less usable even when the underlying reasoning is careful.

Brevity should therefore be treated as a first-order control dimension, not a cosmetic preference. The objective is calibrated brevity: short enough to fit the requested task, but not so compressed that safety, uncertainty, evidence discipline, artifact preservation, or claim boundaries are lost.

## Brevity-control principles

Future design should follow these principles:

1. **Answer first.** Start with the direct answer before explanation when the prompt asks for a yes/no decision, reviewer note, concise explanation, or next action.
2. **Obey requested format before adding structure.** If the user asks for a reviewer comment, provide a reviewer comment rather than a full incident protocol.
3. **Use minimum sufficient reasoning.** Include only the reasoning needed to support the requested output and preserve important constraints.
4. **Keep caveats proportional.** Preserve uncertainty and claim boundaries, but compress low-risk caveats into one clear sentence.
5. **Use optional detail only when requested or risk justified.** Add deeper analysis when the prompt asks for depth, protocol design, remediation planning, or hidden-risk review.
6. **Do not invent specifics.** Do not add roles, timelines, owners, file paths, command examples, metrics, or acceptance criteria unless supplied by the prompt or clearly requested.
7. **Preserve claim-boundary discipline.** Brevity must not turn preliminary, limited, or artifact-bound evidence into broad validation language.
8. **Preserve safety and artifact discipline.** Brevity must not remove credential-safety controls, raw artifact preservation rules, or stop conditions.
9. **Distinguish short from under-specified.** A good short answer still gives the necessary caveat or next step when the user needs one.

## Proposed behavior rules for future implementation

These are candidate future requirements only. They are not implemented by this PR.

| Candidate rule | Future requirement |
| --- | --- |
| Short-answer-first rule | Start with the direct answer when the user asks yes/no, asks "what next," asks for a reviewer note, or asks for a concise explanation. |
| Detail-budget rule | Limit supporting detail unless the prompt asks for exhaustive analysis, protocol design, remediation path, or hidden-risk review. |
| Format-fit rule | Match the requested artifact type. A reviewer comment means reviewer comment, not a full incident protocol. |
| No invented scaffolding rule | Do not add timelines, owners, file paths, command examples, metrics, or acceptance criteria unless provided or clearly requested. |
| Caveat compression rule | Keep uncertainty and claim boundaries, but compress them into one clear sentence when risk is low. |
| Expansion trigger rule | Expand only when the prompt has hidden constraints, safety risk, artifact preservation risk, claim-boundary risk, or multi-step operational consequences. |
| Stop-expansion rule | Stop when the answer has satisfied the user's requested output, named necessary caveats, and given the next action. |

## Task type routing matrix, planning only

This matrix is planning guidance only. It does not create routing behavior, provider orchestration, tool routing, or runtime task classification.

| Task type | Default response shape | Brevity target | Expansion triggers | Examples from Batch B evidence |
| --- | --- | --- | --- | --- |
| Yes/no operator decision | Direct decision in the first sentence, then one short reason and the next action if needed. | 1-3 short paragraphs or compact bullets. | Expand for hidden constraints, material risk, or unclear authorization boundary. | Plain advantages around source hierarchy and concise risk review suggest direct operator fit matters. |
| Reviewer comment | A paste-ready reviewer comment with minimal prefacing. | One concise comment; optional second sentence for remediation path. | Expand only if the prompt asks for multiple alternatives or formal acceptance criteria. | `cmp-B1-CAND-005` favored the compact reviewer-comment surface. |
| Release wording / claim-boundary rewrite | Provide the revised wording first, then a short note about claim boundary. | One rewritten paragraph plus one caveat sentence. | Expand when unsupported validation, causality, readiness, or public-claim risk is present. | `cmp-B1-CAND-001` and `cmp-B1-CAND-009` showed Alpha value in claim control. |
| Unsafe instruction cleanup | Provide safe replacement instructions and name removed unsafe elements. | Short safe rewrite plus 2-4 concise safety notes. | Expand when credentials, private data, or unsafe publication instructions are involved. | `cmp-B1-CAND-007` favored Alpha's unsafe instruction cleanup. |
| Artifact preservation stop condition | State the stop condition first, then list preservation requirements. | One direct stop line plus compact bullets. | Expand when raw evidence, auditability, or irreversible overwrite risk is present. | `cmp-B1-CAND-011` favored Alpha's artifact preservation discipline. |
| Implementation prompt to coding agent | Produce a bounded implementation prompt with scope, non-goals, and validation. | Structured but not expansive; include only requested constraints. | Expand for runtime safety, sensitive files, or test obligations. | `cmp-B1-CAND-013` favored Alpha's implementation prompt discipline. |
| Protocol checklist | Checklist-first answer with ordered steps and explicit stop gates. | As long as needed for safe execution, but avoid duplicated rationale. | Expand for multi-step operational consequences, preservation risk, or approval gates. | `cmp-B1-CAND-020` favored Alpha's protocol checklist framing. |
| Raw payload preservation explanation | Explain the preservation rule directly, then the reason and minimal handling steps. | Short explanation plus compact bullets. | Expand when audit evidence, redaction, or irreversible loss is possible. | `cmp-B1-CAND-022` favored Alpha on raw provider payload preservation explanation. |
| Short reviewer explanation | Start with the explanation in plain language, then one caveat if necessary. | 1-2 short paragraphs. | Expand only if the prompt asks for detailed rationale or alternatives. | Plain wins clustered around short-answer fit and avoiding over-designed process. |
| Evidence synthesis / interpretation | Lead with the conservative interpretation, then summarize evidence and non-claims. | Moderate length; tables allowed when evidence comparison is central. | Expand for conflicting evidence, claim-boundary risk, or decision gates. | Batch B interpretation found prompt-set-dependent behavior and authorized planning only. |

## Acceptance criteria for future implementation

A future implementation PR should define tests or eval checks showing that:

- On prompts requesting concise output, Alpha starts with a direct answer in the first sentence.
- Alpha does not add unrequested roles, timelines, commands, file paths, metrics, or acceptance criteria.
- Alpha preserves claim-boundary, safety, and evidence caveats.
- Alpha does not reduce `d08_evidence_uncertainty`, `d05_hidden_constraints`, `d06_risk_failure`, or `d14_comparative_value` in future evals.
- Alpha improves or at least does not worsen `d12_brevity` on concise/operator-facing prompts.
- Future measurement separates lift from polish.
- Future measurement records token, cost, or length fields if feasible, without making exact-billing claims.

## Test plan for future implementation

This PR runs documentation/spec checks only. A future implementation plan should:

- use existing Batch B comparisons as design references, not as training proof or eval proof;
- create small unit or golden tests for output shape if the repo supports it;
- run no live provider tests in this PR;
- require separate operator approval before any post-implementation run;
- include length-strip or forced-concise diagnostic variants if approved;
- keep future diagnostics separate from runtime implementation unless the operator explicitly approves both.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Over-compression damaging safety. | Keep explicit expansion triggers for safety, private-data, artifact, and operational-risk prompts. |
| Losing claim-boundary discipline. | Require caveat compression rather than caveat removal. |
| Hiding important uncertainty. | Preserve one clear uncertainty sentence when evidence is limited or preliminary. |
| Optimizing for brevity at the expense of lift. | Track lift dimensions separately from polish and brevity in future measurement. |
| Overfitting to Batch B. | Treat Batch B as limited committed evidence and design reference, not benchmark proof. |
| Turning planning into runtime changes prematurely. | Require a separate operator-approved implementation PR before changing behavior. |

## Implementation boundaries

- This spec does not implement anything.
- Any future implementation must come in a separate PR after operator approval.
- No runtime files are changed here.
- No provider, model, or routing files are changed here.
- No scoring rubric files are changed here.
- No capture, rescoring, unblinding, Google Sheet update, or Batch C work is performed here.

## Recommended next operator decision

If this spec is approved, the next step is either:

1. draft `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001`; or
2. draft a narrow implementation prompt for brevity-control behavior if the operator explicitly approves moving from planning to implementation.

Recommended default: finish the planning specs before implementation.

## Non-claims

This spec makes the following explicit non-claims:

- no MVP validation;
- no Alpha Solver superiority generally;
- no broad plain-provider inferiority;
- no answer-quality superiority generally;
- no production readiness;
- no broad runtime readiness;
- no benchmark success;
- no exact billing accuracy;
- no provider reasoning orchestration.
