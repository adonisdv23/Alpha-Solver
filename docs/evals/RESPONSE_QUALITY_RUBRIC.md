# Universal Response Quality Rubric

## Purpose

This rubric calibrates side-by-side review of plain provider output versus Alpha
Solver expert-preview output during `OUTPUT-DIFFERENTIATION-PHASE-001`.

Its job is to define what "better" means before higher-headroom comparison runs
start. Reviewers should use it to score the two answers against the user's real
goal, record defects, and identify whether Alpha, the plain provider, neither,
or both performed better on the prompt.

## Scope and inputs

Use this rubric when a reviewer has all of the following:

- the original user prompt and any instructions supplied with it;
- the plain provider output;
- the Alpha Solver expert-preview output;
- any preserved evaluation metadata needed to identify the prompt family, run,
  reviewer, and artifact source.

This rubric is documentation/spec-only. It does not alter runtime behavior,
provider behavior, request metrics, dashboard auth/session/CSRF behavior,
deployment posture, billing/accounting, or backlog spreadsheets.

## Base scoring scale

Score each answer independently for each dimension unless the dimension is
explicitly comparative. Use conservative interpretation when evidence is mixed.

| Score | Meaning | Reviewer interpretation |
| --- | --- | --- |
| 0 | Harmful, missing, or materially wrong | The answer fails the dimension in a way that could mislead, block, or harm the user. |
| 1 | Weak or incomplete | The answer partially addresses the dimension but leaves important gaps, vagueness, or avoidable defects. |
| 2 | Acceptable | The answer is usable and mostly correct for the dimension, though not especially strong. |
| 3 | Strong | The answer handles the dimension clearly, accurately, and usefully for the prompt's real goal. |

## Required dimensions

### 1. User intent preservation

**Definition:** How well the answer preserves the user's actual request,
deliverable, constraints, audience, and implied goal.

| Score | Criteria |
| --- | --- |
| 0 | Ignores, contradicts, or replaces the user's requested task; answers a different question. |
| 1 | Captures the broad topic but misses a key deliverable, constraint, audience, or requested framing. |
| 2 | Addresses the requested task and most constraints with only minor drift. |
| 3 | Accurately preserves the explicit request and the practical goal behind it, including important context and audience needs. |

**Common failure examples:** Rewriting a request for a rubric into a generic eval
essay; producing advice when the user asked for a checklist; optimizing for
model self-promotion instead of the user's decision.

**What reviewers should look for:** Compare the answer to the prompt, not to
what the answer seems comfortable discussing. Check whether the requested output
form, role, audience, and success condition survived.

### 2. Direct answer usefulness

**Definition:** How quickly and effectively the answer gives the user the core
thing they asked for.

| Score | Criteria |
| --- | --- |
| 0 | No usable answer, or the answer is materially wrong or blocks the user's next step. |
| 1 | Some relevant content, but the core deliverable is buried, incomplete, or too indirect. |
| 2 | Provides a usable answer with the main deliverable present. |
| 3 | Provides the requested deliverable directly, with high practical utility and minimal friction. |

**Common failure examples:** Long preambles before the actual answer; vague
recommendations where a concrete decision was requested; failure to provide the
artifact requested.

**What reviewers should look for:** Ask whether a busy user could immediately
use the answer for the stated task.

### 3. Structure and format discipline

**Definition:** How well the answer follows requested format and uses structure
to improve readability, comparison, or execution.

| Score | Criteria |
| --- | --- |
| 0 | Violates required format or is disorganized enough to impair use. |
| 1 | Has some structure but misses requested sections, ordering, labels, or formatting constraints. |
| 2 | Mostly follows the requested structure and is readable. |
| 3 | Follows the requested format precisely and uses headings, bullets, tables, or ordering to make review easier. |

**Common failure examples:** Not using the requested scoring scale; omitting a
required section; adding unrequested narrative that makes the deliverable harder
to review.

**What reviewers should look for:** Check requested output shape first, then
judge whether the chosen structure makes the answer easier to verify and act on.

### 4. Assumption surfacing

**Definition:** How well the answer identifies assumptions that affect the
answer's validity without letting assumptions replace the requested deliverable.

| Score | Criteria |
| --- | --- |
| 0 | Hides critical assumptions, invents facts, or relies on assumptions that make the answer wrong. |
| 1 | Mentions assumptions vaguely or too late, or uses assumptions to avoid answering. |
| 2 | Surfaces important assumptions and still provides a usable answer. |
| 3 | Clearly separates assumptions from facts, explains why they matter, and proceeds with a useful default when reasonable. |

**Common failure examples:** "Assuming everything is standard" when the prompt
contains unusual constraints; asking for clarification instead of answering when
a safe assumption would work; overloading the answer with speculative caveats.

**What reviewers should look for:** Identify whether unstated defaults changed
the deliverable, and whether the answer tells the user what would change if an
assumption is false.

### 5. Hidden constraint detection

**Definition:** How well the answer notices constraints that are not prominent
but are implied by the domain, workflow, user context, or downstream use.

| Score | Criteria |
| --- | --- |
| 0 | Misses a hidden constraint whose omission materially undermines the answer. |
| 1 | Notices a possible constraint but handles it superficially or inconsistently. |
| 2 | Accounts for the main hidden constraints needed for a safe, useful answer. |
| 3 | Proactively identifies important hidden constraints and integrates them into the recommendation or deliverable. |

**Common failure examples:** Ignoring privacy, deployment, cost, reviewability,
audience, deadline, regulatory, compatibility, or dependency constraints.

**What reviewers should look for:** Ask what an expert in the user's situation
would check before acting, then see whether the answer accounted for it.

### 6. Risk and failure-mode detection

**Definition:** How well the answer identifies likely ways the recommendation,
plan, or deliverable could fail.

| Score | Criteria |
| --- | --- |
| 0 | Omits serious risks or recommends an unsafe path. |
| 1 | Lists generic risks without tying them to the prompt or action. |
| 2 | Identifies relevant risks and gives basic mitigation guidance. |
| 3 | Identifies the most important failure modes, prioritizes them, and gives practical mitigations or decision gates. |

**Common failure examples:** Treating all risks as equal; mentioning risk only as
a disclaimer; missing failure modes that are central to the prompt.

**What reviewers should look for:** Look for prompt-specific risks, not boilerplate.
A strong answer helps the user avoid the most likely or highest-impact failures.

### 7. Claim boundary discipline

**Definition:** How well the answer avoids unsupported claims and distinguishes
what is proven, likely, assumed, unknown, or outside scope.

| Score | Criteria |
| --- | --- |
| 0 | Makes false, overbroad, or unsupported claims; presents speculation as fact. |
| 1 | Includes some boundaries but also overstates certainty or scope. |
| 2 | Mostly stays within the available evidence and flags important limits. |
| 3 | Uses precise claim language, avoids overreach, and makes scope boundaries easy to audit. |

**Common failure examples:** Claiming broad superiority from one example;
claiming production readiness from a smoke test; asserting exact billing,
benchmark success, or orchestration behavior without evidence.

**What reviewers should look for:** Underline every claim that sounds like a
conclusion and ask whether the artifact supports it.

### 8. Evidence and uncertainty handling

**Definition:** How well the answer uses evidence, cites or explains its basis
when appropriate, and handles uncertainty without becoming unusable.

| Score | Criteria |
| --- | --- |
| 0 | Fabricates evidence, ignores uncertainty, or uses irrelevant support. |
| 1 | Mentions evidence or uncertainty but does not connect it to the answer's decisions. |
| 2 | Uses relevant evidence or clear reasoning and notes important uncertainty. |
| 3 | Grounds claims in the right evidence level, separates knowns from unknowns, and explains how uncertainty affects the recommendation. |

**Common failure examples:** Unsupported confidence; excessive hedging that
prevents a decision; citing irrelevant facts; treating missing data as proof.

**What reviewers should look for:** Check whether the evidence is adequate for
the strength of the answer's claims.

### 9. Decision usefulness

**Definition:** How well the answer helps the user choose, prioritize, approve,
reject, or sequence action.

| Score | Criteria |
| --- | --- |
| 0 | Does not help the user decide or points toward the wrong decision. |
| 1 | Provides information but little prioritization, tradeoff analysis, or recommendation. |
| 2 | Supports a reasonable decision with relevant pros, cons, or criteria. |
| 3 | Clarifies the decision, identifies the best path or options, and explains tradeoffs in a way the user can apply. |

**Common failure examples:** Neutral lists when the prompt asks for a
recommendation; unprioritized options; hiding the recommended action.

**What reviewers should look for:** Ask whether the answer reduces decision
ambiguity for the user's actual situation.

### 10. Execution-ready next actions

**Definition:** How well the answer converts analysis into concrete next steps,
commands, checklists, owners, or acceptance criteria when appropriate.

| Score | Criteria |
| --- | --- |
| 0 | Provides no actionable next step where one is needed, or gives unsafe/unusable steps. |
| 1 | Gives broad next steps that require substantial interpretation. |
| 2 | Provides usable next actions with enough detail to begin. |
| 3 | Provides sequenced, concrete, verifiable next actions that match the user's workflow. |

**Common failure examples:** "Do more research" without specifying what to
check; recommendations with no implementation path; missing acceptance criteria.

**What reviewers should look for:** Determine whether the user could hand the
answer to an operator or teammate and get started without re-planning from
scratch.

### 11. Specificity over generic filler

**Definition:** How much prompt-specific substance the answer provides compared
with generic advice, filler, or reusable boilerplate.

| Score | Criteria |
| --- | --- |
| 0 | Mostly generic, irrelevant, or template-like content. |
| 1 | Some prompt-specific details, but generic filler dominates. |
| 2 | Mostly specific to the prompt with limited filler. |
| 3 | Highly specific, tailored, and free of unnecessary generic padding. |

**Common failure examples:** Generic best-practice lists; repeating the prompt
without adding value; boilerplate caveats unrelated to the task.

**What reviewers should look for:** Remove generic sentences mentally and see
how much useful answer remains.

### 12. Brevity versus necessary depth

**Definition:** How well the answer balances concise delivery with enough depth
to satisfy the prompt and prevent misuse.

| Score | Criteria |
| --- | --- |
| 0 | So brief that it is unusable, or so long that the core answer is effectively lost. |
| 1 | Noticeably under-explained or over-expanded for the task. |
| 2 | Reasonable length and depth for the prompt. |
| 3 | Efficiently provides all necessary depth with little wasted text. |

**Common failure examples:** Rewarding length as quality; omitting needed
rationale; adding exhaustive background when the user asked for a concise
artifact.

**What reviewers should look for:** Judge length relative to task complexity,
not personal preference. Depth is good only when it improves usability or
correctness.

### 13. Safety and policy preservation

**Definition:** How well the answer preserves applicable safety, privacy,
security, legal, medical, financial, and platform-policy constraints while still
being useful.

| Score | Criteria |
| --- | --- |
| 0 | Unsafe, policy-violating, or encourages harmful action. |
| 1 | Avoids the worst issue but is over-refusing, under-informative, or misses relevant safety context. |
| 2 | Safely addresses the request with useful boundaries. |
| 3 | Maintains safety while maximizing helpful, allowed content and practical alternatives. |

**Common failure examples:** Unsafe operational details; unnecessary refusal;
missing privacy/security implications; using safety language to avoid a benign
deliverable.

**What reviewers should look for:** Do not automatically reward the most
cautious answer. Reward safety that improves decision quality while preserving
allowed usefulness.

### 14. Comparative added value over plain output

**Definition:** Whether Alpha adds visible, material value over the plain
provider answer for the user's real goal.

| Score | Criteria |
| --- | --- |
| 0 | Alpha is materially worse than plain output, or adds harmful confusion. |
| 1 | Alpha adds minor or cosmetic differences but no meaningful improvement, or improves one area while degrading a more important one. |
| 2 | Alpha is at least comparable and adds some useful improvement for the prompt. |
| 3 | Alpha is clearly and materially better than plain output on important dimensions for the user's task. |

**Common failure examples:** Better formatting but worse content; safer caveats
but missing the deliverable; more assumptions but less direct usefulness;
longer answer with no incremental insight.

**What reviewers should look for:** Judge visible user-facing value. Do not
score Alpha higher merely because it is branded as Alpha, longer, or more
structured.

## Reviewer calibration guidance

- Score the answer, not the model brand.
- Compare against the prompt's real user goal, not only the literal topic words.
- Do not reward length by itself.
- Do not punish useful caution if it improves decision quality.
- Do not reward unsupported confidence.
- Treat "Alpha was safer but less useful" as mixed, not automatically better.
- Treat "Alpha added assumptions but missed the requested deliverable" as a
  defect.
- Mark cases where plain output is better.
- Mark ties honestly.
- Use conservative interpretation when the evidence is ambiguous.
- If an answer is polished but wrong, score the relevant correctness, evidence,
  claim-boundary, and usefulness dimensions low.
- If an answer is terse but fully satisfies a simple prompt, do not penalize it
  for not being elaborate.

## Summary scoring template

Use one summary row per prompt comparison.

| Field | Required entry |
| --- | --- |
| Prompt/run identifier | Stable prompt and artifact identifier. |
| Prompt family | Higher-headroom category or local prompt group. |
| Reviewer | Reviewer name or stable reviewer ID. |
| Total score | Sum of scored dimensions for the evaluated answer, or both totals if using one row for the pair. |
| Alpha score | Sum of Alpha's dimension scores. |
| Plain score | Sum of plain provider's dimension scores. |
| Delta | `Alpha score - Plain score`. |
| Winning surface | `Alpha`, `Plain`, `Tie`, or `Inconclusive`. |
| Reason for winner | Short explanation tied to the highest-impact dimensions. |
| Defects found | Specific defects, including whether they affect Alpha, plain, or both. |
| Follow-up tickets | Proposed backlog/spec/test follow-ups, or `None`. |

### Dimension score sheet

| Dimension | Plain score (0-3) | Alpha score (0-3) | Notes |
| --- | --- | --- | --- |
| 1. User intent preservation |  |  |  |
| 2. Direct answer usefulness |  |  |  |
| 3. Structure and format discipline |  |  |  |
| 4. Assumption surfacing |  |  |  |
| 5. Hidden constraint detection |  |  |  |
| 6. Risk and failure-mode detection |  |  |  |
| 7. Claim boundary discipline |  |  |  |
| 8. Evidence and uncertainty handling |  |  |  |
| 9. Decision usefulness |  |  |  |
| 10. Execution-ready next actions |  |  |  |
| 11. Specificity over generic filler |  |  |  |
| 12. Brevity versus necessary depth |  |  |  |
| 13. Safety and policy preservation |  |  |  |
| 14. Comparative added value over plain output |  |  |  |

## Winner and threshold guidance

Use the score delta as an input, not as an automatic verdict.

- A small delta is not enough to claim superiority.
- A single prompt cannot prove superiority.
- A narrow prompt family can show local advantage only.
- Broad claims require repeated artifact-backed evidence across higher-headroom
  prompts.
- Cost and latency can be noted, especially when they affect usability, but they
  should not dominate this rubric in `OUTPUT-DIFFERENTIATION-PHASE-001` unless
  they prevent the answer from being practically usable.
- If Alpha wins on safety but loses on direct usefulness, mark the outcome as
  mixed unless the safety issue is central enough to decide the prompt.
- If plain output better satisfies the user goal, mark `Plain` as the winning
  surface even if Alpha has better structure or more caveats.
- Use `Tie` when the answers are materially equivalent for the user's goal.
- Use `Inconclusive` when artifacts are incomplete, reviewer context is missing,
  or the prompt cannot be fairly scored.

### Aggregation, blinding, and lift qualification (additive)

These dimension definitions are unchanged. For how per-dimension scores are
aggregated without rewarding output polish — the lift/polish subscores, the
`lift_qualified` decision aid, and the polish-only-win guard — see
`docs/evals/LIFT_DECISION_RULE.md`. For label-stripped Output A / Output B
scoring, see `docs/evals/BLIND_SCORING_PROCEDURE.md`. These aids are internal
review tooling only and do not strengthen any claim boundary below.

## Strict non-claims

This rubric does not validate the MVP.

This rubric does not prove Alpha superiority.

This rubric does not prove production readiness.

This rubric does not prove broad runtime readiness.

This rubric does not prove benchmark success.

This rubric does not prove exact billing accuracy.

This rubric does not prove provider reasoning orchestration.

## Relationship to future work

This rubric is the reviewer contract for later output-differentiation work. It
should be referenced or incorporated by future specs and artifacts such as:

- `DISC-MRG-068`, prompt quality scoring and regression harness;
- `HIGHER-HEADROOM-EVAL-001`;
- `ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001`;
- `EVAL-DIFFERENTIATION-RUN-001`;
- `ALPHA-VISIBLE-DIFFERENTIATOR-001`;
- `ALPHA-ANSWER-STRUCTURE-V2-001`.

Those future tasks may add datasets, harnesses, preservation formats,
reviewer-agreement checks, or answer-structure improvements, but they should not
weaken the claim boundaries above.

## Backlog impact

`DISC-MRG-069` should be marked Done only if this PR is merged.

This is a P0 task for `OUTPUT-DIFFERENTIATION-PHASE-001`.

This defines what "better than plain output" means for future comparison runs.

This does not claim Alpha Solver superiority.

This does not validate the MVP.

This does not prove production readiness.
