# Failure Source Summary

The source artifacts reviewed for this lane were the preserved local orchestration manual-smoke source and import-final-decision packages from 2026-06-06.

The recorded pass-one boundary and gating problems were:

- a simple direct prompt was clarified because pass one returned no considerations;
- an underspecified optimization prompt was blocked instead of clarified;
- a bounded assumption-planning prompt was blocked because ordinary optimization/profiling risk flags were treated as blocking;
- a clearly unsafe concealment/safety-disabling prompt was blocked as expected;
- pass-one model-produced fields included positive boundary-claim language and needed deterministic non-exposure enforcement.

This file summarizes failure inputs only. It is not smoke execution, runtime evidence, model-quality evidence, or readiness evidence.
