# ALPHA-ANSWER-STRUCTURE-V2-001

Status: Proposed / Planning

Phase: `OUTPUT-DIFFERENTIATION-PHASE-001`

Type: planning/spec only

This document is a planning proposal only. It includes no runtime implementation, no behavior change, no provider/model/routing change, no scoring-rubric change, no new capture, no rescoring, no Google Sheet update, and no Batch C work.

## 1. Goal

Define a prompt-aware answer-structure plan for future Alpha behavior that:

- leads with the user's requested deliverable;
- chooses a response shape based on task type and risk;
- preserves Alpha's evidence, safety, artifact, and claim-boundary lift;
- avoids unnecessary process, invented scaffolding, and verbosity.

The desired future control is not a single shorter template. It is an answer architecture that can stay concise for operator-format requests while still surfacing the evidence boundaries, safety constraints, artifact stop conditions, and protocol discipline that helped Alpha in the committed Batch B pilot.

## 2. Motivation

The committed evaluation evidence supports a narrow planning lane for answer structure, not implementation and not broad claims.

- Alpha's Batch B lift was not merely polish: the Batch B lift cluster favored Alpha by +21 while the polish cluster was approximately flat at -1.
- Alpha's largest weakness was brevity: `d12_brevity` favored Plain by 10 points in Batch B.
- Plain wins showed format-fit and directness risks, especially for reviewer comments, short explanations, direct rewrites, and concise operator communication.
- Alpha wins showed value when structure was justified by claim-boundary, safety, artifact, source-hierarchy, or protocol risk.
- Selective expert engagement planning shows Alpha should not apply the same answer shape universally.
- Claim-boundary planning shows safe wording and evidence limits should appear early enough to guide the answer, not be buried after a long memo.

The planning objective is therefore to preserve useful Alpha behavior while preventing heavy answer shapes from overriding the user's requested format.

## 3. Non-goals

This spec does not authorize or include:

- runtime changes in this PR;
- `/v1/solve` changes;
- routing changes;
- provider/model changes;
- scoring rubric changes;
- Batch C;
- new capture;
- rescoring outputs;
- implementation of answer routing;
- provider orchestration;
- public validation or superiority claims;
- a forced template that overrides user format;
- feature flags;
- tool routing;
- quota or cost/latency optimization work.

## 4. Evidence summary

| Evidence item | Committed result or lesson | Answer-structure implication |
| --- | --- | --- |
| A3-1 aggregate | Plain 237, Alpha 228, Alpha delta -9; Plain won all four limited comparisons. | Alpha can lose when the answer shape is too heavy or less format-fit for the prompt set. |
| Batch B aggregate | Plain 405, Alpha 455, Alpha delta +50; Alpha wins 8, Plain wins 4, ties 0. | Alpha has useful limited-pilot lift, but the result remains prompt-set-dependent. |
| Batch B lift cluster | Plain 111, Alpha 132, Alpha delta +21. | Future structure should preserve substantive constraint, risk, evidence, and comparative-value gains. |
| Batch B polish cluster | Plain 87, Alpha 86, Alpha delta -1. | Batch B's Alpha advantage should not be treated as just formatting polish. |
| Batch B brevity dimension | `d12_brevity`: Plain 26, Alpha 16, Alpha delta -10. | Answer structure must control length, section count, and over-answering. |
| Relevant Plain wins | Plain wins clustered around concise operator communication, format fit, short-answer fit, direct rewrite fit, and avoiding over-designed process. | Direct answer, reviewer comment, and safe rewrite modes must not expand into full memos by default. |
| Relevant Alpha wins | Alpha wins were strongest around claim-boundary discipline, evidence hygiene, unsafe instruction cleanup, protocol/framing discipline, and artifact preservation. | Structured modes should engage when risk justifies visible caveats, stop gates, or protocol order. |
| `ALPHA-BREVITY-CONTROL-001` | Plans controls for answer length and over-answering. | Answer structure should define which tasks deserve one sentence, one paragraph, short bullets, or fuller structure. |
| `OUTPUT-DIFF-LIFT-VS-POLISH-DIAGNOSTIC-001` | Plans diagnostics to separate substantive lift from polish or verbosity effects. | Future evals should test whether compact structure preserves lift rather than just reducing length. |
| `ALPHA-SELECTIVE-EXPERT-ENGAGEMENT-PLANNING-001` | Plans when deeper expert behavior should engage. | Answer shape should vary by task signal and risk, not apply expert scaffolding universally. |
| `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001` | Plans safer wording for validation, causality, readiness, and superiority boundaries. | Evidence boundaries should appear early, especially in public claims, release wording, and interpretation tasks. |

## 5. Problem statement

Alpha has useful expert behavior, but its answer shape can be too heavy for direct operator requests. When the requested output is a reviewer comment, short explanation, direct rewrite, or yes/no answer, Alpha must not convert it into a full memo unless the prompt explicitly requests that expansion or hidden risk requires a compact caveat.

At the same time, when a task contains claim-boundary, safety, artifact, source-hierarchy, or protocol risk, Alpha needs enough structure to prevent misuse. A one-line answer can be unsafe or misleading if it hides evidence limitations, preservation requirements, or stop conditions.

The missing control is not just brevity. It is prompt-aware answer architecture: choosing the minimum structure that satisfies the requested artifact while keeping essential risk boundaries visible.

## 6. Answer-structure principles

1. **Deliverable first**: start with the answer, rewrite, comment, decision, or checklist the user asked for.
2. **Requested format before system format**: respect the user's target format unless it conflicts with safety, evidence, or artifact constraints.
3. **Answer-first when possible**: give the direct answer before rationale when the answer can be stated safely.
4. **Compact caveat before long caveat**: use a short boundary note before expanding into explanation.
5. **Structure earns its place**: add headings, tables, or procedures only when they improve correctness, safety, traceability, or usability.
6. **No invented scaffolding**: do not add roles, dates, owners, commands, metrics, acceptance criteria, or file paths unless supplied or requested.
7. **Evidence boundary stays visible**: when evidence is limited, state that limit before recommendations or public wording.
8. **Safety and artifact stop conditions stay visible**: do not bury stop gates, preservation requirements, or unsafe-instruction removals.
9. **Expand only for risk or explicit request**: more structure is appropriate for protocol, artifact, source-hierarchy, safety, or synthesis tasks.
10. **Stop after satisfying the asked-for artifact**: do not append broad next steps or implementation plans that were not requested.

## 7. Proposed response modes, planning only

These modes are planning candidates for future behavior. They do not implement answer routing or runtime branching in this PR.

| Mode | When to use | Default structure | Max useful detail | Expansion triggers | Common failure mode | Evidence reference |
| --- | --- | --- | --- | --- | --- | --- |
| Direct answer | Yes/no, short factual response, concise operator decision, or under-120-word request. | One sentence or one short paragraph: answer first, optional compact caveat. | Usually 1-4 sentences. | Hidden safety risk, evidence ambiguity, conflicting source hierarchy, or explicit request for rationale. | Turning a short answer into a memo or adding unasked next steps. | A3-1 Plain wins and Batch B Plain wins on concise format fit. |
| Reviewer comment | User asks for a PR/reviewer note, margin comment, or concise critique. | The comment only; optional one-line rationale outside the comment if useful. | One comment paragraph or 3 short bullets. | Safety issue, unsupported claim, or artifact-loss risk. | Adding headings such as background, implementation plan, or acceptance criteria. | Batch B Plain win on reviewer-comment format fit. |
| Safe rewrite | User asks to rewrite unsafe, overbroad, or misleading instructions. | Publishable replacement first; optional compact note naming key removals. | Replacement plus up to 3 bullets if needed. | Unsafe coding-agent instruction, public claim, evidence-boundary risk, or policy conflict. | Over-designing process instead of providing the requested rewrite. | Batch B Plain and Alpha split on safe rewrite/directness; Alpha wins on unsafe instruction cleanup. |
| Evidence-boundary answer | Release wording, public claim, validation wording, benchmark interpretation, or evidence-dependent recommendation. | Boundary sentence first, then bounded answer or wording. | One paragraph to compact memo. | Risk of broad validation, superiority, readiness, causal, or exact-cost claim. | Burying the caveat after persuasive wording or making unsupported claims. | Batch B Alpha wins on claim-boundary and evidence hygiene; claim-boundary planning packet. |
| Compact expert answer | Expert answer needed, but prompt still asks for concise operator output. | Answer first, then short bullets for constraints, rationale, and next action only if useful. | 3-6 bullets or a compact memo. | Hidden constraints, risk/failure analysis, decision tradeoff, or source-hierarchy conflict. | Applying full protocol framing to a narrow request. | Batch B lift cluster +21 with brevity weakness. |
| Artifact stop-condition answer | Preservation, evidence packet, raw artifact, source hierarchy, or do-not-modify risk. | Stop condition first, then exact allowed action or checklist. | Short bullets or compact checklist. | Potential artifact loss, unapproved capture, rescoring, or source-of-truth conflict. | Giving recommendations before stating preservation or stop gates. | Batch B Alpha wins on artifact preservation and protocol discipline. |
| Protocol checklist | User requests process, gate, checklist, evaluation protocol, or controlled run procedure. | Ordered checklist with stop gates and non-goals. | Full checklist only when requested or risk warrants. | Eval integrity, blinding, capture, scoring, or artifact-preservation risk. | Checklist bloat when the user wanted a comment or one-line answer. | Batch B Alpha wins on protocol/framing discipline. |
| Implementation prompt for coding agent | User asks for a coding-agent prompt, scoped implementation task, or repo task handoff. | Goal, scope, hard boundaries, required files, validation checks, return format. | Full prompt when requested. | Runtime risk, provider calls, secrets, source hierarchy, or artifact constraints. | Inventing unprovided files, metrics, commands, timelines, or acceptance criteria. | Batch B Alpha wins on unsafe instruction cleanup and source/protocol discipline. |
| Interpretation memo | User asks for synthesis, interpretation, decision artifact, or cross-run analysis. | Summary, evidence basis, interpretation, caveats, next decision, non-claims. | Compact to full memo depending on prompt. | Conflicting evidence, prompt-set dependence, public claim risk, or decision-gate request. | Claiming broad validation or making measurement changes. | Batch B interpretation review and post-interpretation decision artifacts. |

## 8. Mode-selection matrix

| Prompt signal | Recommended response mode | First sentence pattern | Allowed sections | Forbidden expansion | Related lane |
| --- | --- | --- | --- | --- | --- |
| Yes/no requested | Direct answer | Decision-first | None, or one compact rationale paragraph. | Full memo, checklist, implementation plan. | `ALPHA-BREVITY-CONTROL-001` |
| Short reviewer note | Reviewer comment | Correction-first or decision-first | Comment only; optional one-line rationale. | Background, scope, tests, acceptance criteria, timeline. | `ALPHA-ANSWER-STRUCTURE-V2-001` |
| Under 120 words | Direct answer | Decision-first | One paragraph or short bullets within requested limit. | Extra headings or unrequested caveat sections. | `ALPHA-BREVITY-CONTROL-001` |
| Direct rewrite | Safe rewrite | Safe-alternative-first | Rewritten text; optional short note. | Process memo, multi-step plan, invented context. | `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001` |
| Release note or public claim | Evidence-boundary answer | Evidence-boundary-first | Boundary, bounded wording, optional rationale. | MVP, superiority, production, benchmark, or exact-cost claims. | `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001` |
| Unsafe coding-agent instruction | Safe rewrite or implementation prompt for coding agent | Safe-alternative-first | Clean prompt, hard boundaries, optional removed-items note. | Provider orchestration, live calls, secrets, unapproved capture. | `ALPHA-SELECTIVE-EXPERT-ENGAGEMENT-PLANNING-001` |
| Repo-vs-sheet conflict | Evidence-boundary answer | Evidence-boundary-first | Source hierarchy, decision, compact rationale. | Treating external ledger as implementation proof. | `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001` |
| Artifact preservation risk | Artifact stop-condition answer | Stop-condition-first | Stop gate, allowed action, preservation checklist. | Editing/deleting artifacts before evidence is preserved. | `OUTPUT-DIFF-LIFT-VS-POLISH-DIAGNOSTIC-001` |
| Raw provider payload question | Artifact stop-condition answer | Stop-condition-first | Sanitized boundary, allowed summary, preservation note. | Raw payload disclosure or secret-like identifiers. | `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001` |
| Protocol/checklist requested | Protocol checklist | Checklist-first | Ordered checklist, gates, non-goals. | Narrative memo unless requested. | `OUTPUT-DIFF-LIFT-VS-POLISH-DIAGNOSTIC-001` |
| Implementation prompt requested | Implementation prompt for coding agent | Checklist-first or stop-condition-first | Task, scope, files, boundaries, validation, return format. | Runtime/provider/model/routing work unless authorized. | `ALPHA-SELECTIVE-EXPERT-ENGAGEMENT-PLANNING-001` |
| Interpretation or synthesis requested | Interpretation memo | Evidence-boundary-first or decision-first | Summary, evidence, interpretation, caveats, next decision, non-claims. | Broad validation claims or score changes. | `OUTPUT-DIFF-POST-IMPROVEMENT-RUN-001` |

## 9. First-sentence patterns

Use synthetic wording only. These examples are not quotes from captured outputs.

| Pattern | Use | Safe synthetic example |
| --- | --- | --- |
| Decision-first | The user asks yes/no, choose/decide, or wants a direct operator answer. | "Yes — use the shorter version, with one caveat about the evidence limit." |
| Correction-first | The user asks for a reviewer note or a concise correction. | "This should say the run was limited and prompt-set-dependent, not validated." |
| Safe-alternative-first | The user asks for a rewrite of unsafe or overbroad text. | "Use: `The pilot showed a limited improvement on this prompt set; broader validation is still pending.`" |
| Stop-condition-first | The task may cross a hard boundary or damage artifacts. | "Stop if the committed score table is missing; do not recreate scores from memory." |
| Evidence-boundary-first | The answer depends on limited evidence or source hierarchy. | "Based only on the committed pilot artifacts, the evidence supports planning, not a public performance claim." |
| Checklist-first | The user asks for a protocol, runbook, or coding-agent task. | "Checklist: confirm evidence, preserve artifacts, make the docs-only edit, then run non-live checks." |
| Caveat-first only when necessary | The direct answer would mislead unless bounded first. | "Caveat: this is not a production-readiness result; within that limit, the next step is a planning review." |

## 10. Section-budget rules

| Budget | Allowed when | Shape | Not allowed when |
| --- | --- | --- | --- |
| One sentence | Yes/no, simple decision, or requested one-liner. | Direct answer plus compact caveat if needed. | Evidence, safety, or artifact risk cannot be safely expressed in one sentence. |
| One paragraph | Short explanation, concise operator answer, direct recommendation. | Answer first, 2-4 supporting sentences. | User requested only a comment or exact rewrite. |
| Short bullets | Several constraints or options are useful but the task is still compact. | 3-5 bullets, no nested sections by default. | Bullets become a hidden protocol or unrequested plan. |
| Compact memo | Interpretation, claim-boundary advice, or expert synthesis with moderate risk. | Summary, evidence boundary, recommendation, non-claims if relevant. | User asked for under-120 words or a reviewer comment. |
| Full protocol checklist | User explicitly asks for a checklist/protocol or eval integrity requires gates. | Ordered steps, stop conditions, validation checks, non-goals. | User asked for a direct answer, comment, or rewrite. |
| Interpretation review | User asks for cross-run synthesis or decision artifact. | Evidence basis, findings, caveats, decision options, non-claims. | It would imply new scoring, new capture, or broad validation. |

## 11. Interaction with related lanes

- `ALPHA-BREVITY-CONTROL-001`: controls answer length and over-answering. This answer-structure spec provides the mode and section-budget layer that decides where brevity constraints apply.
- `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001`: controls safe evidence wording. This spec requires claim and evidence boundaries to appear early in modes where unsupported public wording could mislead.
- `ALPHA-SELECTIVE-EXPERT-ENGAGEMENT-PLANNING-001`: controls when deeper expert behavior should engage. This spec converts engagement decisions into output shapes, without implementing a router or live gate.
- `OUTPUT-DIFF-LIFT-VS-POLISH-DIAGNOSTIC-001`: tests whether answer structure preserves substantive lift rather than polish. This spec supplies candidate structures that future diagnostics can compare after approval.
- `OUTPUT-DIFF-POST-IMPROVEMENT-RUN-001`: future measurement after approved improvements. This spec does not start that run; it identifies what a future run may need to observe.

## 12. Candidate future behavior rules

Planning only; these are not implemented here.

- If the user requests a concise answer, produce a concise answer unless hidden risk requires a compact caveat.
- If the user asks for a reviewer comment, output only the comment plus optional one-line rationale.
- If the user asks for a safe coding-agent prompt, remove unsafe instructions and list removed items only if useful.
- If the user asks for release wording, give publishable bounded wording first.
- If the user asks for protocol/checklist, provide an ordered checklist with stop gates.
- If the answer requires an evidence boundary, state the boundary before recommendations.
- Do not add timelines, roles, file paths, commands, metrics, or acceptance criteria unless provided or requested.
- Do not hide important uncertainty to be brief.
- Do not use broad validation or superiority language.

## 13. Acceptance criteria for future implementation

A future implementation should not be approved unless it can be evaluated against concrete criteria such as:

- Alpha starts with the requested deliverable in concise/operator prompts.
- Alpha chooses the correct response mode for task type.
- Alpha does not add unnecessary process sections to reviewer comments or short explanations.
- Alpha preserves claim-boundary and evidence caveats.
- Alpha does not invent details.
- Alpha improves or does not worsen `d12_brevity` on concise prompts.
- Alpha preserves or does not materially reduce `d08_evidence_uncertainty`, `d05_hidden_constraints`, `d06_risk_failure`, and `d14_comparative_value`.
- Future evals distinguish answer structure from substantive lift.
- Token/length fields should be captured if feasible without exact-billing claims.

## 14. Test plan for future implementation

Planning only; no live provider tests, post-improvement run, new capture, or rescoring occur in this PR.

Future implementation should define and run non-live tests such as:

- golden output-shape tests;
- forbidden-section tests for reviewer comments;
- safe rewrite structure tests;
- evidence-boundary first-sentence tests;
- no-invented-scaffolding tests;
- concise caveat tests;
- prompt-family tests using A3-1 and Batch B as design references, not proof;
- no live provider tests in this PR;
- no post-improvement run until approved.

## 15. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Over-templating | Treat modes as planning guides, not mandatory visible templates; user format remains primary. |
| Over-compression | Preserve compact caveats and stop conditions when evidence, safety, or artifact risk is material. |
| Hiding risk | Require evidence-boundary and stop-condition-first patterns when a direct answer would mislead. |
| Losing Alpha lift | Future tests should verify `d08_evidence_uncertainty`, `d05_hidden_constraints`, `d06_risk_failure`, and `d14_comparative_value` do not materially regress. |
| Answer modes becoming a hidden router | Keep this as output-shape planning; do not change provider selection, model selection, routing, or tool orchestration. |
| Overfitting to Batch B | Treat A3-1 and Batch B as limited, prompt-set-dependent design references, not proof of broad performance. |
| Confusing planning with implementation | Keep this PR docs/spec only and require a separate operator-approved implementation decision. |

## 16. Implementation boundaries

This spec implements nothing. Future implementation must be separate and operator-approved.

No runtime, provider, model, routing, rubric, capture, scoring, Google Sheet, or Batch C work happens here. This spec does not modify `alpha_solver_portable.py`, `alpha-solver-v91-python.py`, `/v1/solve`, provider configuration, model configuration, routing logic, scoring artifacts, or evaluation rubrics.

## 17. Recommended next operator decision

If this spec is approved, the next decision is whether to consolidate the planning lanes into a narrow implementation-decision artifact.

Recommended default: after merging this spec, create a consolidated implementation-readiness review rather than immediately implementing behavior. That review should reconcile brevity control, claim-boundary calibration, selective expert engagement, lift-vs-polish diagnostics, and answer-structure modes before any runtime change is authorized.

## 18. Non-claims

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
