# Selected Direction

## Selected direction

`VALUE_READ_DISCRIMINATION_WORKBENCH`

Plain-language name: Value Read / discrimination workbench.

## Operator job-to-be-done

Help the operator understand whether Alpha Solver is producing differentiated, evidence-bounded, route-aware work compared with plain or baseline outputs.

## Source-truth alignment

This direction aligns with:

- discrimination and Value Read evidence
- prompt-contract simulation
- captured outputs and case packets
- route/expert context
- SAFE-OUT and confidence boundaries
- claim-safety controls
- operator decisions before implementation claims

## Relationship to current artifacts

The workbench should organize and explain existing artifacts before it creates new execution behavior. It should help the operator inspect packet state, captured output state, comparison state, scoring boundary state, and next safe action.

## Relationship to Operator Console

The Operator Console becomes a support surface only if it helps the workbench job. It should not become a generic cockpit by default.

## Relationship to B012/B013

B012 and B013 remain deferred. They may become useful support lanes later, but this decision does not authorize them.

## Relationship to route/expert preview

Route and expert preview is strongly aligned, but should be designed as a workbench component first unless a later lane deliberately separates it.

## What it should not become

It should not become a generic prompt runner, dashboard-only status page, uncontrolled model-run surface, or broad readiness claim generator.
