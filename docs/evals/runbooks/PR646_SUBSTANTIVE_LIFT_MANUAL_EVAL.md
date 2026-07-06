# PR646 Substantive Lift Manual Eval Runbook

Lane: `PR646-SUBSTANTIVE-LIFT-MANUAL-EVAL-PREP-001`

This runbook prepares a local-only manual comparison workflow for checking
whether PR #646's Substantive Lift Answer Contract creates an operator-visible
answer-quality difference. It is preparation and capture guidance only.

## Source-truth scope

- PR #646 added the portable substantive-lift answer contract.
- PR #647 bounded non-substantive local template outputs.
- PR #648 capped unsupported SAFE-OUT confidence.
- The existing operator run capture harness is the only capture/export flow for
  this packet.

## Manual workflow

1. Open a normal ChatGPT thread without Alpha Solver loaded and generate the
   plain/baseline answer for each prompt in
   `tests/fixtures/operator_run_capture/pr646_substantive_lift_case_packet.json`.
2. Open a fresh thread using the latest `alpha_solver_portable.py` after PR #648
   as the Alpha Solver instruction surface and generate the Alpha answer for the
   same prompt.
3. Scaffold a local capture file with the existing CLI:

   ```bash
   python scripts/operator_run_capture.py init \
     --case-packet tests/fixtures/operator_run_capture/pr646_substantive_lift_case_packet.json \
     --out local/pr646_substantive_lift_capture.json
   ```

4. Manually paste both outputs into the capture file:
   - `baseline_output` receives the plain ChatGPT output.
   - `routed_output` receives the Alpha Solver output.
   - `route_metadata` records only observed route/capture facts.
   - `validation_status` is `captured`, or `excluded` with an
     `exclusion_reason`.
5. Validate the capture using the existing CLI only:

   ```bash
   python scripts/operator_run_capture.py validate \
     --capture local/pr646_substantive_lift_capture.json --for-export
   ```

6. Export the local evidence packet using the existing CLI only:

   ```bash
   python scripts/operator_run_capture.py export \
     --capture local/pr646_substantive_lift_capture.json \
     --out local/pr646_substantive_lift_packet.json
   ```

7. Review qualitatively only. Look for operator-visible differences in whether
   each answer surfaces intent diagnosis, hidden assumption, dominant tradeoff,
   committed recommendation, failure condition, and same-day next action.

## Boundaries and non-claims

- Capture only; do not start the manual evaluation from this prep lane.
- No provider calls, hosted model calls, local model calls, or network calls are
  made by the packet, runbook, tests, or capture harness.
- Do not score, rank, assign a winner, blind, unblind, add a `blind_label`, add
  a `source_map`, add an `identity_map`, or create A/B identity keys.
- Do not use this packet to claim benchmark results, readiness, production
  suitability, provider validation, local-model validation, or Alpha superiority.
- A passing CLI validation means only that the local capture structure is valid
  for the existing operator run capture harness.
- `/v1/solve`, dashboards, APIs, provider routing, local-model routing, and
  route/persona activation remain out of scope.
