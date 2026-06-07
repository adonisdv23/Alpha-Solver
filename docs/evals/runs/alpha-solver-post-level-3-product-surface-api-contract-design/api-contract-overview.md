# API Contract Overview

## Candidate surface

The candidate product surface considered by this reference is a future HTTP API endpoint named `/v1/solve`. This document does not create, expose, register, test-call, or reserve that endpoint. It only records contract requirements that a later Level 6-controlled lane may use if product-surface work is explicitly approved.

## Contract goals

A future `/v1/solve` contract should be:

1. **Evidence-bounded**: responses must distinguish executed evidence, referenced evidence, missing evidence, and unsupported claims.
2. **Traceable**: every accepted request should be linkable to a request ID, run ID, decision log, validation result, and evidence reference set.
3. **Determinism-aware**: the contract should identify runtime mode, solver profile, and reproducibility inputs without implying deterministic output when nondeterministic providers are used.
4. **Privacy-preserving**: sensitive inputs, secrets, provider payloads, and raw evidence must be redacted or omitted unless a later privacy-reviewed implementation explicitly permits them.
5. **Failure-explicit**: invalid input, missing evidence, unsupported route, unsafe claim, provider unavailable, timeout, and blocked execution states should be represented as structured errors.
6. **Non-promotional**: contract fields must not imply benchmark performance, Alpha superiority, MVP readiness, production readiness, or customer readiness unless later accepted evidence supports those claims.

## Candidate lifecycle

A future route should not exist until implementation gates are satisfied. Candidate lifecycle stages are:

1. design reference only;
2. Level 6 decision on whether to consume or revise this reference;
3. implementation spec approval;
4. route implementation behind explicit non-public gates;
5. offline and mocked tests;
6. privacy, evidence, provider, timeout, and blocked-execution validation;
7. operator review before any public or production exposure.

This packet completes only stage 1.
