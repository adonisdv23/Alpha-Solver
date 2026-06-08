# Non-Actions

This packet is docs-only routing and selection policy design.

It does not implement routing.

It does not call providers.

It does not select providers at runtime.

It does not add fallback, retry, load balancing, model aliasing, or provider preference logic.

It does not modify runtime, provider, API, dashboard, CLI, checker, test, Makefile, CI, or source-artifact files.

It does not expose `/v1/solve` or any product surface.

It does not run models, run benchmarks, perform billing work, create provider credentials, or change environment expectations.

It does not promote evidence, approve evidence for product claims, or change the status of any existing eval result.

Level 7 controls whether and how this packet is used.
