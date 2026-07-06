# ALPHA-SOLVER-SUBSTANTIVE-LIFT-ANSWER-CONTRACT-001 · Substantive Lift Answer Contract

Status: Implemented (portable surface only)

Runtime successor of the `ALPHA-ANSWER-STRUCTURE-V2-001` planning lane for the
portable prompt surface (`alpha_solver_portable.py`).

## Goal

Make Alpha's answers on substantive tasks visibly and structurally different
from a generic model response by requiring the SOLUTION itself to perform six
compact reasoning moves — intent diagnosis, hidden-assumption surfacing,
dominant-tradeoff identification, a committed recommendation, a named failure
condition, and an executable next action — plus anti-generic wording rules.

## Motivation

The active answer surface operators use is the portable spec monolith loaded
as a system prompt. Its existing contract contains envelope structure and ten
restraint rules (brevity, format fit, claim safety) but no rule that forces
sharper content inside SOLUTION. The committed Batch B planning evidence
recorded that Alpha's limited-pilot lift clustered around substantive
constraint, risk, evidence, and comparative-value behavior (+21 lift cluster)
while its clearest weakness was brevity (-10), and `ALPHA-ANSWER-STRUCTURE-V2-001`
proposed a prompt-aware answer architecture as planning only, with no runtime
implementation. This lane implements that architecture's high-headroom half as
an enforceable contract on the portable surface, leaving the existing
low-headroom restraint rules in control of concise tasks.

## Scope

- New docstring section in `alpha_solver_portable.py`:
  `SUBSTANTIVE LIFT CONTRACT (HIGH-HEADROOM TASKS)` with the six-move lift
  block, applicability triggers, low-headroom exemptions with explicit
  restraint precedence, five anti-generic rules, and a wording-only boundary.
- Machine-readable constants mirroring the contract: `SUBSTANTIVE_LIFT_MOVES`,
  `SUBSTANTIVE_LIFT_TRIGGERS`, `SUBSTANTIVE_LIFT_EXEMPT`,
  `GENERIC_HEDGE_PATTERNS`, `WEAK_NEXT_ACTION_OPENERS`,
  `SUBSTANTIVE_LIFT_ANTI_GENERIC_RULES`, plus
  `substantive_lift_contract_summary()` for prompt-loading workflows.
- Deterministic structural checker `check_substantive_lift(solution_text)`
  verifying: all six labels present in order, `Intent:` first, non-empty move
  content, no hedge phrasing (word-boundary matched), and an executable rather
  than deliberative `Next:` line.
- Updated `COMPLIANCE_EXAMPLES` (compliant lift-block example plus a new
  `NON_COMPLIANT_GENERIC` example showing that envelope labels without
  substantive content fail the protocol) and a lift-form
  `ENVELOPE_OUTPUT_EXAMPLE`.
- Fixtures with three realistic substantive prompts (decision, root-cause
  diagnosis, constrained plan) carrying compliant and non-compliant answers,
  plus one low-headroom case proving restraint precedence.

## Non-goals

- No provider, hosted-model, or local-model calls; no network calls.
- No `/v1/solve`, routing, SAFE-OUT, or SolverEnvelope shape changes.
- No scoring, ranking, blinding, or unblinding; no capture or rescoring.
- No claim that the contract improves scores: whether these wording
  requirements produce measurable lift is a separate, future evaluation lane.
- No benchmark, readiness, production, public-MVP, provider-validation,
  local-model-validation, or Alpha-superiority claims.
- The deterministic local ToT path is out of scope: it cannot generate
  substantive content without a model, which remains out of bounds here.

## Code Targets

- `alpha_solver_portable.py` — contract text, constants, summary helper,
  checker, examples.
- `tests/fixtures/alpha_substantive_lift_cases.json` — synthetic cases.
- `tests/test_alpha_substantive_lift_contract.py` — structural enforcement.

## Test Plan

`tests/test_alpha_substantive_lift_contract.py` covers: contract section
presence and placement after the restraint contract, explicit low-headroom
precedence wording, wording-only boundary statements, constant/label
consistency, summary completeness, checker pass on compliant fixtures, checker
failure on non-compliant fixtures with named missing moves, hedge-phrase
flagging (including a word-boundary false-positive guard), weak next-action
flagging, out-of-order block rejection, low-headroom answers correctly carrying
no lift block, fixture shape (three or more realistic substantive prompts),
and compliance-example round-trips through the checker.

## Acceptance Criteria

- `python -m pytest tests/test_alpha_substantive_lift_contract.py -q` passes.
- `python -m pytest tests/test_alpha_minimal_behavior_contract.py -q` still
  passes (restraint contract and its precedence untouched).
- `python scripts/check_narrative_claim_safety.py` passes on this spec.
- A passing checker result means only that the configured wording structure
  held for the given text; it is not a quality or correctness judgment.

## Definition of Done

Contract text, constants, checker, examples, fixtures, and tests merged; all
listed checks pass; the low-headroom restraint contract retains precedence and
all boundaries above hold.
