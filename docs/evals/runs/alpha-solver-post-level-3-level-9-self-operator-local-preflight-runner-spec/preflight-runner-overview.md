# Preflight runner overview

A future local preflight runner, if separately authorized, may perform local static readiness checks before a Self Operator lane starts. It must be offline, deterministic, operator-supervised, and fail closed.

The runner must not execute implementation tasks. It may only report whether preflight conditions are satisfied.
