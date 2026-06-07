# Selected-Next and Blocker Fallback Authoring

Selected-next and blocker fallback files keep packet continuity clear for future agents and guardrail checks.

## Selected-next lane files

Use `selected-next-lane.md` when the packet intentionally selects one future packet lane. Use `selected-next-action.md` when the packet closes with a no-further action instead of selecting a future lane. Do not include both files in the same packet unless a future checker explicitly allows that pattern.

A selected-next file should contain:

1. A short heading.
2. Exactly one selected lane or action.
3. Rationale for why that state follows from the packet.
4. A non-start statement when the selection identifies future work.

Safe wording for a future lane:

> This packet selects exactly one next lane: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-4-PRE-PRODUCT-SURFACE-REQUIREMENTS-PACKET-001`.
>
> This selection does not start Level 4. It only identifies the next packet to create if work continues.

Safe wording for a closed/no-further action:

> Selected next action: `NO_FURTHER_RELEASE_READINESS_AUTHORING_GUIDE_LANES_SELECTED`.
>
> No follow-on lane is started by this guide.

Unsafe wording:

> Level 4 is selected, and the packet also begins MVP readiness implementation.

## Blocker fallback lane files

Use `blocker-fallback-lane.md` to identify the fix lane that should be used if the packet is incomplete, inconsistent, unsafe, or unable to preserve the accepted evidence boundary.

A blocker fallback file should contain:

- The fallback lane token.
- The conditions that route work to the fallback lane.
- A statement that the fallback lane fixes the current packet rather than starting downstream product work.

Safe wording:

> If this packet is incomplete, inconsistent, or unable to preserve the evidence boundary, use `ALPHA-SOLVER-POST-LEVEL-3-RELEASE-READINESS-AUTHORING-GUIDE-FIX-001`.

Unsafe wording:

> If blocked, skip the fix lane and begin `/v1/solve`, dashboard, provider orchestration, or MVP readiness work.

## Continuity rules

- Preserve the accepted prior state in the README or equivalent packet overview.
- Select only one current next lane or one no-further action.
- Keep fallback state separate from selected-next state.
- Do not treat fallback lanes as product lanes.
- Do not use prior chat context as packet evidence.
