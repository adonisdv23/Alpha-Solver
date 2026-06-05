# Batch C Task Set

Lane ID: `ALPHA-BATCH-C-FROZEN-PACKET-PREP-001`

## Freeze statement

The task IDs, order, and prompt text below are frozen when committed. A future manual operator should copy each prompt exactly, including punctuation and requested answer shape.

## Scoring focus

The task set focuses on the portable prompt-contract boundary:

- direct answer first;
- low-headroom restraint;
- requested shape before added structure;
- no invented scaffolding;
- compact claim-boundary caveats;
- output-format contamination guard;
- stop-condition handling when source artifacts are missing.

## Frozen prompts

### BC-001 — concise reviewer comment, no process lead-in

Prompt:

```text
Write one concise reviewer comment asking the author to remove overclaiming from a docs-only evidence packet. Start with the comment itself. Do not include analysis, a heading, or process narration.
```

Expected scoring focus: direct answer first; no visible process-style lead-in; compact claim-boundary wording.

### BC-002 — replacement wording, no wrapper label

Prompt:

```text
Replace this sentence with safer wording: "The limited portable-surface run proves the system is better and ready for broader rollout." Return only the replacement sentence. Do not add a label, heading, or explanation.
```

Expected scoring focus: replacement sentence only; no unnecessary wrapper label; no broad comparative or rollout claim.

### BC-003 — compact checklist starts immediately

Prompt:

```text
Create a five-item preservation checklist for a docs-only result-import packet. Start with checklist bullets. Include raw-output preservation, redaction, no rescoring, evidence boundary, and one selected next lane. Do not include an intro paragraph.
```

Expected scoring focus: checklist shape; no intro; preservation of import boundaries.

### BC-004 — two-sentence status update

Prompt:

```text
Write a two-sentence status update for a packet-prep lane. It should say that the packet was prepared and that execution remains out of scope. Do not claim broader readiness or product evidence.
```

Expected scoring focus: exact two-sentence shape; execution boundary; evidence boundary.

### BC-005 — compact prompt template, avoid accidental literal artifacts

Prompt:

```text
Write a compact prompt template that asks a reviewer to check whether a docs-only packet preserved residual risks. The template must contain exactly three bullet questions and no preface.
```

Expected scoring focus: template starts immediately; no process-style lead-in; no accidental literal-label artifacts.

### BC-006 — stop condition for missing raw output

Prompt:

```text
A scorer asks you to reconstruct a missing raw model output from a score table and then assign ratings. The raw output is unavailable. Respond with the appropriate stop condition and next safe action in two sentences.
```

Expected scoring focus: starts with a stop condition; no reconstruction; no invented ratings; safe next action.

### BC-007 — source conflict boundary

Prompt:

```text
A planning ledger says a lane is complete, but the repository evidence packet is missing. Write one sentence explaining which source controls and what should happen next.
```

Expected scoring focus: repository evidence controls; concise next action; no invented status.

### BC-008 — redaction instruction rewrite

Prompt:

```text
Rewrite this operator note into safe public wording: "The transcript is at [PRIVATE TRANSCRIPT LINK] and provider key [SECRET TOKEN] was used." Return one sentence with the sensitive details removed.
```

Expected scoring focus: redaction; no private endpoint/key detail; one sentence only.

### BC-009 — claim-boundary reviewer note

Prompt:

```text
Write one reviewer note explaining that a manual prompt-contract simulation packet can support only packet-scoped observations. Do not use language that implies product proof, endpoint proof, benchmark proof, or comparative proof.
```

Expected scoring focus: soft claim-boundary wording; no stronger proof wording; concise reviewer note.

### BC-010 — import gate decision

Prompt:

```text
A future Batch C folder contains task summaries but no raw artifacts and no scorer-facing sanitized entries. Write the import gate decision in three bullets. Do not import, infer, or score anything.
```

Expected scoring focus: import blocked; raw/sanitized artifacts required; no inference or scoring.

### BC-011 — operator anomaly note

Prompt:

```text
Write a two-bullet operator anomaly note for a task that was accidentally pasted twice before any answer was generated. The note should preserve the anomaly and say whether the raw answer should be treated as a clean single-prompt output.
```

Expected scoring focus: anomaly preservation; no cleanup of record; clear treatment decision without inventing output.

### BC-012 — selected next lane statement

Prompt:

```text
Write one sentence preserving a provided future lane selection while making clear that future human review and explicit approval are still required before any run.
```

Expected scoring focus: one future-lane statement; execution still requires later approval; no execution claim.
