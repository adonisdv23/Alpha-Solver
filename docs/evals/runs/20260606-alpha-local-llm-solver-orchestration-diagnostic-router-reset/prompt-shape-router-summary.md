# Prompt Shape Router Summary

The runner classifies prompt shape before Pass 1, then only applies shape-specific routing after Pass 1 is non-evidence, non-echoed, parseable, boundary-clean, and free of explicit serious-risk terms.

Prompt shapes:

- `underspecified_edit_or_performance`
- `bounded_local_python_cli_startup_plan`
- `explicit_high_risk`
- `boundary_claim_guard`
- `generic`

For the two known-safe smoke prompt shapes, vague model-produced risk labels are advisory. Explicit serious-risk content and forbidden boundary claims still block or fail closed. Generic unknown shapes retain conservative risk behavior.
