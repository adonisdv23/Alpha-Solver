# Value Experiment Direction

> Created by lane `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-13**. This sets **direction only** — it is **not**
> the full experiment protocol, and **no experiment is run in this lane**.

## The core unresolved question

Alpha Solver has strong **evidence discipline** (a large, disciplined packet
history) but the **core value question remains unresolved**: does Alpha Solver
produce materially better outputs than a plain baseline? Repo signals support
this framing:

- Differentiation/measurement specs exist (`.specs/EVAL-DIFFERENTIATION-RUN-001.md`,
  `.specs/OUTPUT-DIFF-*`, `.specs/HIGHER-HEADROOM-EVAL-001.md`), indicating prior
  Alpha-vs-plain comparison attempts whose results are mixed/noisy
  (PARTIALLY_CONFIRMED — not re-scored here).
- A brevity-control spec exists (`.specs/ALPHA-BREVITY-CONTROL-001.md`),
  consistent with the concern that Alpha may be **penalized or flattered for
  verbosity** rather than judged on utility.

## What a tiny OpenAI smoke does and does not prove

- A tiny synthetic OpenAI smoke proves **plumbing only**: that a request can be
  formed, sent, and a response captured under redaction/cost boundaries.
- It does **not** prove Alpha Solver value, quality, or superiority. Smoke must
  never be promoted to value evidence (record an explicit smoke→eval gate).

## Next strategic validation

**`ALPHA-SOLVER-VALUE-EXPERIMENT-PROTOCOL-001`** — the highest-value strategic
lane after a successful tiny smoke. Direction for that protocol:

1. **Baseline comparison** — Alpha Solver vs a plain LLM baseline on the same
   tasks and same model.
2. **Enough tasks to reduce noise** — a task set large enough for the result not
   to hinge on one or two items; report variance, not just a mean.
3. **Verbosity / brevity controls** — control for length so Alpha is not
   rewarded or penalized for verbosity; measure utility per unit length.
4. **No self-referential governance prompts** — tasks must be real user-style
   problems, not prompts about Alpha's own evidence/governance process.
5. **Blind scoring** — graders do not know which output is Alpha vs baseline.
6. **Clear pass/fail thresholds** — pre-register what "Alpha adds value" means
   before scoring (effect size + threshold), to avoid post-hoc narrative.

## Boundaries

- Do **not** run the experiment, call providers, use tokens, or run evals in
  this lane.
- This direction makes **no** claim of benchmark validation, benchmark
  superiority, or broad-user readiness.
- The protocol is **blocked** until a real tiny smoke proves plumbing and
  OpenAI project/billing is clarified (see [`LANE_REGISTRY.md`](LANE_REGISTRY.md)).
