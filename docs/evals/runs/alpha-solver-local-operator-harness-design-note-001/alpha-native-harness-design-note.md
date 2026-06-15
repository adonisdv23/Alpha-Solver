# Alpha-native Harness Design Note

## Purpose

This note defines a concise Alpha-native local operator harness concept for future review. The design adapts safe operator-workflow patterns recorded after the Pi.dev feasibility review while preserving Alpha Solver's repo-native specs, evidence boundaries, budget guardrails, and no-runtime-change posture.

## Design concept

An Alpha-native local operator harness would be a local evidence-workbench pattern that helps an operator run authorized repo tasks in a disciplined sequence:

1. choose a committed packet or prompt template by name;
2. declare the branch label, task id, evidence boundary, and stop conditions before work begins;
3. record each operator action as an explicit step with an approval state;
4. preserve raw outputs by pointer, not by uncontrolled copy/paste;
5. attach score pointers, redaction state, non-claims, stop reason, and operator decision;
6. export only sanitized evidence artifacts after review.

For this lane, the harness remains a paper design. No executable automation, provider adapter, local model adapter, dashboard panel, API endpoint, routing change, scoring engine, or package integration is added.

## Why this is not a generic chat UI

The design is evidence-first, not chat-first. A generic chat UI centers a conversation stream. The Alpha-native concept centers lane ids, prompt sources, evidence boundaries, stop conditions, score pointers, non-claims, and export discipline.

The proposed message card is not merely a prettier assistant answer. It is a structured review surface for Alpha's existing discrimination wedge:

- answerability and confidence are recorded before broad claims;
- assumptions, false premises, hidden constraints, and needs-human conditions are visible;
- derivation/no-echo status distinguishes substantive reasoning from prompt reflection;
- route explanations and evidence links make provenance inspectable;
- next-safe-action prevents uncontrolled continuation.

## Why this is not Pi.dev integration

This lane does not install, run, vendor, copy, configure, depend on, or runtime-link Pi.dev. It borrows only high-level workflow ideas that are safe to describe in Alpha's own docs: named prompt packets, explicit operator actions, session-tree evidence, export discipline, interrupt/follow-up semantics, message/evidence-card concepts, local-first defaults, and review rules for any future package or skill.

Any future Pi.dev experiment would require a separate threat model, package/provenance review, sandbox, no-secret fixture workspace, provider/key policy, export policy, and explicit operator authorization. This design note does not grant that authorization.

## Support for Alpha's wedge

### Discrimination

The harness concept keeps discrimination dimensions visible during operator review: false-premise detection, hidden-constraint handling, no-echo substantive derivation, needs-human mapping, confidence calibration, claim-boundary discipline, and evidence-conflict handling. It does not score those dimensions automatically; it specifies where future authorized evidence and score pointers would be recorded.

### Stopping

The harness concept treats stopping as a first-class outcome. A stopped session can be valid evidence if it records the stop condition, missing authorization, missing raw output, failed preflight, evidence conflict, or needs-human gate. This mirrors the blocked Value Read artifact and the failed-closed local Ollama attempt: stopped work must not be converted into success, value, or readiness claims.

### Evidence

The harness concept separates prompt source, raw output pointer, score pointer, redaction status, operator decision, and non-claims. This prevents a session transcript from being mistaken for scored evidence, runtime validation, provider validation, or model-quality evidence.

### Provenance

Each session record would name the lane id, branch label, task id, prompt source, repo commit when available, artifact pointers, and export decisions. Provenance is local-first and review-gated by default.
