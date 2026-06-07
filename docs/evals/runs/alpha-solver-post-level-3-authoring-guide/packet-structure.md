# Packet Structure for Future Post-Level-3 Packets

Future `alpha-solver-post-level-3-*` packets should be narrow, docs-first, and explicit about what they do not prove. A packet should be understandable from its files alone, without relying on prior chat context, command history, or uncommitted operator memory.

## Required structure

Use a directory under `docs/evals/runs/` with a stable lane-oriented name. Within that directory, include authoritative decision files rather than burying decisions in command logs.

A typical packet should include:

- `README.md` with the lane name, purpose, accepted prior state, files in the packet, selected next state, blocker fallback lane, and evidence boundary.
- A source-evidence section or file that lists the repo artifacts reviewed before authoring.
- One or more design or requirements files that contain the actual packet content.
- `selected-next-lane.md` or `selected-next-action.md`, but not both for the same packet.
- `blocker-fallback-lane.md` when the packet records or depends on a blocker fallback state.
- A boundary file such as `evidence-boundary.md`, `blocked-claims.md`, `non-actions.md`, or an equivalent file that keeps unsupported claims blocked.
- `checks-run.md` that records validation commands, while making clear that command logs are not authoritative decision files.

## Lane naming

Use one lane token for the packet itself and one current selected-next state. The selected-next state may be a future packet lane or a closed/no-further action, but it must not select competing lanes.

Safe wording:

> This packet selects exactly one next lane: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-4-PRE-PRODUCT-SURFACE-REQUIREMENTS-PACKET-001`.

Unsafe wording:

> This packet selects Level 4, provider orchestration, dashboard readiness, and MVP readiness as current next lanes.

## Decision files versus logs

Decision markers belong in authoritative packet files such as `README.md`, `selected-next-lane.md`, `selected-next-action.md`, `final-decision.md`, or a comparable decision file. `checks-run.md` may record that a command found a marker, but the marker must also be present in an authoritative file.

Safe wording:

> `checks-run.md` records checks only; it does not establish the packet decision.

Unsafe wording:

> The `rg` output in `checks-run.md` is the final selected-next decision.

## Source artifacts

Do not edit preserved source artifacts to make a new packet easier to write. If a source artifact appears stale or confusing, record the limitation and use a blocker fallback lane rather than modifying preserved evidence.
