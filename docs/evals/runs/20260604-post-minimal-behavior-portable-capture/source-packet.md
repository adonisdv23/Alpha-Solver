# Source Packet

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-PORTABLE-CAPTURE-001`

Status: capture-only source record.

## Source frozen packet

- Frozen packet source path: `docs/evals/runs/20260604-post-minimal-behavior-portable-frozen-packet/`
- Frozen packet commit SHA used: `f950514ff9d74f0ea405104d8a12f601dca725d3`
- Frozen prompt packet file: `docs/evals/runs/20260604-post-minimal-behavior-portable-frozen-packet/frozen-prompt-packet.md`
- PR #265 merge evidence in local history: `f950514ff9d74f0ea405104d8a12f601dca725d3 Add post-improvement frozen prompt packet (#265)`

## Portable contract source

- `alpha_solver_portable.py` path: `alpha_solver_portable.py`
- Capture repository commit containing the portable file: `f950514ff9d74f0ea405104d8a12f601dca725d3`
- `alpha_solver_portable.py` last-modifying commit SHA: `2f9032f3a3994b8126473d89448d579e6785712f`
- `alpha_solver_portable.py` SHA-256 hash: `3064ff6c7f1d0605e9ee7808338e4e564ab80a9e2e00806785cac5a7504faec6`

## Capture authorization summary

The user authorized capture only for `OUTPUT-DIFF-POST-IMPROVEMENT-PORTABLE-CAPTURE-001` using the merged frozen packet from PR #265 exactly. The authorization permits paired output capture, exact raw-output preservation, sanitized scorer-facing material creation, and separate operator-only map preservation.

Alpha uses the portable contract surface.

Plain excludes Alpha protocol text, expert scaffolding, SolverEnvelope requirements, and portable contract content.

`/v1/solve` was not used unless separately proven and authorized.

## Provider/model/tool policy used for both conditions

- Capture generation surface: Codex conversation model surface available in this task.
- Provider/model label available to artifacts: exact provider/model runtime configuration is not exposed by the repository or shell environment; both conditions used the same assistant surface in the same session.
- Tool policy for generation: no browsing, no generation-time tools, no repository runtime provider adapters, no provider orchestration, and no `/v1/solve`.
- Generation settings: no task-visible temperature, seed, or sampling controls were exposed; the same task surface and policy were used for both conditions.

## Legacy-audit gates applied as capture stop conditions

Capture was gated on the following conditions:

- source packet and frozen prompt packet must exist;
- raw paired outputs must be preserved exactly and separately;
- sanitized scorer-facing material must be separate from raw outputs;
- operator-only unblinding map must be separate from scorer-facing material;
- defects and manifest records must be present;
- missing artifacts must not be reconstructed;
- weak, verbose, malformed, surprising, or inconvenient outputs must not trigger selective reruns;
- planning notes or Google Sheets must not be treated as implementation proof;
- offline portable-contract capture must not be treated as `/v1/solve` evidence;
- no self-healing, adaptive-learning, self-optimization, autonomous-optimization, provider-orchestration, MVP-validation, superiority, production-readiness, benchmark, exact-billing, or broad-runtime-readiness claims may be made.
