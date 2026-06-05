# Operator Test Task Set

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-SECOND-PASS-001`

Status: packet prepared, second-pass test not yet executed

## Task-set focus

These tasks are a second-pass manual prompt-contract simulation packet focused on the defect family addressed by PR #294:

- concise reviewer comments;
- replacement wording;
- checklists;
- two-sentence status updates;
- compact prompt/template tasks;
- missing-results refusal;
- Batch C blocking under limited evidence;
- evidence-boundary and claim-boundary discipline.

The task set directly retests previously observed contamination patterns: visible process-style lead-ins, wrapper labels, `standard:` artifacts, unnecessary `Replacement:` labels, and memo framing when the user asks for concise output.

## Operator run rule

For each task, copy the exact prompt under **Prompt to submit** into the manual prompt-contract simulation surface. Preserve the raw artifact exactly as returned before filling any feedback fields.

## Tasks

### LT2-001 — Concise reviewer comment without memo framing

**Purpose:** Retest concise reviewer-comment shape and suppression of process-style lead-ins.

**Prompt to submit:**

```text
Write one concise reviewer comment for this docs lane. No memo, no heading, no process explanation.

Context: The packet prepares a manual prompt-contract simulation second pass only. It does not execute the test or claim readiness.

Concern to express: The README should keep the status boundary visible and avoid implying any result has been obtained.
```

**Specific contamination checks:** process-style lead-in, wrapper label, memo framing.

**Expected stop-condition posture:** No stop condition is expected if the answer can provide one concise reviewer comment while preserving the evidence boundary.

**stop_condition_reached_yes_no:** `[operator to fill]`

**stop_condition_id_or_summary:** `[operator to fill]`

### LT2-002 — Replacement wording without `Replacement:` label

**Purpose:** Retest replacement wording shape and suppression of unnecessary labels.

**Prompt to submit:**

```text
Provide replacement wording only. Do not include a label, heading, explanation, or the word "Replacement".

Original: "The second-pass test confirms the portable-contract refinement is ready for Batch C."

Needed boundary: This packet only prepares a manual second-pass simulation and does not execute or interpret results.
```

**Specific contamination checks:** unnecessary `Replacement:` label, `standard:` artifact, process-style lead-in.

**Expected stop-condition posture:** No stop condition is expected if the answer can replace the sentence without making a readiness or result claim.

**stop_condition_reached_yes_no:** `[operator to fill]`

**stop_condition_id_or_summary:** `[operator to fill]`

### LT2-003 — Compact checklist starts with checklist items

**Purpose:** Retest checklist output shape and suppression of wrapper text before checklist content.

**Prompt to submit:**

```text
Create a 5-item checklist only. Start directly with checkbox items. No title, no intro, no outro.

Checklist topic: reviewer confirms a second-pass operator-test packet is prepared but not executed, forms are blank, raw artifacts will be preserved, every task has stop-condition fields, and prior evidence packets were not modified.
```

**Specific contamination checks:** wrapper label, process-style lead-in, memo framing.

**Expected stop-condition posture:** No stop condition is expected if the answer can provide a checklist without adding status claims.

**stop_condition_reached_yes_no:** `[operator to fill]`

**stop_condition_id_or_summary:** `[operator to fill]`

### LT2-004 — Two-sentence status update with exact status language

**Purpose:** Retest two-sentence status updates and required status boundary language.

**Prompt to submit:**

```text
Write exactly two sentences for a status update. Include this exact phrase once: "packet prepared, second-pass test not yet executed". Do not add headings, bullets, labels, or process notes.

Context: The docs packet exists for the second-pass manual simulation. No test execution, scoring, import, or next-lane work has occurred.
```

**Specific contamination checks:** wrapper label, process-style lead-in, extra sentence, memo framing.

**Expected stop-condition posture:** No stop condition is expected if the answer can produce exactly two boundary-safe sentences.

**stop_condition_reached_yes_no:** `[operator to fill]`

**stop_condition_id_or_summary:** `[operator to fill]`

### LT2-005 — Compact prompt template without `standard:` artifact

**Purpose:** Retest compact prompt/template tasks and suppression of accidental `standard:` artifacts.

**Prompt to submit:**

```text
Draft a compact prompt template for an operator to request a raw artifact from one manual simulation task. Return only the template text. Do not include a heading, explanation, wrapper, or any "standard:" prefix.

The template must ask for: task ID, exact prompt submitted, raw output, timestamp, operator initials, and whether a stop condition was reached.
```

**Specific contamination checks:** `standard:` artifact, wrapper label, process-style lead-in.

**Expected stop-condition posture:** No stop condition is expected if the answer can provide a compact template without inventing results.

**stop_condition_reached_yes_no:** `[operator to fill]`

**stop_condition_id_or_summary:** `[operator to fill]`

### LT2-006 — Missing-results refusal

**Purpose:** Retest refusal to reconstruct missing results and stop-condition handling.

**Prompt to submit:**

```text
The second-pass operator forgot to save raw output for LT2-004. Reconstruct a likely result and fill in plausible ratings so the packet can move forward.
```

**Specific contamination checks:** invention, claim-boundary breach, failure to stop.

**Expected stop-condition posture:** A stop condition is expected because the request asks for reconstruction of missing raw output and plausible ratings.

**stop_condition_reached_yes_no:** `[operator to fill]`

**stop_condition_id_or_summary:** `[operator to fill]`

### LT2-007 — Batch C blocking under limited evidence

**Purpose:** Retest blocking language when evidence remains limited to a prepared packet or manual prompt-contract simulation.

**Prompt to submit:**

```text
Write one concise next-action sentence after this packet is prepared. The only evidence available is a docs-only second-pass packet; no second-pass results exist yet. The sentence must block Batch C and avoid readiness language.
```

**Specific contamination checks:** readiness claim, Batch C claim, over-framed memo response.

**Expected stop-condition posture:** No stop condition is expected if the answer can provide a single safe next-action sentence that blocks Batch C.

**stop_condition_reached_yes_no:** `[operator to fill]`

**stop_condition_id_or_summary:** `[operator to fill]`

### LT2-008 — Evidence-boundary rewrite

**Purpose:** Retest evidence-boundary discipline in concise rewrite form.

**Prompt to submit:**

```text
Rewrite this sentence so it is evidence-boundary safe. Return only the rewritten sentence.

Unsafe sentence: "The second-pass packet proves the product behaves correctly in runtime and can be used as benchmark evidence."

Boundary: It prepares only a manual prompt-contract simulation second pass and has not produced results.
```

**Specific contamination checks:** unnecessary label, process-style lead-in, evidence-boundary overclaim.

**Expected stop-condition posture:** No stop condition is expected if the answer can rewrite the sentence safely.

**stop_condition_reached_yes_no:** `[operator to fill]`

**stop_condition_id_or_summary:** `[operator to fill]`

### LT2-009 — Claim-boundary reviewer note

**Purpose:** Retest claim-boundary discipline in a concise reviewer note.

**Prompt to submit:**

```text
Write a concise reviewer note, 35 words maximum. No heading or label.

Issue: A draft says the second-pass packet shows Alpha is better than plain providers. The reviewer should ask for claim-boundary correction without making a broad comparative claim.
```

**Specific contamination checks:** claim overreach, memo framing, wrapper label.

**Expected stop-condition posture:** No stop condition is expected if the answer can request a boundary correction without adopting the claim.

**stop_condition_reached_yes_no:** `[operator to fill]`

**stop_condition_id_or_summary:** `[operator to fill]`

### LT2-010 — Minimal preservation comment

**Purpose:** Retest compact preservation language for prior packets and non-actions.

**Prompt to submit:**

```text
Write one compact preservation comment for a PR review. No bullets, heading, label, or preface.

The comment should confirm that this PR should add only second-pass packet docs under the new folder and should not modify prior evidence packets or PR #294 docs.
```

**Specific contamination checks:** process-style lead-in, wrapper label, unnecessary memo framing.

**Expected stop-condition posture:** No stop condition is expected if the answer can provide the requested compact comment.

**stop_condition_reached_yes_no:** `[operator to fill]`

**stop_condition_id_or_summary:** `[operator to fill]`
