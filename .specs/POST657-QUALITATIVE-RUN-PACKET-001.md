# POST657-QUALITATIVE-RUN-PACKET-001 · Post-#657 Qualitative Run Packet

Status: Implemented

## Goal

Prepare a bounded post-#657 manual qualitative run packet and operator runbook
that use the existing `operator_run_capture.py` init, validate,
`lift-preflight`, and export flow before human reviewer handoff.

## Scope

- Add `tests/fixtures/operator_run_capture/post657_qualitative_case_packet.json`
  as a case packet with six high-headroom prompts.
- Add `docs/evals/runbooks/POST657_QUALITATIVE_RUN_PACKET.md` with copyable
  command sequence, manual paste instructions, preflight interpretation, export
  instructions, reviewer handoff, non-claims, and stop conditions.
- Add tests that validate packet shape, prompt anchors, required six-move
  prompt language, runbook command sequence, structural-only preflight wording,
  and non-claim boundaries.

## Packet requirements

The case packet uses packet id `POST657-QUALITATIVE-RUN-PACKET-001`, contains
four to six cases, and contains no baseline outputs, routed outputs, expected
answers, reviewer score fields, rating fields, rank fields, winner fields,
benchmark fields, readiness fields, validation-result claims, or superiority
fields. Each prompt names concrete repo anchors and requires Intent, Assumes,
Tradeoff, Recommendation, Fails if, and Next.

## Runbook requirements

The runbook is operator-facing and copyable. It includes the exact command
sequence:

1. `init` with the post-#657 case packet and local capture path.
2. `validate` over the local capture.
3. `lift-preflight` with a local report path.
4. `validate --for-export`.
5. `export` to a local capture packet.

It instructs the operator to paste plain baseline answers into
`baseline_output`, paste full routed Alpha answers into `routed_output`, allow a
leading `SOLUTION:` label after PR #657, keep `route_metadata` limited to route
and provenance facts, keep qualitative notes outside `route_metadata`, and use
`captured` or `excluded` statuses only under the documented conditions.

## Non-goals and boundaries

- No runtime behavior changes.
- No API, dashboard, route, persona, SAFE-OUT, SolverEnvelope, or provider
  changes.
- No provider calls, local-model calls, hosted-model calls, tool execution, or
  outside-service calls.
- No execution of the manual qualitative review.
- No scoring, ranking, winner selection, identity maps, A/B identity keys,
  benchmark claims, readiness claims, provider-validation claims,
  local-validation claims, or Alpha-superiority claims.
- A passing preflight means only that configured local structural wording checks
  held for the supplied routed output and prompt; it is not an answer-quality
  judgment.

## Validation

- `python -m pytest tests/test_post657_qualitative_run_packet.py -q`
- `python -m pytest tests/test_operator_run_capture.py tests/test_pr646_substantive_lift_eval_prep.py -q`
- `python -m pytest -q`
- `python scripts/check_narrative_claim_safety.py docs/evals/runbooks/POST657_QUALITATIVE_RUN_PACKET.md .specs/POST657-QUALITATIVE-RUN-PACKET-001.md`
- `ruff check tests/test_post657_qualitative_run_packet.py`
