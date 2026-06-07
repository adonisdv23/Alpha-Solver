# Prompt 3 Assumption Routing Summary

Prompt shape `bounded_local_python_cli_startup_plan` covers the manual smoke Prompt 3 style:

`Draft a concise execution plan to improve a small Python CLI’s startup time when only profiling later is available; state assumptions.`

For this shape, Pass 1 may route to `answer_with_assumptions` only when confidence is parseable and at or above threshold, considerations are present and bounded, assumptions are present and bounded, missing information is bounded, assumptions are not none/unknown/unbounded, no explicit serious-risk terms are present, and no forbidden boundary claims are present.

The runner does not fabricate assumptions. Failed confidence, missing assumptions, unknown/unbounded assumptions, too-broad missing information, explicit serious risk, or boundary claims prevent `answer_with_assumptions`.
