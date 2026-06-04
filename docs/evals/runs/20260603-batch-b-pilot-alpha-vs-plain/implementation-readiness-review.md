# Alpha Implementation Readiness Review

## 1. Title and status

- **Title:** Alpha Implementation Readiness Review
- **Lane:** `ALPHA-IMPLEMENTATION-READINESS-REVIEW-001`
- **Status:** decision/review only
- **Implementation status:** no implementation is included in this artifact.

This review synthesizes the committed Batch B planning and interpretation artifacts to decide the smallest safe implementation path. It does not change runtime behavior, provider behavior, model behavior, routing behavior, `/v1/solve`, scoring rubrics, scored artifacts, capture scripts, or Google Sheets integrations.

## 2. Evidence basis

This review is based on the completed planning and evidence artifacts associated with PRs #251-#260:

| PR | Evidence artifact | Role in this review |
| --- | --- | --- |
| #251 | Batch B scored artifacts: `README.md`, `source-packet.md`, `blind-scorer-result.md`, `blinded-score-sheet.csv`, `blinding-map.csv`, `score-table.csv`, `defects.md`, `run-summary.md`, and `artifact-build-checks.md` | Preserved scored evidence and arithmetic basis for Batch B. |
| #252 | `interpretation-review.md` | Interprets A3-1 and Batch B as prompt-set-dependent evidence. |
| #253 | `post-interpretation-decision.md` | Defines post-interpretation lane direction and non-implementation boundaries. |
| #254 | `.specs/ALPHA-BREVITY-CONTROL-001.md` | Defines brevity-control planning and short-answer-first behavior goals. |
| #255 | `lift-vs-polish-diagnostic-plan.md` and `lift-vs-polish-diagnostic-matrix.csv` | Separates candidate substantive lift from polish/format effects. |
| #256 | `selective-expert-engagement-plan.md` and `selective-expert-engagement-matrix.csv` | Frames selective engagement as a future diagnostic/gating problem, not immediate runtime work. |
| #257 | `claim-boundary-calibration-plan.md`, `claim-boundary-risk-taxonomy.csv`, and `claim-boundary-scenario-bank.md` | Defines safe wording and non-claim boundaries. |
| #258 | `.specs/ALPHA-ANSWER-STRUCTURE-V2-001.md` | Defines answer-shape planning and response-mode concepts for future behavior. |
| #259 | `complexity-gradient-holdout-plan.md` and `complexity-gradient-slot-matrix.csv` | Defines holdout and contamination controls before judging future improvements. |
| #260 | `alpha-implementation-surface-map.md`, `alpha-implementation-impact-matrix.csv`, `future-implementation-test-map.md`, and `protected-surfaces-checklist.md` | Maps candidate surfaces, protected surfaces, and future tests. |

No new capture, scoring, rescoring, unblinding, provider call, or Sheet update was performed for this review.

## 3. Current evidence summary

The current evidence remains mixed and prompt-set-dependent:

| Evidence slice | Plain | Alpha | Alpha delta | Interpretation |
| --- | ---: | ---: | ---: | --- |
| A3-1 limited four-comparison run | 237 | 228 | -9 | Plain aggregate win in the limited A3-1 prompt set. |
| Batch B limited 12-comparison pilot | 405 | 455 | +50 | Alpha aggregate win in the limited Batch B prompt set. |
| Batch B lift cluster | 111 | 132 | +21 | Alpha showed candidate lift on claim boundaries, evidence hygiene, protocol framing, and artifact discipline. |
| Batch B polish cluster | 87 | 86 | -1 | Polish/format did not explain the Batch B aggregate advantage. |
| Batch B brevity dimension | 26 | 16 | -10 | Plain retained a clear brevity/control advantage. |

Combined evidence is prompt-set-dependent. A3-1 and Batch B together do not establish broad Alpha superiority, broad plain inferiority, MVP validation, benchmark success, production readiness, broad runtime readiness, exact billing accuracy, or provider reasoning orchestration.

## 4. Readiness judgment

**Judgment:** Ready for test-first implementation, constrained to minimal implementation planning and not runtime implementation yet.

Rationale:

- The evidence is strong enough to justify a test-first and contract-first implementation proposal.
- The evidence is not strong enough to authorize runtime/provider/model/routing changes.
- The safest next step is to make desired behavior executable through offline golden tests and explicit behavior-contract wording before changing user-visible behavior.
- Selective engagement, response-mode selection, and answer assembly guardrails remain higher-risk implementation surfaces until tests and boundaries are reviewed.

## 5. Candidate implementation paths

| Path | Benefit | Risk | Files likely touched | Tests required | Readiness | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| A. docs-only behavior-contract update | Lowest-risk way to convert planning evidence into explicit behavior expectations without changing runtime behavior. | Clarifies desired behavior but does not prove runtime behavior. | `docs/specs`, `.specs/`, and planning docs. | Documentation consistency checks, forbidden-claim scan, and no-runtime-diff confirmation. | Ready. | Include in the next lane as contract wording. |
| B. offline golden tests first | Creates an executable safety net for short-answer-first behavior, claim boundaries, evidence boundaries, artifact stop conditions, and no invented scaffolding before behavior changes. | Fixtures could overfit Batch B if they copy official scored artifacts or encode too narrow a prompt set. | `tests/golden` or other offline test fixtures; focused test files. | Short-answer-first golden tests, no invented scaffolding tests, claim-boundary safe wording tests, evidence-boundary tests, artifact stop-condition tests, no validation/superiority claim tests, and no live-provider-call checks. | Ready. | Start here. This is the safest first implementation step. |
| C. prompt/protocol wording update | A narrow wording change could improve answer structure, concise caveats, and safe claim wording once tests exist. | Changes user-visible behavior and may regress lift, brevity, or evidence discipline if applied before tests. | Prompt/protocol text only if explicitly approved; possibly `alpha_solver_portable.py` only if that is the approved prompt-text surface. | All offline golden tests plus regression checks that provider/model/routing behavior did not change. | Conditionally ready. | Consider only after tests and behavior-contract wording are reviewed. |
| D. answer assembly guardrails | Could enforce short-answer-first answer shape and avoid unnecessary sections in deterministic assembly seams. | More invasive runtime behavior change; may affect broad answer formatting. | Answer assembly modules; possibly `alpha_solver_portable.py` only if explicitly approved. | Response-shape golden tests, safety/evidence regression tests, artifact-boundary tests, and no live-provider-call checks. | Not ready. | Defer until the minimal contract/tests lane is complete. |
| E. safe wording helper | Could centralize limited-evidence and non-claim wording for claim-boundary-sensitive outputs. | Could create boilerplate, hide nuance, or become a runtime dependency before tests are mature. | Docs/specs first; helper code only in a later explicitly approved lane. | Claim-boundary safe wording tests, evidence-boundary tests, no validation/superiority claim tests. | Planning ready, implementation deferred. | Draft wording in docs first; do not implement a runtime helper yet. |
| F. response-mode selector | Could select compact answer shapes for reviewer notes, go/no-go decisions, and constrained summaries. | May become hidden routing or policy selection and can overlap with unapproved behavioral routing. | Response-mode docs/specs now; selector code only if later approved. | Mode selection golden tests, no invented scaffolding tests, and routing non-change verification. | Not ready. | Keep as future planning; do not implement yet. |
| G. selective engagement gate prototype | Could preserve Alpha-style lift on high-headroom prompts while avoiding over-answering on low-headroom prompts. | Highest risk because it can overlap provider orchestration, routing, model selection, and live-call behavior. | Selective engagement planning docs only unless a later lane explicitly approves code. | Gate fixture tests, false-positive/false-negative tests, routing/provider non-change checks, and no live provider calls. | Blocked for implementation. | Do not implement in the next lane. |

See also `minimal-implementation-decision-matrix.csv` for the same path comparison in CSV form.

## 6. Recommended minimal path

Recommended sequence:

1. First create offline golden tests and a behavior-contract wording proposal.
2. Use those tests to cover short-answer-first behavior, no invented scaffolding, claim-boundary safe wording, evidence boundaries, artifact stop conditions, and strict non-claims.
3. Then consider minimal prompt/protocol wording changes only after the tests and behavior contract are reviewed.
4. Do not touch provider adapters, model configuration, routing, `/v1/solve`, scoring rubrics, scored artifacts, capture scripts, Google Sheet integrations, or selective engagement gates yet.

The immediate next implementation proposal should be narrow enough that it can merge without changing provider/model/routing behavior.

## 7. Files allowed for next implementation proposal

Likely allowed surfaces for the next proposal, subject to explicit operator approval:

- `tests/golden` or other offline tests/fixtures that do not call live providers.
- `docs/specs`, `.specs/`, or other behavior-contract documentation.
- `alpha_solver_portable.py` only if explicitly approved and only for the narrow approved behavior-contract or prompt-text surface.
- Prompt/protocol text only if explicitly approved and guarded by offline tests.

## 8. Protected files

Protected surfaces for the next implementation proposal:

- Provider adapters and provider request/response helpers.
- Model configuration and model selection files.
- Routing, solver selection, and engagement-routing logic.
- `/v1/solve` API behavior and request/response contract.
- Scoring rubric and scoring procedure files.
- Official scored artifacts, score tables, blinded score sheets, defects records, and blinding maps.
- Capture scripts and live-provider capture workflows.
- Google Sheet integrations and backlog workbook update paths.
- Secrets, environment config, API keys, and credential/config files.

## 9. Required tests before implementation merge

Before any behavior implementation merges, the next lane should define and pass offline tests for:

- Short-answer-first golden behavior.
- No invented scaffolding: no invented roles, owners, timelines, files, commands, metrics, acceptance criteria, or process stages when not supplied or requested.
- Claim-boundary safe wording.
- Evidence-boundary behavior under limited or conflicting evidence.
- Artifact stop-condition behavior for official scored artifacts and raw evidence records.
- No validation, superiority, production-readiness, benchmark-success, exact-billing, broad-runtime-readiness, or provider-reasoning-orchestration claims.
- No live provider calls.

## 10. Implementation PR recommendation

Recommended next lane: `ALPHA-MINIMAL-BEHAVIOR-CONTRACT-AND-TESTS-001`.

This should be test-first and contract-first. It should not touch provider/model/routing behavior. It should create offline golden tests and behavior-contract wording before any prompt/protocol behavior change is proposed.

## 11. Not authorized

This review does not authorize:

- Runtime/provider/model/routing changes yet.
- `/v1/solve` changes.
- Batch C.
- New capture.
- Live provider calls.
- Rescoring.
- Scoring rubric changes.
- Google Sheet updates.
- Production readiness work.
- Public validation claims.

## 12. Non-claims

This artifact makes these strict non-claims:

- No MVP validation.
- No Alpha Solver superiority generally.
- No broad plain-provider inferiority.
- No answer-quality superiority generally.
- No production readiness.
- No broad runtime readiness.
- No benchmark success.
- No exact billing accuracy.
- No provider reasoning orchestration.

## Validation performed for this review

Validation expected for this lane:

- Confirm all referenced artifacts exist.
- Recompute A3-1 and Batch B score math from committed score tables.
- Confirm the review contains strict non-claims rather than forbidden positive claims.
- Confirm no runtime/provider/model/routing/scoring files changed.
- Run `git diff --check`.
- Run focused docs/eval tests if safe.
- Do not run live-provider tests.
