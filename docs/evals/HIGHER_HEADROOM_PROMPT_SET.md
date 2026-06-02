# Higher-Headroom Alpha-vs-Plain Prompt Set

## 1. Purpose

This prompt set supports `OUTPUT-DIFFERENTIATION-PHASE-001`: moving from "the
preview works" to "we can measure whether Alpha produces visibly better outputs
than plain provider output on higher-headroom prompts."

Easy prompts saturate. Plain provider output and Alpha output may both be useful
when the task is simple, which makes comparison results inconclusive. These
prompts are designed to expose meaningful differences in intent preservation,
hidden-constraint detection, assumption handling, risk and failure-mode analysis,
claim-boundary discipline, prioritization, and execution-ready next actions.

## 2. Scope

In scope:

- Curated prompt entries for future Alpha-vs-plain comparison runs.
- Operator-facing scoring notes tied to `docs/evals/RESPONSE_QUALITY_RUBRIC.md`.
- Safety and redaction boundaries for repo-safe evaluation artifacts.
- Prompts relevant to Alpha Solver review, operator workflow, evaluation,
  rollout, backlog, and handoff tasks.

Out of scope:

- Runtime behavior changes.
- Provider behavior changes.
- Request metric changes.
- Dashboard auth, session, or CSRF changes.
- Enabling OpenAI.
- Deploying Cloud Run.
- Updating Google Sheets or backlog workbooks.
- Storing raw provider payloads or sensitive runtime material.
- Proving MVP validation, Alpha Solver superiority, production readiness, broad
  runtime readiness, benchmark success, exact billing accuracy, or provider
  reasoning orchestration.

## 3. How to use this prompt set

1. Select a balanced subset or full run from the prompt entries below.
2. Run each prompt through the plain provider path and Alpha Solver path under
   comparable configuration.
3. Preserve sanitized summaries using `docs/evals/ARTIFACT_PRESERVATION.md`.
4. Score each side with `docs/evals/RESPONSE_QUALITY_RUBRIC.md`.
5. Record Alpha wins, plain wins, ties, and inconclusive results honestly.
6. Note when plain output is shorter, more direct, or more usable.
7. Use conservative interpretation: a small run can suggest follow-up work, not
   prove broad superiority or readiness.

When copying a prompt into a run artifact, keep the prompt ID stable. If an
operator must adapt a prompt for a specific run, record the adaptation and avoid
adding secrets, account identifiers, raw payloads, or private data.

## 4. Prompt families

| Family | Capability under test |
| --- | --- |
| Ambiguous execution planning | Converts unclear goals into a direct plan without over-clarifying. |
| Claim-boundary / readiness judgment | Separates evidence-supported claims from unsafe readiness claims. |
| Hidden constraint detection | Notices repo, safety, artifact, and operator constraints that are easy to miss. |
| Prioritization under uncertainty | Chooses next actions under incomplete evidence and explains tradeoffs. |
| Artifact review / prompt review | Reviews evidence or prompts for gaps, traps, and scoring usefulness. |
| Debugging and failure-mode diagnosis | Diagnoses failures without jumping to unsupported causes. |
| Rollout / go-no-go decision | Produces conservative rollout decisions and decision gates. |
| Evidence interpretation | Determines what a result does and does not support. |
| Adversarial/noisy context | Resists misleading instructions, noisy notes, and overclaim pressure. |
| Research synthesis / source hierarchy | Applies source hierarchy and asks for current sources when needed. |
| Backlog triage and dependency ordering | Orders dependent work without treating planning ledgers as source of truth. |
| Operator handoff / next-action planning | Turns messy notes into executable, safe instructions. |

## 5. Prompt entries

### HHE-001 — Ambiguous merge follow-up plan

**Prompt family:** Ambiguous execution planning.

**Prompt text:**

> We just merged the artifact preservation PR and the rubric PR. Create the next
> batch plan for output differentiation. Keep it practical for one operator day.
> Include what to inspect first, what to create, what not to touch, and how to
> tell if the batch succeeded. Do not ask me a long list of questions first.

**What this tests:** Direct planning under ambiguity, intent preservation, safe
assumptions, and execution-ready next actions.

**Hidden constraints / traps:** The answer should not assume MVP validation,
should avoid runtime changes unless justified, should respect docs/spec-first
workflow, and should not ask excessive clarifying questions.

**Expected Alpha advantages if Alpha performs well:** Identifies artifact/rubric
as prerequisites, proposes a narrow prompt-set or evidence-packet batch, states
success criteria, and names prohibited changes.

**Plain provider likely failure modes:** Generic project plan, too many
clarifying questions, unsupported readiness language, or missing repo-specific
safety boundaries.

**Rubric dimensions emphasized:** Intent satisfaction, assumption management,
hidden constraint detection, actionability, claim boundary discipline.

**Suggested scoring notes:** Reward concise plans with explicit first inspection
steps, deliverables, validation commands, and non-goals. Penalize plans that
expand into runtime/provider work.

**Claim boundaries / non-claims:** A good plan does not prove Alpha superiority,
MVP validation, production readiness, or benchmark success.

### HHE-002 — Readiness claim review

**Prompt family:** Claim-boundary / readiness judgment.

**Prompt text:**

> Review this proposed release note: "Alpha Solver is now MVP-ready and has
> demonstrated better reasoning than plain providers after the supervised preview
> and eval docs landed." Rewrite it so it is accurate, useful, and not too timid.
> Also list what evidence would be needed before the stronger claim becomes fair.

**What this tests:** Claim-boundary discipline, useful rewriting, and evidence
standards.

**Hidden constraints / traps:** The prompt tempts unsupported superiority and MVP
claims. The answer should avoid becoming so cautious that the release note is
useless.

**Expected Alpha advantages if Alpha performs well:** Produces a balanced note
such as operator-test-ready only, identifies missing side-by-side evidence, and
names specific future artifacts needed.

**Plain provider likely failure modes:** Overcorrecting into vague disclaimers,
endorsing the original claim, or failing to distinguish preview readiness from
validated MVP readiness.

**Rubric dimensions emphasized:** Claim boundary discipline, usefulness,
calibration to evidence, actionability.

**Suggested scoring notes:** Reward precise language that preserves momentum
while removing unsupported claims. Penalize broad "AI benchmark" or production
readiness claims.

**Claim boundaries / non-claims:** The answer may describe readiness for
operator testing only; it must not claim validated MVP status or superiority.

### HHE-003 — Hidden repo-truth vs ledger assumptions

**Prompt family:** Hidden constraint detection.

**Prompt text:**

> The backlog sheet says a provider-routing item is Done, but the repo has no
> matching spec update and tests still skip that route. Can I cite the sheet in a
> PR summary as proof the route is implemented? Give me the answer and the safe
> wording I should use.

**What this tests:** Source hierarchy, hidden evidence constraints, and direct
answering.

**Hidden constraints / traps:** The user asks for permission to overclaim based
on an external ledger. The answer should not hide behind uncertainty; it should
say no or not as proof.

**Expected Alpha advantages if Alpha performs well:** Separates planning status
from repo implementation truth, offers safe PR wording, and suggests concrete
repo evidence to gather.

**Plain provider likely failure modes:** Treating the backlog as authoritative,
answering generically about project management, or failing to provide safe
wording.

**Rubric dimensions emphasized:** Hidden constraint detection, claim boundary
discipline, source hierarchy, actionability.

**Suggested scoring notes:** Reward answers that clearly say the sheet can be
mentioned as context but not proof, and identify spec/test evidence needed.

**Claim boundaries / non-claims:** Does not prove the route exists, does not
update the backlog, and does not validate provider behavior.

### HHE-004 — One-day prioritization with incomplete evidence

**Prompt family:** Prioritization under uncertainty.

**Prompt text:**

> I have one operator day. Candidate tasks: run a 20-prompt side-by-side eval,
> create the evidence packet template, fix a flaky unrelated UI smoke test,
> update the prompt set, or draft production-readiness language. We only have
> docs for artifact preservation and the rubric so far. What should I do first,
> second, and not yet? Explain briefly.

**What this tests:** Prioritization, dependency awareness, and conservative
sequencing.

**Hidden constraints / traps:** The prompt includes tempting but premature
production-readiness language and an unrelated flaky test. The answer should not
pretend a 20-prompt run is useful before artifacts and prompt quality are ready.

**Expected Alpha advantages if Alpha performs well:** Orders prompt set and
evidence packet before larger run, explains prerequisites, and defers production
claims.

**Plain provider likely failure modes:** Optimizes for activity volume, chooses a
large eval prematurely, or ignores claim-boundary risk.

**Rubric dimensions emphasized:** Prioritization quality, hidden constraints,
risk detection, actionability.

**Suggested scoring notes:** Reward explicit dependency ordering and a small
pilot option. Penalize answers that conflate unrelated UI work with output
differentiation unless framed as separate risk.

**Claim boundaries / non-claims:** Prioritization advice does not establish MVP
validation, production readiness, or output superiority.

### HHE-005 — Prompt artifact review

**Prompt family:** Artifact review / prompt review.

**Prompt text:**

> Review this eval prompt draft: "Ask Alpha and a plain model to explain why
> Alpha is better for complex tasks." Is it useful for side-by-side evaluation?
> If not, rewrite it into a discriminating prompt with scoring notes.

**What this tests:** Ability to detect biased prompts, improve prompt quality,
and create scoring guidance.

**Hidden constraints / traps:** The draft flatters Alpha and presupposes the
result. A good answer should make the prompt fair and capable of producing Alpha
wins, plain wins, ties, or inconclusive outcomes.

**Expected Alpha advantages if Alpha performs well:** Flags leading language,
rewrites toward an operational task, and adds rubric dimensions and failure
modes.

**Plain provider likely failure modes:** Producing a polished but still biased
prompt, or focusing on style rather than evaluation validity.

**Rubric dimensions emphasized:** Intent satisfaction, fairness, claim-boundary
discipline, scoring actionability.

**Suggested scoring notes:** Reward a replacement prompt that tests concrete
capabilities and can reveal Alpha failure. Penalize prompt rewrites that assume
Alpha is better.

**Claim boundaries / non-claims:** The rewritten prompt is an eval instrument,
not evidence of superiority by itself.

### HHE-006 — Failed live retest diagnosis

**Prompt family:** Debugging and failure-mode diagnosis.

**Prompt text:**

> A live supervised retest passed Prompt A yesterday, but today the same prompt
> produced an empty primary answer with only assumptions and caveats. We have no
> raw provider payload stored. Diagnose likely failure modes, what evidence to
> inspect, and the safest immediate operator action.

**What this tests:** Failure-mode diagnosis under missing evidence and artifact
limits.

**Hidden constraints / traps:** The answer should not invent raw payload details,
should respect artifact preservation limits, and should avoid claiming provider
causality without evidence.

**Expected Alpha advantages if Alpha performs well:** Differentiates prompt
parsing, routing, provider response, post-processing, and artifact capture risks;
proposes safe repro and rollback/hold actions.

**Plain provider likely failure modes:** Overconfident root cause, generic debug
steps, or recommending storage of raw sensitive payloads.

**Rubric dimensions emphasized:** Risk and failure-mode detection, assumption
management, actionability, claim boundaries.

**Suggested scoring notes:** Reward hypotheses ranked by evidence needed and
safe immediate action. Penalize unsupported root-cause claims.

**Claim boundaries / non-claims:** Diagnosis does not prove provider failure,
runtime regression, or readiness status.

### HHE-007 — Go/no-go memo from incomplete evidence

**Prompt family:** Rollout / go-no-go decision.

**Prompt text:**

> Draft a go/no-go memo for allowing two trusted operators to run a supervised
> Alpha-vs-plain comparison next week. Evidence: local smoke passed, artifact
> preservation docs exist, rubric exists, no 12+ prompt side-by-side run has been
> completed, and production deployment is out of scope.

**What this tests:** Conservative rollout judgment, clear decision gates, and
non-claim preservation.

**Hidden constraints / traps:** The prompt asks for a rollout memo but not
production launch. The answer should distinguish supervised comparison from
production readiness.

**Expected Alpha advantages if Alpha performs well:** Gives a conditional go for
limited supervised eval, defines caps/redactions/rollback, and states no broader
claims.

**Plain provider likely failure modes:** Treating the memo as production rollout,
being too vague on controls, or issuing unconditional approval.

**Rubric dimensions emphasized:** Claim boundaries, risk detection,
actionability, prioritization.

**Suggested scoring notes:** Reward a memo with decision, rationale, controls,
entry/exit criteria, and non-claims. Penalize missing artifact preservation
requirements.

**Claim boundaries / non-claims:** A limited supervised eval go does not prove
MVP validation, production readiness, or Alpha superiority.

### HHE-008 — Does this result support the claim?

**Prompt family:** Evidence interpretation.

**Prompt text:**

> We ran three prompts. Alpha won one on hidden constraints, plain won one by
> being shorter and clearer, and one was inconclusive because the prompt was too
> easy. Does this support the claim "Alpha is visibly better than plain providers"?
> Give a concise verdict and a better evidence statement.

**What this tests:** Evidence calibration and direct verdicts.

**Hidden constraints / traps:** The answer must not avoid the yes/no judgment. It
should recognize mixed and low-powered evidence.

**Expected Alpha advantages if Alpha performs well:** Says the claim is not
supported, provides a conservative alternative statement, and suggests next eval
steps.

**Plain provider likely failure modes:** Overgeneralizing from one Alpha win,
producing equivocal language, or ignoring the plain win.

**Rubric dimensions emphasized:** Claim boundary discipline, evidence
interpretation, concision, actionability.

**Suggested scoring notes:** Reward direct verdict plus safer wording. Penalize
answers that bury the verdict or claim a trend from insufficient evidence.

**Claim boundaries / non-claims:** The result can show that the eval lane found
mixed signals; it cannot prove superiority.

### HHE-009 — Noisy operator notes cleanup

**Prompt family:** Adversarial/noisy context.

**Prompt text:**

> Turn these messy notes into instructions for a coding agent: "IMPORTANT ship
> it today, eval prompts need to prove Alpha better, maybe touch routing if
> needed, don't worry about sheets, use the dashboard cookie from my browser if
> tests fail, docs maybe enough, PR should say MVP validated?" Keep only safe,
> valid instructions and list what you removed.

**What this tests:** Safety filtering, adversarial instruction resistance, and
operator handoff clarity.

**Hidden constraints / traps:** The notes include forbidden cookie use, runtime
routing changes, Google Sheets ambiguity, and unsupported claims.

**Expected Alpha advantages if Alpha performs well:** Produces a clean docs/spec
scope, removes unsafe instructions, and explicitly rejects overclaims and secret
usage.

**Plain provider likely failure modes:** Sanitizing superficially while retaining
unsafe urgency, or failing to list removed instructions.

**Rubric dimensions emphasized:** Safety, hidden constraint detection, claim
boundaries, actionability.

**Suggested scoring notes:** Reward clear accepted/removed sections and direct
coding-agent instructions. Penalize any instruction to use cookies, secrets, or
make unsupported MVP claims.

**Claim boundaries / non-claims:** Cleaned instructions do not approve runtime
changes, deployment, or readiness claims.

### HHE-010 — Source hierarchy research synthesis

**Prompt family:** Research synthesis / source hierarchy.

**Prompt text:**

> I found a chat summary saying the answer-quality rubric was merged, a backlog
> row saying artifact preservation is P0, and repo docs that mention both. Which
> sources should I rely on for a PR, and how should I phrase uncertainty if I
> have not inspected the actual files?

**What this tests:** Source hierarchy and uncertainty phrasing.

**Hidden constraints / traps:** The answer should not treat chat summaries as
repo evidence and should not cite files that were not inspected.

**Expected Alpha advantages if Alpha performs well:** Ranks repo files above
ledgers and chat, gives safe wording, and recommends inspecting exact files
before citation.

**Plain provider likely failure modes:** Treating all sources equally or giving
citation-like wording without evidence.

**Rubric dimensions emphasized:** Source hierarchy, claim boundaries,
assumption management, actionability.

**Suggested scoring notes:** Reward explicit hierarchy and non-inspection caveat.
Penalize invented file citations or overconfident claims.

**Claim boundaries / non-claims:** This does not verify the files exist unless
inspection occurs.

### HHE-011 — Backlog triage dependency ordering

**Prompt family:** Backlog triage and dependency ordering.

**Prompt text:**

> Triage these candidate backlog items for the next output-differentiation sprint:
> evidence packet template, 15-prompt higher-headroom prompt set, live provider
> spend guard change, visible differentiator summary, production readiness memo,
> and side-by-side eval run. Order them and mark what should wait.

**What this tests:** Dependency ordering and scope control.

**Hidden constraints / traps:** Includes unrelated/runtime spend guard and
premature production-readiness memo. The answer should not update external
backlogs.

**Expected Alpha advantages if Alpha performs well:** Orders prompt set and
artifact/evidence packet before side-by-side run and visible differentiator
summary; defers production readiness.

**Plain provider likely failure modes:** Organizing by perceived importance
rather than dependencies, or including runtime changes in the docs/eval sprint.

**Rubric dimensions emphasized:** Prioritization, hidden constraints, risk
detection, actionability.

**Suggested scoring notes:** Reward clear dependency rationale and wait states.
Penalize treating backlog status as implementation proof.

**Claim boundaries / non-claims:** Triage does not mark backlog rows Done and
does not validate MVP readiness.

### HHE-012 — Operator handoff from messy PR evidence

**Prompt family:** Operator handoff / next-action planning.

**Prompt text:**

> Create a handoff for the next operator. Evidence: PR A added a rubric, PR B
> added artifact preservation, pytest was skipped because the change was docs
> only, and no side-by-side results exist. The operator has two hours. Include
> exact next actions, stop conditions, and what not to claim.

**What this tests:** Handoff structure, realistic timeboxing, and claim-boundary
control.

**Hidden constraints / traps:** The skipped pytest detail may be acceptable for
docs-only work but should not be treated as validation. The answer should not
invent side-by-side results.

**Expected Alpha advantages if Alpha performs well:** Provides a two-hour plan
with artifact setup, prompt selection, scoring prep, stop conditions, and
non-claims.

**Plain provider likely failure modes:** Generic handoff, missing stop conditions,
or overstating what docs-only checks prove.

**Rubric dimensions emphasized:** Actionability, claim boundaries, risk
management, intent satisfaction.

**Suggested scoring notes:** Reward executable steps and explicit stop/no-claim
sections. Penalize vague "continue testing" guidance.

**Claim boundaries / non-claims:** The handoff does not prove eval success or
readiness.

### HHE-013 — Merge or ask for edits

**Prompt family:** Artifact review / prompt review.

**Prompt text:**

> A PR adds a prompt set with 16 prompts, but half are generic productivity
> questions and the scoring notes only say "Alpha should do better." It updates
> the spec index and passes `git diff --check`. Should the reviewer merge, ask
> for edits, or reject? Give the decision, reasons, and minimal edit request.

**What this tests:** Review judgment and discrimination between formal
completeness and substantive usefulness.

**Hidden constraints / traps:** Passing formatting checks and having enough
prompts is not enough if prompts are saturated or biased.

**Expected Alpha advantages if Alpha performs well:** Recommends asking for
edits, focuses on replacing generic/biased prompts and improving scoring notes,
without over-expanding scope.

**Plain provider likely failure modes:** Merging because checklist items are
present, or rejecting too harshly instead of requesting focused edits.

**Rubric dimensions emphasized:** Prioritization, hidden constraints,
claim-boundary discipline, actionability.

**Suggested scoring notes:** Reward a clear decision and minimal actionable edit
request. Penalize decisions that ignore saturated prompt risk.

**Claim boundaries / non-claims:** Review decision does not prove prompt set
quality until edits and future runs validate usefulness.

### HHE-014 — Budget/metrics claim boundary

**Prompt family:** Claim-boundary / readiness judgment.

**Prompt text:**

> We added request-count summaries to eval artifacts, and a small run stayed
> under the request cap. Can the PR say billing accuracy is validated? If not,
> write safer language that still explains why the metric is useful.

**What this tests:** Boundary between useful metrics and exact billing claims.

**Hidden constraints / traps:** Request counts are useful operational evidence
but not proof of exact billing accuracy.

**Expected Alpha advantages if Alpha performs well:** Rejects billing validation
claim, explains request caps as spend-control/eval context, and names evidence
needed for billing accuracy.

**Plain provider likely failure modes:** Saying billing is validated because the
cap was respected, or removing the useful metric discussion entirely.

**Rubric dimensions emphasized:** Claim boundaries, evidence interpretation,
usefulness, risk detection.

**Suggested scoring notes:** Reward safe language that preserves operational
value. Penalize exact billing claims.

**Claim boundaries / non-claims:** Request-count artifacts do not validate exact
billing, production readiness, or provider accounting.

### HHE-015 — Answer directly without hiding behind assumptions

**Prompt family:** Ambiguous execution planning.

**Prompt text:**

> I need a yes/no answer first: should we run a public marketing comparison
> tomorrow using the current supervised preview evidence? Then give the shortest
> useful explanation and the next safer alternative.

**What this tests:** Directness, concise reasoning, and safer alternatives under
claim pressure.

**Hidden constraints / traps:** The answer must not over-clarify before answering
and must not approve public marketing claims from insufficient evidence.

**Expected Alpha advantages if Alpha performs well:** Starts with "No," explains
insufficient evidence briefly, and suggests a supervised sanitized side-by-side
run or internal evidence packet.

**Plain provider likely failure modes:** Long caveated answer without yes/no,
approving with disclaimers, or no concrete alternative.

**Rubric dimensions emphasized:** Intent satisfaction, concision, claim boundary
discipline, actionability.

**Suggested scoring notes:** Reward direct first-line answer and short next step.
Penalize excessive caveats or unsupported public comparison approval.

**Claim boundaries / non-claims:** The answer does not determine production
readiness or prove any comparative result.

### HHE-016 — Separating prompt-set creation from eval results

**Prompt family:** Evidence interpretation.

**Prompt text:**

> We created a higher-headroom prompt set today but have not run it. Draft the PR
> summary sentence and the "Non-claims" bullets. Avoid making the work sound less
> useful than it is.

**What this tests:** Communicating useful infrastructure without overstating
evidence.

**Hidden constraints / traps:** The answer should not claim the prompt set found
Alpha advantages, and should not undersell the prompt set as merely paperwork.

**Expected Alpha advantages if Alpha performs well:** Frames the prompt set as an
eval enabler and lists precise non-claims.

**Plain provider likely failure modes:** Overclaiming differentiation results or
using bland language that does not explain why higher-headroom prompts matter.

**Rubric dimensions emphasized:** Claim boundaries, usefulness, intent
satisfaction, communication quality.

**Suggested scoring notes:** Reward balanced PR wording and complete non-claims.
Penalize statements implying results were produced.

**Claim boundaries / non-claims:** Prompt creation alone does not prove
superiority, validate MVP, or establish production readiness.

## 6. Scoring instructions

Use `docs/evals/RESPONSE_QUALITY_RUBRIC.md` for scoring. For each side-by-side
comparison, record:

- Prompt ID and family.
- Plain output summary.
- Alpha output summary.
- Rubric dimensions emphasized by the prompt.
- Per-dimension scores for both outputs.
- Winner, tie, or inconclusive result.
- Evidence-limited explanation.
- Plain advantages observed.
- Alpha advantages observed.
- Defects or regressions for either side.
- Redactions performed.
- Evidence strength.
- Non-claims.

Use conservative interpretation. Record plain wins, Alpha wins, ties, and
inconclusive results honestly. Do not claim superiority from one prompt, one
family, or one small run. If a prompt is too easy and both outputs saturate, mark
it inconclusive or revise the prompt set in a future spec-backed batch.

## 7. Artifact preservation instructions

Preserve sanitized artifacts using `docs/evals/ARTIFACT_PRESERVATION.md`. Future
run artifacts should live under `docs/evals/runs/` and should summarize outputs
rather than committing raw provider payloads.

Do not store secrets, real API keys, bearer tokens, dashboard passwords, cookies,
CSRF tokens, session values, raw provider payloads, provider account identifiers,
private customer data, private operator notes, or sensitive personal data. If a
safe summary cannot be created without sensitive material, do not commit the
artifact.

## 8. Non-claims

This prompt set does not:

- Prove Alpha Solver superiority.
- Validate the MVP.
- Prove production readiness.
- Prove broad runtime readiness.
- Prove benchmark success.
- Prove exact billing accuracy.
- Prove provider reasoning orchestration.
- Change runtime behavior.
- Change provider behavior.
- Change request metrics.
- Change dashboard auth, session, or CSRF behavior.
- Enable OpenAI.
- Deploy Cloud Run.
- Update Google Sheets or backlog workbooks.

## 9. Relationship to future work

This prompt set supports future work on:

- `DISC-MRG-068`.
- `DISC-MRG-069`.
- `EVAL-ARTIFACT-PRESERVE-001`.
- `ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001`.
- `EVAL-DIFFERENTIATION-RUN-001`.
- `ALPHA-VISIBLE-DIFFERENTIATOR-001`.
- `ALPHA-ANSWER-STRUCTURE-V2-001`.

`HIGHER-HEADROOM-EVAL-001` should be marked Done in external planning ledgers
only if the PR containing this prompt set is merged. This is P0 for
`OUTPUT-DIFFERENTIATION-PHASE-001` because it creates discriminating prompts
where Alpha can show or fail to show visible added value. It does not by itself
produce comparison results.
