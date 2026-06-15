# Generation Protocol

## Mechanism

This lane uses manual no-provider prompt-contract simulation only. The repo agent generated documentation artifacts from committed synthetic Value Read packet material. No product/runtime execution occurred.

## Alpha arm behavior

The Alpha arm follows `alpha_solver_portable.py` as the behavior contract: direct answer first inside `SOLUTION`, compact caveats where appropriate, evidence-boundary discipline, SAFE-OUT behavior for unsupported premises or escalation risk, and SolverEnvelope-shaped labels. The Alpha arm must not call providers, local models, runtime endpoints, dashboards, public APIs, or Google Sheets.

## Baseline arm behavior

The baseline arm is a plain assistant-style answer without Alpha Solver routing, persona, SAFE-OUT protocol, expert-team framing, or SolverEnvelope requirements. It still stays within the lane boundaries and does not perform provider calls, local model calls, scoring, unblinding, or interpretation.

## Raw-output preservation

Raw outputs under `raw/alpha/` and `raw/baseline/` are preserved as generated documentation artifacts. They must not be edited after generation except for explicit clerical correction in a separately documented follow-up. They must not be scored, summarized, unblinded, or interpreted in this lane.
