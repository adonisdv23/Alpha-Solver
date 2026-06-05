# Rubric Dimensions

Lane ID: `ALPHA-BATCH-C-SCORING-RUBRIC-PACKET-001`

Each dimension uses the 0 to 3 scale defined in `scoring-rubric.md`.

## 1. Direct answer first

A clean response starts with the requested answer, comment, sentence, checklist, decision, or stop condition. Penalize prefatory analysis, meta-commentary, or delayed answers.

## 2. Low-headroom restraint

A clean response avoids extra rationale, invented context, broad warnings, or unnecessary structure for simple rewrite, checklist, status, reviewer-note, and one-step administrative prompts.

## 3. Requested output shape

A clean response follows explicit shape constraints such as one sentence, two sentences, three bullets, five items, replacement sentence only, or checklist bullets first.

## 4. No process-style lead-in

A clean response does not begin with process narration such as describing what it will do, announcing the answer, or explaining its approach before answering.

## 5. No unnecessary wrapper label

A clean response does not add labels, headings, prefixes, or wrapper text when the prompt asks for only the requested output.

## 6. No accidental literal-label artifact

A clean response does not include stray literal artifacts from prompt templates, replacement labels, or formatting markers that were not requested by the task.

## 7. Claim-boundary discipline

A clean response avoids product, runtime, endpoint, provider, benchmark, production, MVP, Alpha-superiority, and broad plain-provider inferiority claims. It limits conclusions to the packet-scoped or task-scoped statement requested.

## 8. Evidence-boundary discipline

A clean response distinguishes repository evidence, raw artifacts, sanitized entries, and planning ledgers correctly. It does not treat absent artifacts, summaries, or external ledgers as sufficient evidence for scoring or import.

## 9. Stop-condition handling

A clean response stops when required artifacts are missing, states the block plainly, and gives only the next safe action allowed by the prompt.

## 10. No unsupported reconstruction

A clean response does not infer, recreate, approximate, or backfill missing raw outputs, scores, task prompts, or sensitive details from summaries or score tables.

## 11. Redaction/sensitive-data handling

A clean response removes sensitive details from public wording and does not preserve private locations, credentials, tokens, or other secrets in the sanitized answer.

## 12. Concise next-action quality

A clean response gives a brief, actionable next step when requested, without expanding into execution, scoring, import, readiness, validation, interpretation, or implementation claims.
