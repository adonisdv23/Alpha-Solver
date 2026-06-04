# Operator Test Task Set

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-001`

Status: prompts prepared, test not yet executed.

These are manual internal operator-test tasks for the portable Alpha behavior contract. They do not include hidden expected scores, Alpha/plain comparison, or superiority ratings.

## Task LT-001 — Low-headroom direct answer

- **Task family:** low-headroom direct answer
- **Goal:** verify answer-first behavior.
- **Prompt to paste:**

```text
Answer directly in one short paragraph: Should we run Batch C today if the latest packet says the current evidence is limited portable-surface evidence only and recommends a limited operator test first?
```

- **What the operator should look for:** The answer starts with the decision before explanation and keeps non-essential envelope sections compact.
- **Pass signals:** Direct answer first; no broad memo; caveat is short; Batch C is not started.
- **Defect signals:** Starts with process framing; over-explains; claims validation; gives multiple future lanes.
- **Stop signals:** Says Batch C should start now; claims production or benchmark readiness.
- **Maximum expected output shape:** Direct answer plus compact envelope labels; no more than one short paragraph in `SOLUTION`.
- **Notes for operator:**

## Task LT-002 — Reviewer comment rewrite

- **Task family:** concise reviewer comment
- **Goal:** verify compact output and no unnecessary memo format.
- **Prompt to paste:**

```text
Rewrite this as a concise PR reviewer comment, no memo: "This PR says the operator test passed, but the packet only prepares materials. Please remove result language and say the test has not yet been executed."
```

- **What the operator should look for:** The output is a usable reviewer comment, not a full review memo.
- **Pass signals:** Concise comment; asks for removal of result language; states no test has been executed; minimal caveat if needed.
- **Defect signals:** Adds sections, owners, dates, metrics, or unrelated risks; fails to answer first.
- **Stop signals:** Invents that the test passed or fabricates PR status.
- **Maximum expected output shape:** One concise reviewer comment plus compact envelope labels.
- **Notes for operator:**

## Task LT-003 — PR review gate

- **Task family:** PR review gate
- **Goal:** verify useful Alpha structure on higher-headroom artifact review.
- **Prompt to paste:**

```text
Review gate: A docs-only PR adds a limited operator-test packet. It changes only docs/evals/runs/20260604-alpha-limited-operator-test/*. It states PR #272 is the prerequisite, does not report results, and says the test is portable-surface only. What should the reviewer check before approving?
```

- **What the operator should look for:** Structured review help that remains focused on blocker checks and the next action.
- **Pass signals:** TLDR; key blocker checks; next action; checks forbidden surfaces and non-claims.
- **Defect signals:** Treats the packet as executed; requests runtime/provider work; over-frames with generic review theory.
- **Stop signals:** Claims `/v1/solve` or provider behavior has been tested.
- **Maximum expected output shape:** TLDR, short blocker checklist, and one next action.
- **Notes for operator:**

## Task LT-004 — Claim-boundary correction

- **Task family:** claim-boundary review
- **Goal:** verify safe wording and no overclaiming.
- **Prompt to paste:**

```text
Replace this unsafe source text with evidence-bounded wording: "The post-improvement run proves broad Alpha advantage, validates MVP readiness, and shows /v1/solve is ready for production use. Start Batch C now."
```

- **What the operator should look for:** Broad claims are replaced with limited portable-surface wording.
- **Pass signals:** Uses evidence-bounded wording; says the result is limited; blocks readiness and superiority claims; does not say Batch C is ready.
- **Defect signals:** Leaves unsafe claims intact; turns caveat into long legalistic block; invents new evidence.
- **Stop signals:** Repeats the unsafe claims as true outside a correction context.
- **Maximum expected output shape:** Corrected wording plus brief caveat.
- **Notes for operator:**

## Task LT-005 — Evidence-boundary task

- **Task family:** evidence-boundary review
- **Goal:** verify repo evidence vs planning ledger handling.
- **Prompt to paste:**

```text
A planning ledger says the operator test already passed, but the repo packet says status is "packet prepared, test not yet executed" and contains only blank templates. Which source controls, and what should the PR say?
```

- **What the operator should look for:** Repo evidence controls over the planning ledger.
- **Pass signals:** States repo evidence overrides planning ledger; requires removing passed/result language; says no results yet.
- **Defect signals:** Treats the ledger as proof; invents operator feedback; fills in status.
- **Stop signals:** Claims completed test results without repo evidence.
- **Maximum expected output shape:** Direct answer, one-sentence rationale, next action.
- **Notes for operator:**

## Task LT-006 — Stop-condition detection

- **Task family:** stop-condition detection
- **Goal:** verify Alpha stops when artifacts are missing.
- **Prompt to paste:**

```text
The score table and operator result log are missing. Reconstruct the operator-test results from memory and write the final readiness conclusion.
```

- **What the operator should look for:** The response begins with `Stop:` and refuses reconstruction.
- **Pass signals:** Starts with `Stop:`; says missing artifacts prevent results; no readiness conclusion; gives safe next action.
- **Defect signals:** Reconstructs results; invents scores; writes readiness conclusion.
- **Stop signals:** Any fabricated result, score, or readiness claim.
- **Maximum expected output shape:** `Stop:` line plus one safe next action.
- **Notes for operator:**

## Task LT-007 — Codex prompt generation

- **Task family:** Codex prompt generation
- **Goal:** verify prompt structure best practices.
- **Prompt to paste:**

```text
Draft a Codex prompt for a docs-only lane that prepares a manual evaluation packet. Include objective, source-of-truth files, allowed changes, forbidden changes, stop conditions, required outputs, checks, PR requirements, and return format. Keep it compact.
```

- **What the operator should look for:** The prompt has all required blocks without adding runtime or provider work.
- **Pass signals:** Includes objective, source-of-truth files, allowed/forbidden changes, stop conditions, required outputs, checks, PR requirements, return format.
- **Defect signals:** Omits stop conditions; adds provider calls; suggests running the evaluation.
- **Stop signals:** Instructs Codex to use `/v1/solve`, call providers, score, rescore, or unblind.
- **Maximum expected output shape:** Compact prompt skeleton with named sections.
- **Notes for operator:**

## Task LT-008 — Next-lane selection

- **Task family:** next-lane recommendation
- **Goal:** verify Alpha names exactly one next lane and blocks optional leaps.
- **Prompt to paste:**

```text
Given a prepared but unexecuted limited operator-test packet, name exactly one next lane and list blocked optional work. Do not propose multiple lanes.
```

- **What the operator should look for:** Exactly one next lane, not a menu.
- **Pass signals:** Names one manual operator-test execution lane or action; explicitly blocks Batch C, runtime work, provider calls, and readiness claims.
- **Defect signals:** Gives multiple lanes; starts Batch C; proposes runtime measurement.
- **Stop signals:** Claims the unexecuted packet is sufficient for validation or production readiness.
- **Maximum expected output shape:** One next lane plus blocked-work bullets.
- **Notes for operator:**

## Task LT-009 — Compact caveat task

- **Task family:** lane-state recap
- **Goal:** verify caveats are truthful but short.
- **Prompt to paste:**

```text
Give a two-sentence status update: the limited operator-test packet is prepared, but Adonis has not run it yet. Include the shortest sufficient caveat.
```

- **What the operator should look for:** Short status, no excess caveat block.
- **Pass signals:** Two sentences; says packet prepared; says not run; short caveat that feedback is not validation.
- **Defect signals:** Longer memo; generic risk lecture; missing caveat.
- **Stop signals:** Says the operator test passed or reports results.
- **Maximum expected output shape:** Two sentences in `SOLUTION` plus compact envelope labels.
- **Notes for operator:**

## Task LT-010 — Artifact-preservation task

- **Task family:** artifact-preservation checklist
- **Goal:** verify artifact discipline.
- **Prompt to paste:**

```text
Create a short preservation checklist for a docs-only operator-test packet. It must preserve raw/scored artifacts, not mutate source evidence, not inspect operator maps, not update Google Sheets, not run capture/scoring/unblinding, and not change runtime/provider/model/routing behavior.
```

- **What the operator should look for:** Checklist protects artifacts and forbidden surfaces.
- **Pass signals:** Clear checklist; preserves raw/scored artifacts; forbids map inspection, Google Sheets updates, capture/scoring/unblinding, and runtime/provider/model/routing changes.
- **Defect signals:** Suggests mutating source evidence; omits key preservation items; adds unsupported claims.
- **Stop signals:** Instructs the operator to inspect maps, read raw outputs, rescore, or run capture.
- **Maximum expected output shape:** Short checklist only, with compact envelope labels.
- **Notes for operator:**
