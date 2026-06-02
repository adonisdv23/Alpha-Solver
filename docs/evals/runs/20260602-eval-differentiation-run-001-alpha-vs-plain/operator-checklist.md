# OUTPUT-DIFF-A3-OPERATOR-CHECKLIST-DRY-RUN-001 · Operator Checklist

## Purpose

This checklist makes the operator workflow for the first scored Alpha-vs-plain
differentiation run explicit, and defines the dry-run validation rules that must
hold before any output is captured or scored. It is the readiness step for the
controlled pilot scaffolded by `EVAL-DIFFERENTIATION-RUN-001`.

- Lane: `OUTPUT-DIFF-A3-OPERATOR-CHECKLIST-DRY-RUN-001`
- Step: A3-0 (checklist and dry-run readiness only)
- Phase: `OUTPUT-DIFFERENTIATION-PHASE-001`
- Run directory: `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/`
- Rubric reference: `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- Lift decision reference: `docs/evals/LIFT_DECISION_RULE.md`
- Blind scoring reference: `docs/evals/BLIND_SCORING_PROCEDURE.md`
- Artifact preservation reference: `docs/evals/ARTIFACT_PRESERVATION.md`
- Companion guide: `artifact-population-guide.md`

## A3-0 versus A3-1 boundary

This document is the A3-0 step. A3-0 prepares the checklist and validation rules.
It is documentation only.

A3-0 explicitly does not:

- execute the run;
- call live providers or make any provider request;
- add outputs;
- add scores;
- populate paired-output captures;
- populate evidence packets;
- populate `score-table.csv`, `blinded-score-sheet.csv`, or `blinding-map.csv`
  rows;
- modify any runtime, provider, clarify, `/v1/solve`, preview-UI, dashboard-auth,
  or eval-script behavior.

A3-1 is the later, separately approved step that actually captures sanitized
paired outputs, performs blinded scoring, unblinds, and records a conservative
result. A3-1 is not performed here.

## How to use this checklist

Work top to bottom. Do not start output generation until every Section A box is
checked and recorded. If any Section H stop condition is true, halt and escalate
instead of continuing. Treat every rule in Sections B through G as binding during
A3-1.

## A. Pre-run setup

Complete and record all of the following before any execution begins:

- [ ] Operator approval to begin A3-1 is recorded.
- [ ] The approved branch is recorded before execution.
- [ ] The approved commit SHA is recorded before execution.
- [ ] The exact run directory is confirmed as
      `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/`.
- [ ] The exact prompt subset is confirmed as exactly these four prompts:
  - `HHE-002`
  - `HHE-003`
  - `HHE-007`
  - `HHE-009`
- [ ] The expected primary generation cap is confirmed as **8 primary
      generations**, because 4 prompts x 2 surfaces.
- [ ] An optional contingency cap of **10 to 12 total requests** is used only if
      it is explicitly approved in writing; otherwise the cap stays at 8.
- [ ] The plain surface is identified and recorded before execution.
- [ ] The Alpha surface is identified and recorded before execution.
- [ ] It is confirmed that no runtime or provider behavior changes are allowed for
      this run.

The same prompt text must be sent to both surfaces. Neither surface may receive
extra instructions that the other did not receive.

## B. Output generation rules for the later A3-1 step

For each of the four prompts:

- Submit the same prompt to the plain surface.
- Submit the same prompt to the Alpha surface.
- Save sanitized answer text only.
- Save word counts for each output.
- Save only allowed summary-level metadata.
- Save sanitized Alpha expert-envelope fields only if available and allowed.

Do not, while generating outputs:

- Save raw provider payloads.
- Save response IDs, headers, account identifiers, cookies, CSRF or session
  values, environment dumps, or private user data.
- Score the outputs.
- Unblind the outputs.

Output generation is a capture step only. Scoring and unblinding happen later and
separately.

## C. Blinding rules

- Assign plain and Alpha to `Output A` and `Output B` using a recorded random
  method or seed.
- Record the mapping in `blinding-map.csv`.
- Assign `Output A` / `Output B` and record the map before writing any
  judge-facing paired-output capture, so captures and scoring share the same
  neutral labels (see `artifact-population-guide.md`).
- Complete blinded scoring before consulting the map.
- Keep Alpha and plain identity out of all judge-facing fields.
- Treat blinding as procedural, not cryptographic. The committed map is visible;
  the protection comes from scoring the blinded sheet before consulting the map.
  Alpha's expert envelope may remain a structural tell.

## D. Scoring rules for the later A3-1 step

- Score `Output A` and `Output B` on all 14 rubric dimensions.
- Use `docs/evals/RESPONSE_QUALITY_RUBRIC.md` as the scoring contract.
- Fill `blinded-score-sheet.csv` first, using neutral Output A / Output B labels.
- Unblind only after blinded scoring is complete.
- Transfer scores into `score-table.csv` after unblinding.
- Compute and record each of the following:
  - `plain_total`
  - `alpha_total`
  - `total_delta`
  - `lift_delta`
  - `polish_delta`
  - `lift_qualified`
  - `material_constraint_verified`
  - `polish_only_flag`
- Apply the polish-only guard from `docs/evals/LIFT_DECISION_RULE.md`.
- Do not count polish-only wins as expert-interrogation lift. A better-structured,
  longer, or tidier answer is not lift unless a real constraint was surfaced.

The 14 rubric dimensions are: `d01_intent`, `d02_direct`, `d03_structure`,
`d04_assumptions`, `d05_hidden_constraints`, `d06_risk_failure`,
`d07_claim_boundary`, `d08_evidence_uncertainty`, `d09_decision`,
`d10_next_actions`, `d11_specificity`, `d12_brevity`, `d13_safety`, and
`d14_comparative_value`.

## E. Planned artifact names for A3-1

These artifacts are planned for the later A3-1 step. They are listed here for
readiness only and are not created or populated by A3-0.

Planned paired-output captures:

```text
paired-output-captures/cmp-HHE-002-paired-output-capture.md
paired-output-captures/cmp-HHE-003-paired-output-capture.md
paired-output-captures/cmp-HHE-007-paired-output-capture.md
paired-output-captures/cmp-HHE-009-paired-output-capture.md
```

Planned evidence packets:

```text
evidence-packets/cmp-HHE-002-evidence-packet.md
evidence-packets/cmp-HHE-003-evidence-packet.md
evidence-packets/cmp-HHE-007-evidence-packet.md
evidence-packets/cmp-HHE-009-evidence-packet.md
```

Paired-output captures must reuse
`docs/evals/templates/paired_output_capture_template.md`. Evidence packets must
reuse `docs/evals/templates/side_by_side_evidence_packet_template.md`. See
`artifact-population-guide.md` for field-by-field guidance.

## F. Defect workflow

Record each observed defect during A3-1 in `defects.md` with these fields:

- defect ID;
- prompt ID;
- side;
- rubric dimension;
- category;
- severity;
- evidence pointer;
- follow-up ticket;
- whether it affects `lift_qualified`.

Use these defect categories (or a narrowly named new category):

- missed requested deliverable;
- unsupported claim;
- treating backlog as repo proof;
- unsafe secret/cookie/session handling;
- raw payload preservation suggestion;
- over-interrogation;
- excessive caveats;
- invented constraints;
- plain output more direct/useful.

## G. Redaction rules

It is explicitly prohibited to commit any of the following:

- API keys;
- bearer-token credentials;
- dashboard passwords;
- cookies;
- CSRF tokens;
- session values;
- auth headers;
- raw provider payloads;
- provider account identifiers;
- full unredacted request/response traces;
- environment dumps;
- private user data;
- credentials or any secret-like strings.

Only sanitized, summary-level, re-scorable artifacts may be committed. When in
doubt, redact and note the redaction.

## H. Stop conditions

A3 execution must stop if any of the following is true:

- operator approval is missing;
- the branch or commit is not recorded;
- the request cap is missing or has been exceeded;
- the prompt text differs between the plain and Alpha surfaces;
- either surface receives extra instructions not given to the other;
- outputs contain sensitive data that cannot be redacted;
- artifacts would require raw provider payloads;
- runtime or provider changes would be needed to proceed;
- blinding cannot be performed before scoring;
- the scorer sees the Alpha/plain mapping before scoring;
- the artifact format cannot be validated;
- any result would be used to claim validation, superiority, production readiness,
  benchmark success, exact billing accuracy, or provider reasoning orchestration.

If a stop condition triggers, halt, record why, and escalate before continuing.

## I. Non-claims

A3 artifacts do not claim:

- MVP validation;
- Alpha Solver superiority;
- answer-quality superiority;
- production readiness;
- broad runtime readiness;
- benchmark success;
- exact billing accuracy;
- provider reasoning orchestration.

A single small, supervised, blinded comparison cannot establish broad conclusions.
Plain wins and ties must be recorded honestly.

## A3-0 completion confirmation

This A3-0 step confirms that, in this PR:

- the run is not executed;
- no outputs are captured;
- no scores are recorded;
- no provider calls are made;
- no paired-output captures are populated;
- no evidence packets are populated;
- `score-table.csv`, `blinded-score-sheet.csv`, and `blinding-map.csv` remain
  header-only;
- `paired-output-captures/` and `evidence-packets/` remain placeholder
  directories;
- no runtime, provider, clarify, `/v1/solve`, preview-UI, dashboard-auth, or
  eval-script behavior is changed.

A3-0 prepares readiness only. A3-1 is the later approved step that performs the
scored run.
