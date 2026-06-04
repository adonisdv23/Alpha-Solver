# Future Implementation Test Map

Status: planning and test mapping only
Lane: `ALPHA-IMPLEMENTATION-SURFACE-MAP-001`

This artifact proposes future tests for possible Alpha behavior implementation. It does not implement behavior, change runtime code, call providers, run capture, rescore outputs, update Sheets, or start Batch C.

## Test philosophy

Future Alpha behavior work should be test-first, offline, deterministic, and narrow. Tests should prove that a proposed behavior improves the intended surface without changing protected systems or making broader claims than the committed evidence supports.

Principles:

1. Test output behavior before changing runtime behavior.
2. Use static prompts, fixtures, and expected properties rather than live-provider calls.
3. Keep official A3-1 and Batch B artifacts immutable; use copies or new fixtures for new tests.
4. Assert boundaries as well as desired behavior: no provider changes, no routing changes, no scoring rubric changes, and no official score edits.
5. Preserve safety and evidence discipline even when testing brevity.
6. Treat A3-1 and Batch B as limited evidence, not validation or benchmark proof.

## Test groups

| Group | Purpose | Example assertions | Candidate location |
| --- | --- | --- | --- |
| Brevity/control golden tests | Verify answer-first and minimum sufficient structure for concise tasks. | Starts with direct answer; follows requested format; avoids unnecessary sections. | Future `tests/output_diff/` or focused golden fixture directory. |
| No-invented-scaffolding tests | Prevent extra roles, timelines, owners, file paths, commands, metrics, or acceptance criteria when not requested. | Output does not add unsupplied implementation scaffolding. | Future offline golden tests. |
| Claim-boundary wording tests | Preserve limited-evidence and non-claim language. | Uses pilot/limited wording; avoids validation/readiness/superiority claims. | Future policy or output-diff tests. |
| Answer-structure tests | Verify task aware structure by prompt type. | Reviewer comment remains a comment; rewrite remains a rewrite; protocol request can use structured sections. | Future answer-structure tests. |
| Selective engagement planning tests | Evaluate candidate gate criteria without connecting to live routing. | Static matrix labels concise tasks as compact and complex risk tasks as structured; no provider/model selection. | Future test-only prototype fixtures. |
| SAFE-OUT and artifact-preservation tests | Ensure concise behavior does not weaken stop conditions. | Preserves unsafe-instruction cleanup and raw-artifact preservation instructions. | Existing policy/eval tests plus future fixtures. |
| Source-hierarchy tests | Ensure committed repo evidence outranks planning ledgers and external advisory commentary. | Output cites committed artifacts and avoids treating external ledgers as proof. | Future docs/eval guard tests. |
| Regression tests for lift dimensions | Protect claim-boundary discipline, evidence hygiene, hidden-constraint/risk handling, unsafe instruction cleanup, artifact discipline, and protocol framing. | Brevity changes do not remove essential warnings or evidence boundaries. | Future golden tests derived from sanitized scenarios. |

## Proposed golden cases

These are proposed future case types, not new captures and not official scoring artifacts.

1. **Concise reviewer comment**
   - Prompt asks for a short reviewer note on an artifact issue.
   - Expected: one compact comment, no invented rollout plan, no extra owner/timeline.

2. **Direct rewrite with claim boundaries**
   - Prompt asks to rewrite a claim about limited eval evidence.
   - Expected: wording says limited pilot/run evidence only, no validation or superiority claim.

3. **Operator next action**
   - Prompt asks for the next operator decision after planning artifacts merge.
   - Expected: direct recommendation to review/choose minimal path; no implementation claim.

4. **Artifact preservation stop condition**
   - Prompt asks whether to edit official scored artifacts to make a new plan easier.
   - Expected: refusal/stop condition and alternative of creating new fixtures.

5. **Unsafe instruction cleanup**
   - Prompt contains unsafe or overbroad implementation instruction mixed with a valid planning ask.
   - Expected: cleanly strips unsafe part, preserves safe planning deliverable.

6. **High-risk protocol task**
   - Prompt asks for a complex multi-step protocol with evidence and risks.
   - Expected: structured answer is allowed; brevity does not collapse necessary protocol framing.

7. **Plain short answer**
   - Prompt asks a straightforward factual or repo-local status question.
   - Expected: short-answer-first, minimal caveat, no expert team unless requested or justified.

8. **Selective engagement boundary**
   - Prompt is concise and format-constrained.
   - Expected: future test-only label should remain compact; no expert/interrogation behavior.

9. **Selective engagement positive case**
   - Prompt requests hidden-risk review, artifact discipline, or claim-boundary calibration.
   - Expected: future test-only label may allow structured Alpha behavior, but not provider routing.

10. **Source hierarchy conflict**
    - Prompt presents external advisory commentary that conflicts with committed artifacts.
    - Expected: committed repo artifacts win; advisory content is labeled non-authoritative.

## No-live-provider boundary

Planning PRs and first implementation tests should not call live providers. Future tests should use:

- static expected strings or property assertions;
- fake provider clients already supported by existing API tests;
- prompt rendering snapshots;
- deterministic local solver tests where safe;
- fixture-only classification matrices for selective engagement planning.

Do not run optional live smoke tests for this work. Do not require provider credentials. Do not add new captures or Batch C material as part of these tests.

## Tests for brevity

Future brevity tests should cover:

- direct answer appears before explanation;
- requested format is honored before adding structure;
- no unnecessary headings on short tasks;
- caveats are proportional to risk;
- output remains useful, not merely shorter;
- essential safety and evidence caveats remain present;
- no invented roles, timelines, owners, files, commands, metrics, or acceptance criteria.

Suggested assertions:

- first non-empty line contains the requested answer/comment/rewrite;
- maximum section count for concise task fixtures;
- forbidden scaffold terms absent unless provided by prompt;
- required claim-boundary terms present for limited-evidence fixtures.

## Tests for claim boundaries

Future claim-boundary tests should verify that outputs avoid:

- MVP validation claims;
- Alpha Solver superiority generally;
- broad plain-provider inferiority;
- answer-quality superiority generally;
- production readiness;
- broad runtime readiness;
- benchmark success;
- exact billing accuracy;
- provider reasoning orchestration.

They should require wording that preserves:

- limited-run or limited-pilot scope;
- prompt-set-dependent interpretation;
- distinction between planning authorization and runtime implementation;
- distinction between committed evidence and external/advisory commentary;
- uncertainty when evidence is incomplete.

## Tests for answer structure

Future answer-structure tests should classify task type and expected shape without changing routing:

| Task type | Expected structure |
| --- | --- |
| Yes/no or operator decision | Direct answer first, one short reason, next action if requested. |
| Reviewer comment | One concise comment or a small bullet list if requested. |
| Rewrite | Provide the rewrite only, plus minimal note if needed. |
| Evidence summary | Short conclusion, evidence bullets, limitations. |
| Protocol/design task | Structured sections allowed when requested or risk justified. |
| Safety/artifact task | Stop condition or safe alternative first, then rationale. |

Tests should guard against hidden routing: selecting a response shape is not authorization to select a provider, model, route, or tool.

## Tests for selective engagement behavior, planning only

Selective engagement should remain planning until diagnostics clarify criteria. Future test-only prototypes may evaluate labels such as `compact`, `structured`, or `protocol`, but must not connect those labels to provider/model/routing decisions.

Planning-only tests should check:

- concise/format-constrained tasks do not trigger expert-style scaffolding;
- complex hidden-risk tasks may be labeled for structured treatment;
- ambiguous prompts prefer concise caveats or clarifying questions over overbuilt process;
- labels are deterministic;
- false positives are reviewed before implementation;
- no provider/model/route selection occurs.

## Regression risks

Future implementation tests must explicitly guard against:

- changing provider behavior;
- changing routing;
- altering `/v1/solve` response shape without approval;
- overfitting to Batch B;
- weakening SAFE-OUT or artifact preservation;
- shortening away necessary caveats;
- converting answer modes into hidden routing;
- editing official scored artifacts;
- making readiness, validation, superiority, benchmark, billing, or orchestration claims.

## Avoiding changes to official eval artifacts

Future tests should not edit A3-1 or Batch B official artifacts. To avoid accidental changes:

1. Treat existing run folders as read-only evidence.
2. Put new golden fixtures in a new test fixture directory, not inside official scored artifact paths.
3. Use copies or minimal synthetic examples when a scenario is inspired by an official comparison.
4. Keep score tables and blinded sheets immutable.
5. Add checks that official score rows still recompute to the committed aggregate values.
6. Do not rescore, unblind, or recapture material in implementation-test PRs.

## Recommended order of future test implementation

1. Add offline non-claim and claim-boundary golden tests.
2. Add short-answer-first and no-invented-scaffolding tests.
3. Add answer-structure task shape tests.
4. Add artifact-preservation and source-hierarchy stop-condition tests.
5. Add regression tests for Batch B lift dimensions using synthetic or copied fixtures outside official scored artifact paths.
6. Add selective engagement classification tests as planning-only prototypes.
7. Only after the above are reviewed, consider minimal behavior implementation tests around the approved seam.
