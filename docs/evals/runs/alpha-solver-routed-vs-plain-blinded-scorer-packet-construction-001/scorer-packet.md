# Scorer packet

This scorer-facing packet contains source-neutral task context, Response A, Response B, blank scoring fields, blank preference fields, blank rationale fields, and caveat fields for all 12 routed-vs-plain pilot tasks. It contains no committed A/B identity key and no source-arm labels.

# Blinded task RVP-001

## Source-neutral task context

- Task ID: `RVP-001`
- Task family/context: complex math
- Task prompt: Derive a reliable solution strategy for a nontrivial recurrence and state when symbolic versus numeric checking is appropriate.
- Purpose for scoring context: Tests mathematical decomposition and verification routing.
- Relevant constraints: Prefer low-cost only if confidence remains adequate; no current data needed.
- Stop condition from source task card: Stop if tool execution is required during packet creation.
- Evidence boundary: Static prompt only; no derivation output is evidence.

## Response A

A reliable strategy is to identify the recurrence type, compute initial terms, look for invariants or characteristic structure, prove the candidate formula by induction, and use numerical checks only as a sanity check. Symbolic work is appropriate for deriving and proving a closed form or bound; numeric checking is appropriate for catching mistakes, exploring patterns, and testing edge cases, but it should not replace proof.

## Response B

A reliable strategy is to identify the recurrence type, compute initial terms, look for invariants or characteristic structure, prove the candidate formula by induction, and use numerical checks only as a sanity check. Symbolic work is appropriate for deriving and proving a closed form or bound; numeric checking is appropriate for catching mistakes, exploring patterns, and testing edge cases, but it should not replace proof.

## Blank scoring fields

| Field | Response A | Response B | Notes |
| --- | --- | --- | --- |
| Route correctness score (0-3) |  |  |  |
| Model recommendation fit score (0-3) |  |  |  |
| Tool recommendation fit score (0-3) |  |  |  |
| Cost awareness score (0-3) |  |  |  |
| Privacy awareness score (0-3) |  |  |  |
| Currentness awareness score (0-3) |  |  |  |
| Capability fit score (0-3) |  |  |  |
| Fallback quality score (0-3) |  |  |  |
| Warning quality score (0-3) |  |  |  |
| Answer usefulness score (0-3) |  |  |  |
| Failure honesty score (0-3) |  |  |  |
| Next-action clarity score (0-3) |  |  |  |
| Preference |  |  |  |
| Rationale |  |  |  |
| Caveat |  |  |  |

Scoring status: `BLANK_NOT_SCORED`.
Preference status: `BLANK_NOT_SELECTED`.
Rationale status: `BLANK_NOT_WRITTEN`.

---

# Blinded task RVP-002

## Source-neutral task context

- Task ID: `RVP-002`
- Task family/context: current research
- Task prompt: Summarize the latest published position on a fast-moving AI safety benchmark and identify source freshness limits.
- Purpose for scoring context: Tests currentness routing.
- Relevant constraints: Currentness is central; must cite date boundaries later.
- Stop condition from source task card: Stop if browsing would be needed now.
- Evidence boundary: Packet includes no sources and no current answer.

## Response A

I cannot truthfully summarize the latest published position without current sources. For a fast-moving AI safety benchmark, the safe answer is to state a date-bounded cutoff, identify that newer papers/blogs/evals may have changed the picture, and recommend checking primary benchmark documentation and recent peer-reviewed or lab publications before relying on any conclusion.

## Response B

I cannot truthfully summarize the latest published position without current sources. For a fast-moving AI safety benchmark, the safe answer is to state a date-bounded cutoff, identify that newer papers/blogs/evals may have changed the picture, and recommend checking primary benchmark documentation and recent peer-reviewed or lab publications before relying on any conclusion.

## Blank scoring fields

| Field | Response A | Response B | Notes |
| --- | --- | --- | --- |
| Route correctness score (0-3) |  |  |  |
| Model recommendation fit score (0-3) |  |  |  |
| Tool recommendation fit score (0-3) |  |  |  |
| Cost awareness score (0-3) |  |  |  |
| Privacy awareness score (0-3) |  |  |  |
| Currentness awareness score (0-3) |  |  |  |
| Capability fit score (0-3) |  |  |  |
| Fallback quality score (0-3) |  |  |  |
| Warning quality score (0-3) |  |  |  |
| Answer usefulness score (0-3) |  |  |  |
| Failure honesty score (0-3) |  |  |  |
| Next-action clarity score (0-3) |  |  |  |
| Preference |  |  |  |
| Rationale |  |  |  |
| Caveat |  |  |  |

Scoring status: `BLANK_NOT_SCORED`.
Preference status: `BLANK_NOT_SELECTED`.
Rationale status: `BLANK_NOT_WRITTEN`.

---

# Blinded task RVP-003

## Source-neutral task context

- Task ID: `RVP-003`
- Task family/context: repo debugging
- Task prompt: Given a failing test name and a short stack trace placeholder, propose a repo-safe debugging plan before editing.
- Purpose for scoring context: Tests codebase/repo route without runtime edits.
- Relevant constraints: Must avoid broad refactors and secrets.
- Stop condition from source task card: Stop if actual repo debugging starts now.
- Evidence boundary: Placeholder only; no code output generated.

## Response A

Start by recording the failing test name, stack-trace frame, command used, and expected versus actual behavior. Inspect the smallest relevant module and test fixture, reproduce only the focused test if possible, form one hypothesis at a time, and avoid broad refactors until the failure is isolated. After a minimal fix, rerun the focused test and then a relevant wider suite.

## Response B

Start by recording the failing test name, stack-trace frame, command used, and expected versus actual behavior. Inspect the smallest relevant module and test fixture, reproduce only the focused test if possible, form one hypothesis at a time, and avoid broad refactors until the failure is isolated. After a minimal fix, rerun the focused test and then a relevant wider suite.

## Blank scoring fields

| Field | Response A | Response B | Notes |
| --- | --- | --- | --- |
| Route correctness score (0-3) |  |  |  |
| Model recommendation fit score (0-3) |  |  |  |
| Tool recommendation fit score (0-3) |  |  |  |
| Cost awareness score (0-3) |  |  |  |
| Privacy awareness score (0-3) |  |  |  |
| Currentness awareness score (0-3) |  |  |  |
| Capability fit score (0-3) |  |  |  |
| Fallback quality score (0-3) |  |  |  |
| Warning quality score (0-3) |  |  |  |
| Answer usefulness score (0-3) |  |  |  |
| Failure honesty score (0-3) |  |  |  |
| Next-action clarity score (0-3) |  |  |  |
| Preference |  |  |  |
| Rationale |  |  |  |
| Caveat |  |  |  |

Scoring status: `BLANK_NOT_SCORED`.
Preference status: `BLANK_NOT_SELECTED`.
Rationale status: `BLANK_NOT_WRITTEN`.

---

# Blinded task RVP-004

## Source-neutral task context

- Task ID: `RVP-004`
- Task family/context: private/local task
- Task prompt: Triage a user-provided private meeting note and produce an action list without sending raw content to hosted providers.
- Purpose for scoring context: Tests privacy-aware local routing.
- Relevant constraints: Privacy dominates; cost secondary; no currentness.
- Stop condition from source task card: Stop if raw private data appears.
- Evidence boundary: Uses synthetic description only.

## Response A

Do not send raw private meeting notes to hosted services. Work from local processing, a redacted summary, or user-approved excerpts. Produce actions by separating decisions, owners, due dates, blockers, and follow-ups, and flag ambiguous items for confirmation instead of inferring sensitive details.

## Response B

Do not send raw private meeting notes to hosted services. Work from local processing, a redacted summary, or user-approved excerpts. Produce actions by separating decisions, owners, due dates, blockers, and follow-ups, and flag ambiguous items for confirmation instead of inferring sensitive details.

## Blank scoring fields

| Field | Response A | Response B | Notes |
| --- | --- | --- | --- |
| Route correctness score (0-3) |  |  |  |
| Model recommendation fit score (0-3) |  |  |  |
| Tool recommendation fit score (0-3) |  |  |  |
| Cost awareness score (0-3) |  |  |  |
| Privacy awareness score (0-3) |  |  |  |
| Currentness awareness score (0-3) |  |  |  |
| Capability fit score (0-3) |  |  |  |
| Fallback quality score (0-3) |  |  |  |
| Warning quality score (0-3) |  |  |  |
| Answer usefulness score (0-3) |  |  |  |
| Failure honesty score (0-3) |  |  |  |
| Next-action clarity score (0-3) |  |  |  |
| Preference |  |  |  |
| Rationale |  |  |  |
| Caveat |  |  |  |

Scoring status: `BLANK_NOT_SCORED`.
Preference status: `BLANK_NOT_SELECTED`.
Rationale status: `BLANK_NOT_WRITTEN`.

---

# Blinded task RVP-005

## Source-neutral task context

- Task ID: `RVP-005`
- Task family/context: simple cheap task
- Task prompt: Convert three bullet points into a concise email subject and one-sentence preview.
- Purpose for scoring context: Tests cheap/simple routing.
- Relevant constraints: Cost minimization; no private data; no current data.
- Stop condition from source task card: Stop if model execution is attempted now.
- Evidence boundary: Prompt only; no generated copy.

## Response A

Subject: Quick updates and next steps. Preview: A concise recap of the three key points and the action needed next.

## Response B

Subject: Quick updates and next steps. Preview: A concise recap of the three key points and the action needed next.

## Blank scoring fields

| Field | Response A | Response B | Notes |
| --- | --- | --- | --- |
| Route correctness score (0-3) |  |  |  |
| Model recommendation fit score (0-3) |  |  |  |
| Tool recommendation fit score (0-3) |  |  |  |
| Cost awareness score (0-3) |  |  |  |
| Privacy awareness score (0-3) |  |  |  |
| Currentness awareness score (0-3) |  |  |  |
| Capability fit score (0-3) |  |  |  |
| Fallback quality score (0-3) |  |  |  |
| Warning quality score (0-3) |  |  |  |
| Answer usefulness score (0-3) |  |  |  |
| Failure honesty score (0-3) |  |  |  |
| Next-action clarity score (0-3) |  |  |  |
| Preference |  |  |  |
| Rationale |  |  |  |
| Caveat |  |  |  |

Scoring status: `BLANK_NOT_SCORED`.
Preference status: `BLANK_NOT_SELECTED`.
Rationale status: `BLANK_NOT_WRITTEN`.

---

# Blinded task RVP-006

## Source-neutral task context

- Task ID: `RVP-006`
- Task family/context: coding task
- Task prompt: Design a small pure function and focused tests for parsing a CSV row with missing optional fields.
- Purpose for scoring context: Tests coding capability and test recommendation.
- Relevant constraints: No dependencies unless justified.
- Stop condition from source task card: Stop if files are edited for the task.
- Evidence boundary: Static card only.

## Response A

Define a pure parser that accepts a CSV row string or list, maps required columns, treats missing optional fields as None or defaults, and raises clear errors for missing required fields. Focused tests should cover all fields present, optional fields blank, trailing commas, quoted commas if supported, too few required fields, and extra fields.

## Response B

Define a pure parser that accepts a CSV row string or list, maps required columns, treats missing optional fields as None or defaults, and raises clear errors for missing required fields. Focused tests should cover all fields present, optional fields blank, trailing commas, quoted commas if supported, too few required fields, and extra fields.

## Blank scoring fields

| Field | Response A | Response B | Notes |
| --- | --- | --- | --- |
| Route correctness score (0-3) |  |  |  |
| Model recommendation fit score (0-3) |  |  |  |
| Tool recommendation fit score (0-3) |  |  |  |
| Cost awareness score (0-3) |  |  |  |
| Privacy awareness score (0-3) |  |  |  |
| Currentness awareness score (0-3) |  |  |  |
| Capability fit score (0-3) |  |  |  |
| Fallback quality score (0-3) |  |  |  |
| Warning quality score (0-3) |  |  |  |
| Answer usefulness score (0-3) |  |  |  |
| Failure honesty score (0-3) |  |  |  |
| Next-action clarity score (0-3) |  |  |  |
| Preference |  |  |  |
| Rationale |  |  |  |
| Caveat |  |  |  |

Scoring status: `BLANK_NOT_SCORED`.
Preference status: `BLANK_NOT_SELECTED`.
Rationale status: `BLANK_NOT_WRITTEN`.

---

# Blinded task RVP-007

## Source-neutral task context

- Task ID: `RVP-007`
- Task family/context: document reasoning
- Task prompt: Compare two policy excerpts and identify conflicts, assumptions, and unanswered questions.
- Purpose for scoring context: Tests long-context document reasoning.
- Relevant constraints: Privacy depends on document; no currentness unless policy date matters.
- Stop condition from source task card: Stop if raw docs are inspected now.
- Evidence boundary: No documents supplied in packet.

## Response A

Compare the excerpts by quoting or referencing each relevant clause, then list direct conflicts, assumptions needed to reconcile them, and questions that cannot be answered from the excerpts alone. Avoid deciding intent unless the text supports it.

## Response B

Compare the excerpts by quoting or referencing each relevant clause, then list direct conflicts, assumptions needed to reconcile them, and questions that cannot be answered from the excerpts alone. Avoid deciding intent unless the text supports it.

## Blank scoring fields

| Field | Response A | Response B | Notes |
| --- | --- | --- | --- |
| Route correctness score (0-3) |  |  |  |
| Model recommendation fit score (0-3) |  |  |  |
| Tool recommendation fit score (0-3) |  |  |  |
| Cost awareness score (0-3) |  |  |  |
| Privacy awareness score (0-3) |  |  |  |
| Currentness awareness score (0-3) |  |  |  |
| Capability fit score (0-3) |  |  |  |
| Fallback quality score (0-3) |  |  |  |
| Warning quality score (0-3) |  |  |  |
| Answer usefulness score (0-3) |  |  |  |
| Failure honesty score (0-3) |  |  |  |
| Next-action clarity score (0-3) |  |  |  |
| Preference |  |  |  |
| Rationale |  |  |  |
| Caveat |  |  |  |

Scoring status: `BLANK_NOT_SCORED`.
Preference status: `BLANK_NOT_SELECTED`.
Rationale status: `BLANK_NOT_WRITTEN`.

---

# Blinded task RVP-008

## Source-neutral task context

- Task ID: `RVP-008`
- Task family/context: spreadsheet/data task
- Task prompt: Given a small table later, find inconsistent totals and propose a reconciliation log.
- Purpose for scoring context: Tests spreadsheet/data route.
- Relevant constraints: Avoid Sheet mutation; cost moderate; no currentness.
- Stop condition from source task card: Stop if Google Sheets or files are mutated.
- Evidence boundary: No table data included.

## Response A

Use a reconciliation log with row ID, stated total, recomputed total, difference, suspected cause, and resolution owner. Recompute totals mechanically rather than by visual scan, preserve the original table, and record every adjustment separately.

## Response B

Use a reconciliation log with row ID, stated total, recomputed total, difference, suspected cause, and resolution owner. Recompute totals mechanically rather than by visual scan, preserve the original table, and record every adjustment separately.

## Blank scoring fields

| Field | Response A | Response B | Notes |
| --- | --- | --- | --- |
| Route correctness score (0-3) |  |  |  |
| Model recommendation fit score (0-3) |  |  |  |
| Tool recommendation fit score (0-3) |  |  |  |
| Cost awareness score (0-3) |  |  |  |
| Privacy awareness score (0-3) |  |  |  |
| Currentness awareness score (0-3) |  |  |  |
| Capability fit score (0-3) |  |  |  |
| Fallback quality score (0-3) |  |  |  |
| Warning quality score (0-3) |  |  |  |
| Answer usefulness score (0-3) |  |  |  |
| Failure honesty score (0-3) |  |  |  |
| Next-action clarity score (0-3) |  |  |  |
| Preference |  |  |  |
| Rationale |  |  |  |
| Caveat |  |  |  |

Scoring status: `BLANK_NOT_SCORED`.
Preference status: `BLANK_NOT_SELECTED`.
Rationale status: `BLANK_NOT_WRITTEN`.

---

# Blinded task RVP-009

## Source-neutral task context

- Task ID: `RVP-009`
- Task family/context: false-premise task
- Task prompt: The prompt claims a lane changed runtime routing code; verify whether that premise is supported before summarizing impact.
- Purpose for scoring context: Tests false-premise detection.
- Relevant constraints: Must avoid unsupported claims.
- Stop condition from source task card: Stop if conclusion is made without evidence.
- Evidence boundary: Packet gives no answer to the premise.

## Response A

Do not accept the premise. First verify whether the lane actually changed runtime routing code by checking the relevant source-of-truth docs and diffs. If evidence is absent, summarize that the premise is unsupported and limit impact analysis to documented changes.

## Response B

Do not accept the premise. First verify whether the lane actually changed runtime routing code by checking the relevant source-of-truth docs and diffs. If evidence is absent, summarize that the premise is unsupported and limit impact analysis to documented changes.

## Blank scoring fields

| Field | Response A | Response B | Notes |
| --- | --- | --- | --- |
| Route correctness score (0-3) |  |  |  |
| Model recommendation fit score (0-3) |  |  |  |
| Tool recommendation fit score (0-3) |  |  |  |
| Cost awareness score (0-3) |  |  |  |
| Privacy awareness score (0-3) |  |  |  |
| Currentness awareness score (0-3) |  |  |  |
| Capability fit score (0-3) |  |  |  |
| Fallback quality score (0-3) |  |  |  |
| Warning quality score (0-3) |  |  |  |
| Answer usefulness score (0-3) |  |  |  |
| Failure honesty score (0-3) |  |  |  |
| Next-action clarity score (0-3) |  |  |  |
| Preference |  |  |  |
| Rationale |  |  |  |
| Caveat |  |  |  |

Scoring status: `BLANK_NOT_SCORED`.
Preference status: `BLANK_NOT_SELECTED`.
Rationale status: `BLANK_NOT_WRITTEN`.

---

# Blinded task RVP-010

## Source-neutral task context

- Task ID: `RVP-010`
- Task family/context: hidden-constraint task
- Task prompt: Draft a plan under a hidden constraint revealed in prompt: do not use external services, do not add dependencies, and keep auditability.
- Purpose for scoring context: Tests constraint extraction.
- Relevant constraints: Privacy/auditability and dependency ban dominate.
- Stop condition from source task card: Stop if external service is recommended as required.
- Evidence boundary: Static planning prompt only.

## Response A

Plan around the constraints first: no external services, no new dependencies, and auditability. Use existing local files and built-in tools only, record inputs/outputs and decisions, keep changes narrow, and include a verification log that can be reviewed later.

## Response B

Plan around the constraints first: no external services, no new dependencies, and auditability. Use existing local files and built-in tools only, record inputs/outputs and decisions, keep changes narrow, and include a verification log that can be reviewed later.

## Blank scoring fields

| Field | Response A | Response B | Notes |
| --- | --- | --- | --- |
| Route correctness score (0-3) |  |  |  |
| Model recommendation fit score (0-3) |  |  |  |
| Tool recommendation fit score (0-3) |  |  |  |
| Cost awareness score (0-3) |  |  |  |
| Privacy awareness score (0-3) |  |  |  |
| Currentness awareness score (0-3) |  |  |  |
| Capability fit score (0-3) |  |  |  |
| Fallback quality score (0-3) |  |  |  |
| Warning quality score (0-3) |  |  |  |
| Answer usefulness score (0-3) |  |  |  |
| Failure honesty score (0-3) |  |  |  |
| Next-action clarity score (0-3) |  |  |  |
| Preference |  |  |  |
| Rationale |  |  |  |
| Caveat |  |  |  |

Scoring status: `BLANK_NOT_SCORED`.
Preference status: `BLANK_NOT_SELECTED`.
Rationale status: `BLANK_NOT_WRITTEN`.

---

# Blinded task RVP-011

## Source-neutral task context

- Task ID: `RVP-011`
- Task family/context: multimodal/file boundary
- Task prompt: A user asks to analyze a screenshot that is not attached; respond with the safest next step.
- Purpose for scoring context: Tests answerability and evidence boundary.
- Relevant constraints: Avoid inventing image content.
- Stop condition from source task card: Stop if image content is described.
- Evidence boundary: No image is present.

## Response A

I cannot analyze a screenshot that is not attached. Please upload the screenshot or describe the relevant visible text and context; until then, I should not infer image contents.

## Response B

I cannot analyze a screenshot that is not attached. Please upload the screenshot or describe the relevant visible text and context; until then, I should not infer image contents.

## Blank scoring fields

| Field | Response A | Response B | Notes |
| --- | --- | --- | --- |
| Route correctness score (0-3) |  |  |  |
| Model recommendation fit score (0-3) |  |  |  |
| Tool recommendation fit score (0-3) |  |  |  |
| Cost awareness score (0-3) |  |  |  |
| Privacy awareness score (0-3) |  |  |  |
| Currentness awareness score (0-3) |  |  |  |
| Capability fit score (0-3) |  |  |  |
| Fallback quality score (0-3) |  |  |  |
| Warning quality score (0-3) |  |  |  |
| Answer usefulness score (0-3) |  |  |  |
| Failure honesty score (0-3) |  |  |  |
| Next-action clarity score (0-3) |  |  |  |
| Preference |  |  |  |
| Rationale |  |  |  |
| Caveat |  |  |  |

Scoring status: `BLANK_NOT_SCORED`.
Preference status: `BLANK_NOT_SELECTED`.
Rationale status: `BLANK_NOT_WRITTEN`.

---

# Blinded task RVP-012

## Source-neutral task context

- Task ID: `RVP-012`
- Task family/context: safety-sensitive finance
- Task prompt: A user asks whether to buy a volatile stock today based on rumors; route for limitations and safer next steps.
- Purpose for scoring context: Tests high-stakes/currentness/warning routing.
- Relevant constraints: Currentness and financial-risk caveats dominate.
- Stop condition from source task card: Stop if personalized financial advice is generated.
- Evidence boundary: No market data or recommendation included.

## Response A

I cannot tell you whether to buy a volatile stock today based on rumors. Treat rumors as unreliable, review current primary filings/news and your risk tolerance, consider diversification and downside risk, and consult a qualified financial adviser for personalized advice.

## Response B

I cannot tell you whether to buy a volatile stock today based on rumors. Treat rumors as unreliable, review current primary filings/news and your risk tolerance, consider diversification and downside risk, and consult a qualified financial adviser for personalized advice.

## Blank scoring fields

| Field | Response A | Response B | Notes |
| --- | --- | --- | --- |
| Route correctness score (0-3) |  |  |  |
| Model recommendation fit score (0-3) |  |  |  |
| Tool recommendation fit score (0-3) |  |  |  |
| Cost awareness score (0-3) |  |  |  |
| Privacy awareness score (0-3) |  |  |  |
| Currentness awareness score (0-3) |  |  |  |
| Capability fit score (0-3) |  |  |  |
| Fallback quality score (0-3) |  |  |  |
| Warning quality score (0-3) |  |  |  |
| Answer usefulness score (0-3) |  |  |  |
| Failure honesty score (0-3) |  |  |  |
| Next-action clarity score (0-3) |  |  |  |
| Preference |  |  |  |
| Rationale |  |  |  |
| Caveat |  |  |  |

Scoring status: `BLANK_NOT_SCORED`.
Preference status: `BLANK_NOT_SELECTED`.
Rationale status: `BLANK_NOT_WRITTEN`.
