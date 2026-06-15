# Prompt-Contract Simulation Methodology

Lane: `ALPHA-SOLVER-PROMPT-CONTRACT-SIMULATION-METHODOLOGY-001`

Status: docs-only methodology template.

## 1. TLDR

Prompt-contract simulation is a manual, evidence-bound diagnostic method for checking whether a written Alpha Solver prompt or behavior contract appears internally usable before investing in runtime, provider, benchmark, or product-surface execution. It is appropriate only after the first Value Read method has proven practical enough to reuse and only for synthetic or sanitized inputs.

This method can support packet-scoped observations about the prompt contract's clarity, boundary discipline, output-format hygiene, and stop-condition behavior. It cannot prove runtime behavior, provider behavior, benchmark validity, MVP readiness, production readiness, public readiness, Alpha superiority, or value-positive performance.

## 2. Method definition

### Appropriate use

Use prompt-contract simulation when all of the following are true:

1. The first Value Read method has produced a practical reusable pattern worth diagnosing further.
2. The objective is to evaluate a written prompt contract, operator packet, or behavior template rather than a deployed endpoint.
3. Inputs are synthetic, public, or sanitized and contain no private data, secrets, provider account details, customer content, or non-public operational material.
4. The operator can preserve raw model outputs exactly enough for later review while still applying required redactions.
5. The scoring rubric, evidence boundary, stop conditions, and unblinding sequence are frozen before outputs are scored.
6. The lane explicitly labels all outputs as prompt-contract simulation evidence only.

Do not use prompt-contract simulation when the required claim depends on live routing, `/v1/solve`, provider adapters, product UI behavior, latency, token accounting, cost, safety filters in deployed code, benchmark comparability, or production operations.

### What it can prove

Prompt-contract simulation can establish only that, within the preserved packet and scoring rubric:

- a prompt contract was understandable enough for the simulator to produce outputs;
- the generated outputs did or did not follow the written instructions;
- claim-boundary and evidence-boundary language was preserved or violated;
- raw-output artifacts were preserved sufficiently for audit;
- specified stop conditions were triggered, missed, or not encountered;
- a reusable diagnostic workflow was practical or impractical for future simulation lanes.

### What it cannot prove

Prompt-contract simulation cannot prove:

- runtime behavior or endpoint behavior;
- provider behavior, provider quality, or provider compliance;
- benchmark validation or generalizable quality;
- live orchestration, routing, telemetry, billing, cost, latency, or reliability;
- Alpha superiority over plain provider output;
- MVP, production, public, or operator readiness;
- that missing, incomplete, or redacted-away results would have passed.

## 3. Operator template

Copy and complete this template before running a prompt-contract simulation.

```markdown
# Prompt-Contract Simulation Run Packet

Run ID:
Lane ID:
Date:
Operator:
Reviewer roster:
Prompt-contract version / source path:
Simulation surface:
Input source and sanitization status:
Private data present: no
Provider/runtime execution used: no
Benchmark claim intended: no

## Evidence boundary

This run produces prompt-contract simulation evidence only. It is not runtime evidence, `/v1/solve` evidence, provider evidence, benchmark evidence, MVP validation, production readiness, public readiness, Alpha superiority evidence, or broad value proof.

## Frozen inputs

- Case IDs:
- Prompt text or prompt-contract excerpt:
- Rubric version:
- Stop conditions:
- Scoring fields:
- Raw-output preservation path:
- Redaction rules:

## Execution log

For each case preserve:

- case ID;
- prompt/input as supplied, unless redaction is required;
- complete raw output;
- timestamp or sequence number;
- simulator/model/surface label, if known;
- operator notes separated from raw output;
- redactions applied, with reason;
- whether a stop condition was observed.

## Blind scoring packet

For each case provide scorers only:

- anonymized case ID;
- frozen prompt-contract requirements;
- raw output or sanitized raw output;
- rubric;
- stop-condition list.

Do not provide prior score totals, desired outcome, author identity, pass/fail target, or downstream decision preference during blind scoring.

## Scoring table

| Blind Case ID | Boundary discipline | Instruction adherence | Output-format hygiene | Stop-condition handling | Evidence preservation | Score | Disposition | Defects | Reviewer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Unblinded interpretation

After blind scoring is locked, add:

- original case IDs;
- source packet links;
- aggregate score totals;
- defect themes;
- accepted narrow observations;
- blocked claims;
- selected next lane or blocker fallback.
```

## 4. Scoring sequence

1. **Freeze materials**: lock case list, prompt-contract text, rubric, scoring scale, stop conditions, evidence boundary, redaction rules, and artifact paths before output generation or scoring.
2. **Generate or collect simulation outputs**: run only the authorized manual simulation surface. Do not call runtime endpoints or providers unless the lane is separately authorized as runtime/provider work; if that occurs, this methodology no longer describes the evidence type.
3. **Preserve raw outputs**: save complete outputs before editing, summarizing, scoring, or interpreting. If redaction is required, preserve a sanitized raw-output artifact and a redaction log rather than reconstructing content.
4. **Prepare blind packet**: replace original case labels with blind IDs and remove outcome expectations, prior ratings, and downstream decision language.
5. **Score independently**: reviewers score against the frozen rubric without discussing results. They must mark stop conditions and defects even if the aggregate score is high.
6. **Resolve scoring mechanics only**: fix arithmetic or transcription errors before unblinding. Do not revise rubric criteria, reconstruct missing outputs, or change scores to fit an expected result.
7. **Lock blind scores**: record reviewer, timestamp/date, score, disposition, defects, and any invalidated cases.
8. **Unblind**: map blind IDs back to case IDs only after scores are locked.
9. **Interpret narrowly**: summarize only packet-scoped simulation observations, with explicit limitations and non-claims.
10. **Close out**: choose either a narrow next simulation/design lane, a runtime/provider authorization request, or a blocker fallback lane.

## 5. Evidence boundary

### Claim-boundary rules

Simulation evidence must be described with all of these boundaries:

- The evidence is manual prompt-contract simulation evidence only.
- The evidence is packet-scoped and applies only to the preserved cases, prompt-contract version, rubric, and scoring process.
- The evidence may identify observed defects or reusable methodology signals, but it must not be promoted into runtime, provider, benchmark, product, public, MVP, production, or superiority claims.
- Missing raw outputs, missing scores, unresolved redactions, or incomplete case records remain missing; they must not be reconstructed or treated as passes.
- Scoring summaries must distinguish observed outputs from operator interpretation.
- Comparative language is allowed only if the packet actually contains frozen comparable cases and blind scoring for those cases; even then, it remains simulation-only.
- Any future runtime/provider claim requires a separately authorized lane with its own execution artifacts.

### Raw-output preservation rules

- Preserve complete raw outputs before review notes, formatting cleanup, or interpretation.
- Store raw outputs separately from reviewer notes and aggregate summaries.
- Keep case IDs, prompt-contract version, simulation surface, date, and operator metadata with each output.
- If sensitive content appears, stop and redact minimally; record what category was redacted and why, without retaining private data in the repo.
- Do not paraphrase raw outputs as a substitute for missing raw artifacts.
- Do not backfill outputs from memory, screenshots not preserved in the packet, chat summaries, or downstream score comments.
- Mark any case with missing or materially altered raw output as invalid or evidence-limited.

## 6. Failure modes

Stop the run or mark the affected cases invalid if any of the following occur:

- private data, secrets, provider account details, or non-public customer content appears;
- the operator cannot preserve raw outputs in a sanitized, auditable form;
- the prompt-contract version, case set, rubric, or stop conditions were changed after outputs were generated;
- scorers see outcome expectations, desired pass/fail status, prior score totals, or original case identities before blind scoring is locked;
- runtime, provider, benchmark, or product-surface execution is mixed into the packet without a separate authorization and evidence boundary;
- missing outputs, missing scores, or redacted-away material would be needed to support the conclusion;
- the packet contains contradictory evidence-boundary language;
- scoring criteria are too ambiguous for independent reviewers to apply;
- reviewers cannot distinguish raw output from operator commentary;
- the interpretation requires broad claims beyond packet-scoped simulation observations.

Common non-stopping defects that should still be logged include visible process-style text, accidental labels or wrappers, minor formatting drift, incomplete but non-material metadata, reviewer disagreement within a predefined tolerance, and low-confidence observations that are explicitly caveated.

## 7. Non-claims

This methodology does not claim or create:

- provider evidence;
- runtime or `/v1/solve` evidence;
- benchmark validation;
- public demo readiness;
- MVP readiness;
- production readiness;
- value-positive proof;
- Alpha superiority;
- broad prompt quality;
- deployment readiness;
- private-data suitability;
- permission to reconstruct missing results;
- permission to use private data;
- authorization to run live providers, spend money, expose a public surface, or update external backlog ledgers.
