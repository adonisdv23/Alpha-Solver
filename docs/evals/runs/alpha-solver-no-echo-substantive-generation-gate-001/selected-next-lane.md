# Selected Next Lane

STATUS: VALUE/NO-ECHO-LOCAL BLOCKING NEXT LANE AFTER BLOCKED NO-ECHO GATE.

Value/no-echo-local blocking next lane: `ALPHA-SOLVER-PROMPT-CONSUMPTION-WIRING-FIX-001`

This is a value/no-echo-local blocking next lane only. It does not replace the repo-global selected next lane, which remains controlled by `docs/CURRENT_STATE.md` and `docs/LANE_REGISTRY.md`.

Rationale: the identified local Alpha path echoes prompts in the user-visible final answer fields, so the no-echo/substantive-generation precondition is not met. A focused prompt-consumption/final-answer-generation wiring fix is required before this value/no-echo track can advance.

Do not proceed to value pilot execution, value pilot authorization, or `ALPHA-SOLVER-VALUE-EXPERIMENT-PILOT-AUTHORIZATION-001` until this no-echo blocker is resolved by a focused fix and this gate or a successor no-echo gate passes without provider calls or with separately authorized provider use.
