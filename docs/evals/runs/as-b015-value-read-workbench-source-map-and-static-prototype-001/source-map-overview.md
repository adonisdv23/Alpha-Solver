# Source Map Overview

## Purpose

This source map translates B014's workbench design into display-ready source boundaries. It tells a future static mockup or implementation lane what can be shown from committed files, what can only be described at packet-family level, what is inferred from source truth, what is unknown, and what would require future parser or adapter work.

## Design principle

Do not promote artifact existence into quality evidence. The workbench is packet-centered and operator-controlled: it displays source-truth status, missing artifacts, claim boundaries, and one safe next action.

## Certainty classes

- `exact`: a committed file path is known.
- `packet_family`: a family of committed packets exists, but this lane does not name every per-task source.
- `inferred`: status follows from source-truth text or packet-family posture.
- `unknown`: no committed source was identified in this lane.
- `future_required`: a future parser, inventory, adapter, or mockup fixture is required before automatic display.

## Source discipline

If a source path or field is not committed, the display must say `unknown`, `packet family only`, or `future_required`. Missing route metadata, missing scores, or missing interpretation must not be treated as failure unless the packet requires that input.
