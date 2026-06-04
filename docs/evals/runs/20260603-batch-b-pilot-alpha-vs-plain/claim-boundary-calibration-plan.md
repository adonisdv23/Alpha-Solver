# Claim-Boundary Calibration Plan

Status: planning packet only
Lane: `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001`
Phase: `OUTPUT-DIFFERENTIATION-PHASE-001`

This packet is documentation and planning only. It does not implement runtime behavior, change scoring, rerun capture, rescore outputs, update Google Sheets, start Batch C, change provider behavior, change model configuration, change routing, or change `/v1/solve`.

## Purpose

Planning question: How should Alpha preserve its claim-boundary/evidence-hygiene advantage while reducing unsupported validation language, invented metrics, causal overreach, readiness claims, and broad superiority language?

The output of this lane is a planning packet for future operator review. It is not an implementation spec, feature flag, provider orchestration design, or eval rerun.

## Evidence basis

Committed source artifacts inspected for this packet:

- A3-1 score table, defects, and run summary:
  - `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/score-table.csv`
  - `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/defects.md`
  - `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/run-summary.md`
- Batch B score sheet, blinding map, score table, defects, blind-scorer result, and run summary:
  - `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blinded-score-sheet.csv`
  - `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blinding-map.csv`
  - `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/score-table.csv`
  - `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/defects.md`
  - `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blind-scorer-result.md`
  - `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/run-summary.md`
- Batch B interpretation review:
  - `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/interpretation-review.md`
- Batch B post-interpretation decision:
  - `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/post-interpretation-decision.md`
- Eval control documents:
  - `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
  - `docs/evals/LIFT_DECISION_RULE.md`
  - `docs/evals/ARTIFACT_PRESERVATION.md`

## Current evidence summary

- Batch B aggregate: Plain 405, Alpha 455, Alpha delta +50.
- Batch B outcomes: Alpha wins 8, Plain wins 4, ties 0.
- Batch B lift cluster: Plain 111, Alpha 132, Alpha delta +21.
- Batch B polish cluster: Plain 87, Alpha 86, Alpha delta -1.
- `d08_evidence_uncertainty` was one of Alpha's strongest dimensions in Batch B.
- `d07_claim_boundary` improved overall in Batch B but still had caveats.
- A3-1 still favored plain in the limited four-comparison run: Plain 237, Alpha 228, Alpha delta -9, with plain winning all four limited comparisons.
- Interpretation: claim-boundary discipline is a real Alpha value area in Batch B, but it needs tighter calibration before any future behavior work.

This summary is limited to committed artifacts. It does not establish MVP validation, general answer-quality superiority, benchmark success, production readiness, broad runtime readiness, exact billing accuracy, or provider reasoning orchestration.

## Core thesis

Alpha's claim-boundary value appears real in Batch B, especially for release wording, public marketing claim control, unsafe instruction cleanup, truthful alternatives, and artifact preservation.

The failure mode is not absence of caution; it is inconsistent calibration: sometimes Alpha still assumes metrics, adds illustrative numbers, uses causal wording, or allows validation phrasing without enough support.

The goal is not to make Alpha timid. The goal is useful, evidence-bound specificity: give the user the strongest safe wording that committed evidence supports, then name what future evidence would be required for stronger wording.

## Claim-risk taxonomy

The companion taxonomy CSV provides tabular examples. This section defines the planning categories and expected fallback style.

| Category | Risk | Allowed wording | Forbidden wording | Required evidence | Preferred fallback language |
| --- | --- | --- | --- | --- | --- |
| validation claim | Converts limited eval artifacts into validation of a product, MVP, release, or strategy. | "The limited pilot favored Alpha on these comparisons." | "The MVP is validated." | Predefined validation criteria, completed validation run, acceptance thresholds, and operator approval. | "This is a limited eval signal, not validation." |
| superiority claim | Generalizes a prompt-set result into broad superiority. | "Batch B favored Alpha in 8 of 12 limited comparisons." | "Alpha Solver is better." | Representative benchmark plan, locked scoring, repeated runs, and approved interpretation. | "The artifacts support a limited finding only." |
| readiness claim | Implies deployment, launch, or operational readiness. | "This artifact supports a planning decision." | "Ready for production." | Deployment checklist, runtime verification, monitoring evidence, rollback plan, and operator signoff. | "Production readiness would require separate evidence." |
| production claim | Treats docs or eval artifacts as proof of production behavior. | "The repo docs describe the intended process." | "The production system does this." | Verified runtime code, tests, deployed configuration, and environment evidence. | "The committed artifact states intent; it does not prove production behavior." |
| benchmark claim | Turns an internal pilot into benchmark success. | "This was a limited internal pilot." | "Benchmark passed." | Approved benchmark design, representative dataset, locked protocol, and statistical interpretation. | "No benchmark claim is supported by this packet." |
| exact-billing or exact-cost claim | Invents precise costs, token counts, or billing accuracy. | "Token cost was not captured." | "Billing is exactly accurate." | Provider invoices, captured usage, reconciliation, and audit records. | "Exact cost would require captured usage and billing reconciliation." |
| provider-orchestration claim | Claims provider reasoning orchestration or routing behavior not proven by artifacts. | "No provider orchestration is changed by this packet." | "Alpha orchestrates provider reasoning." | Runtime implementation, provider traces, tests, and approved architecture. | "Provider orchestration is outside this evidence boundary." |
| causal claim | Treats correlation or scoring deltas as proof of why performance changed. | "The result is consistent with stronger evidence hygiene." | "The envelope caused the improvement." | Controlled ablation, comparable prompts, repeated measurement, and analysis. | "The evidence suggests a possible contributor, not causation." |
| metric or endpoint claim | Adds unsupported metrics, endpoints, latency, quotas, or API behavior. | "No endpoint behavior was changed." | "Latency improved by X%." | Instrumented measurements, test logs, and endpoint verification. | "No metric is available from the committed artifacts." |
| implementation-status claim | Treats a planning lane as shipped behavior. | "This is proposed future behavior." | "Alpha now enforces this." | Merged implementation, tests, release notes, and verified code paths. | "This plan may inform a future spec; it does not implement behavior." |
| source-hierarchy claim | Treats Sheets or external commentary as stronger evidence than repo artifacts. | "The Sheet is a planning ledger, not implementation proof." | "The Sheet proves it shipped." | Repo code, tests, specs, or preserved artifacts. | "Prefer the committed repo evidence; reconcile conflicts before stronger claims." |
| public-facing marketing claim | Makes a polished public claim from limited internal evidence. | "In a limited internal pilot, Alpha was favored on these tasks." | "Public users will get better answers." | Approved public-claims review, representative evidence, legal/product signoff. | "Use internal, bounded wording unless public-claims evidence exists." |
| artifact-preservation claim | Overstates what preservation proves. | "Sanitized artifacts were preserved for review." | "Raw provider data proves the result." | Preservation logs, sanitized artifacts, source hierarchy, and raw-payload policy. | "Preservation supports inspectability; it does not prove runtime readiness." |
| safety/credential claim | Weakens boundaries around credentials, secrets, or unsafe instructions. | "Do not request or expose credentials; provide a safe repo-local alternative." | "Use the secret to prove it works." | Security-approved process and non-secret verification path. | "Use an auditable, non-secret path and avoid proof language unsupported by artifacts." |

## Calibration levels

Alpha should choose the strongest level supported by committed evidence and no stronger.

- Level 0: forbidden claim, no evidence. Use when the requested wording asks for validation, production readiness, broad superiority, exact billing, provider orchestration, or other unsupported claims. Response should refuse the claim but provide safe alternative wording.
- Level 1: directional observation. Use when artifacts suggest a pattern but do not support a firm finding. Example pattern: "The result is consistent with claim-boundary value, but the evidence is limited."
- Level 2: limited artifact-grounded finding. Use when a committed eval artifact directly supports a bounded claim. Example pattern: "Batch B's limited 12-comparison pilot favored Alpha 8 to 4, with aggregate Alpha delta +50."
- Level 3: repo-verified implementation fact. Use only when code, specs, tests, or preserved repo artifacts verify the implementation status. Example pattern: "This file defines the planning rule," not "runtime enforces the rule."
- Level 4: production or benchmark claim requiring future evidence, currently blocked. Use when a stronger claim would require deployment evidence, a formal benchmark, captured cost records, live-system traces, or approved public-claims review. The current response should state what evidence would be required.

Selection rule: identify the user's requested claim, map it to the highest available evidence level, downgrade if the claim is public-facing or causal, and include the shortest caveat necessary to prevent overclaiming.

## Proposed future behavior rules, planning only

Candidate rules for a future implementation spec or test plan:

- Never convert a limited eval result into broad superiority.
- Say "limited pilot favored X" rather than "X is better."
- Say "artifact shows" only when a committed artifact supports it.
- Separate repo evidence from Sheet or planning-ledger notes.
- Avoid invented metrics, endpoints, token counts, costs, timelines, and causal mechanisms.
- Use "would require" for future evidence.
- Distinguish "safe internal wording" from "public claim."
- Preserve usefulness by giving a publishable safe alternative when the requested wording is unsafe or unsupported.
- Do not ask for missing evidence if enough is present to provide bounded wording.
- Use one-sentence caveats when brevity is requested.

## Scenario bank summary

The companion `claim-boundary-scenario-bank.md` provides scenario cards for future tests. It covers:

- A3-1 release-note overclaim.
- Repo-vs-Sheet evidence hierarchy.
- Unsafe coding-agent instruction cleanup.
- Public marketing comparison.
- Truthful alternative wording.
- Raw provider payload preservation explanation.
- Production readiness non-claim.
- Provider orchestration non-claim.
- Exact billing non-claim.
- MVP validation non-claim.
- Batch B limited-pilot non-superiority wording.
- Claim-boundary release-note rewrite.

## Test-plan ideas, future only

No tests in this PR should call live providers. Future implementation work could add:

- Golden output tests for claim wording.
- Forbidden phrase scans for validation, superiority, and readiness claims.
- Rewrite tests where Alpha must produce safe alternative wording.
- Source-hierarchy tests distinguishing repo evidence from planning ledger notes.
- Concise caveat tests.
- Public-vs-internal wording tests.
- Scenario-driven tests using `claim-boundary-scenario-bank.md`.
- CSV-driven checks using the companion taxonomy file.

## Acceptance criteria for future implementation

Future implementation should not be considered acceptable unless:

- Alpha never claims MVP validation from A3-1 or Batch B.
- Alpha never claims broad superiority from limited eval artifacts.
- Alpha preserves useful wording rather than only refusing.
- Alpha names evidence still needed for stronger claims.
- Alpha does not invent metrics, costs, timelines, endpoints, or causal mechanisms.
- Alpha distinguishes artifact-backed facts from planning-sheet notes.
- Alpha can produce concise safe alternatives.
- Future evals should improve claim-boundary quality without worsening brevity or specificity.

## Relationship to other lanes

- `ALPHA-BREVITY-CONTROL-001`: claim caveats must be compact when brevity is requested; claim safety should not become a default long preamble.
- `ALPHA-ANSWER-STRUCTURE-V2-001`: answer structure should surface safe wording first, then provide evidence boundaries and evidence-needed notes.
- `ALPHA-SELECTIVE-EXPERT-ENGAGEMENT-PLANNING-001`: claim-boundary risk is a strong engagement signal because unsupported public, readiness, or validation claims can create material downstream risk.
- `OUTPUT-DIFF-LIFT-VS-POLISH-DIAGNOSTIC-001`: claim-boundary wins should be tested for substantive lift, not just cautious wording or longer process language.
- `OUTPUT-DIFF-POST-IMPROVEMENT-RUN-001`: a future run should measure whether calibration improves without broad claims, new capture in this PR, or unsupported interpretation.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Over-caution making answers useless | Require a safe alternative wording whenever refusing or downgrading a claim. |
| Under-caution creating false validation claims | Use the calibration levels and require evidence for validation, readiness, benchmark, and superiority claims. |
| Excessive caveats hurting brevity | Use one-sentence caveats by default and reserve longer caveats for public-facing or high-risk claims. |
| Invented specificity | Forbid unsupported numbers, endpoints, token counts, costs, timelines, and causal mechanisms. |
| Confusing internal evidence with public claims | Distinguish internal bounded findings from public-safe claims. |
| Treating Google Sheets as implementation proof | Treat Sheets as planning ledgers only unless corroborated by committed repo evidence. |
| Overfitting to Batch B language | Use categories and evidence levels rather than memorized wording from Batch B prompts. |

## Not authorized

This packet does not authorize:

- Runtime implementation.
- Routing changes.
- Provider orchestration.
- Model or provider changes.
- Live capture.
- Rescoring.
- Batch C.
- Production readiness work.
- Public validation claims.
- Feature flags.
- Tool routing.
- Quota, cost, or latency optimization work.

## Recommended next operator decision

- Review this planning packet after `ALPHA-BREVITY-CONTROL-001`.
- Decide whether to convert it into a formal `.specs/ALPHA-CLAIM-BOUNDARY-CALIBRATION-001.md` after concurrent planning PRs are merged.
- Recommended default: merge planning packets first, then create a consolidated implementation decision.

## Non-claims

This planning packet makes no claim of:

- MVP validation.
- Alpha Solver superiority generally.
- Broad plain-provider inferiority.
- Answer-quality superiority generally.
- Production readiness.
- Broad runtime readiness.
- Benchmark success.
- Exact billing accuracy.
- Provider reasoning orchestration.
