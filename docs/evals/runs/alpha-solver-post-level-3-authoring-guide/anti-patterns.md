# Common Anti-Patterns

Avoid these patterns when authoring future post-Level-3 release-readiness packets.

## Claiming readiness from docs-only packets

Unsafe:

> This docs-only packet proves release readiness.

Safe:

> This docs-only packet defines authoring guidance and does not prove release readiness.

## Treating logs as final decision files

Unsafe:

> The decision is authoritative because it appears in `checks-run` output.

Safe:

> The decision is recorded in `selected-next-lane.md`, `selected-next-action.md`, `README.md`, or another authoritative decision file; `checks-run.md` only records validation commands.

## Selecting multiple current next lanes

Unsafe:

> The packet selects Level 4, quality evaluation, provider orchestration, dashboard readiness, `/v1/solve`, billing, benchmark, and MVP readiness lanes.

Safe:

> The packet selects exactly one next lane or one no-further selected next action.

## Omitting blocker fallback lane

Unsafe:

> If this packet is unsafe or incomplete, proceed directly to downstream work.

Safe:

> If this packet is unsafe or incomplete, use the packet's blocker fallback lane.

## Modifying source artifacts to satisfy docs

Unsafe:

> Edit preserved source artifacts so the new packet can claim a cleaner history.

Safe:

> Leave preserved source artifacts unchanged and document any limitation in the new packet boundary.

## Using prior chat context as packet evidence

Unsafe:

> The packet can rely on the previous chat for the accepted prior state.

Safe:

> The packet cites repo source-of-truth files for the accepted prior state.

## Starting downstream work inside a design packet

Unsafe:

> While writing the design packet, also run local model inference, start Ollama, call hosted providers, expose `/v1/solve`, expose dashboard routes, add provider fallback, run benchmarks, perform billing work, or promote evidence.

Safe:

> Keep the packet docs-only and route downstream work to a separately approved lane.
