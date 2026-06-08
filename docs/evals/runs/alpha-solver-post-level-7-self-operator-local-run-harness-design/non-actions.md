# Non-Actions

This docs-only packet does not take or authorize the following actions:

- Does not create a runner.
- Does not start Level 8.
- Does not implement Self Operator.
- Does not execute Self Operator tasks.
- Does not run models.
- Does not call providers.
- Does not call hosted models.
- Does not call external APIs.
- Does not modify runtime code.
- Does not modify provider code.
- Does not modify API files.
- Does not modify dashboard files.
- Does not modify CLI files.
- Does not modify checker scripts.
- Does not modify tests.
- Does not modify the Makefile.
- Does not modify CI workflows.
- Does not modify source-artifact files.
- Does not configure credentials or secrets.
- Does not add provider routing.
- Does not add provider fallback.
- Does not add hosted fallback.
- Does not expose or call `/v1/solve`.
- Does not expose dashboards.
- Does not run benchmarks.
- Does not perform billing work.
- Does not deploy.
- Does not control browsers.
- Does not promote evidence.

Evidence boundary: Docs-only local harness design. This does not create a runner, execute tasks, run models, call providers, modify runtime, expose dashboards, expose `/v1/solve`, deploy, control browsers, use credentials, incur billing, add fallback, or promote evidence.
