# UI-ALPHA-OPERATOR-CONSOLE-CHATGPT-COPY-PASTE-CAPTURE-001 · Operator Console ChatGPT Copy/Paste Capture

## Goal

Add a protected, display-only Operator Console card that explains the manual ChatGPT copy/paste capture workflow without turning the console into a runner, provider client, browser automation tool, capture editor, or artifact writer.

## Motivation

The Operator Console already lists `chatgpt-copy-paste` as a run mode and already summarizes local capture artifacts. Operators still need a safe cockpit answer to: how do I manually collect plain ChatGPT output, routed Alpha output, route/provenance metadata, and validation status without mixing fields or mistaking local artifacts for runtime output?

## Scope

- Add a top-level status section named `chatgpt_copy_paste_capture`.
- Render a compact `ChatGPT Copy/Paste Capture` card on `/dashboard/operator-console`.
- Show mode, disabled automation/provider/live-execution flags, current capture stage, next manual steps, safe terminal snippets, a placeholder-only capture slot template, route metadata guidance, unsafe action labels, and boundary text.
- Derive capture stage only from existing safe local artifact summaries: states, counts, digest-valid evidence status, and other metadata already exposed by the artifact status layer.
- Preserve the existing receipt action as a separate B006 receipt-store action; this card does not auto-save receipts.

## Non-goals and boundaries

This lane is manual-only guidance. It explicitly does not add any ChatGPT API call, provider/model/MCP/network/browser/CLI/subprocess call, `/v1/solve` call, internal solve call, dry-run execution, prompt submission, generated answer, route generation, confidence generation, SAFE-OUT generation, expert trace, shortlist, diagnostics, model output, provider result, billing result, benchmark result, readiness result, credential validation, provider ping, exact billing/spend calculation, capture artifact creation/edit/deletion, evidence packet edit, preflight report edit, receipt mutation, arbitrary file writing, user-supplied path/filename/capture body, raw or partial API key display/storage, raw prompt/output/route metadata/provider payload display/storage, capture/export/preflight schema change, scoring, ranking, winner selection, model-comparison UI, validation claim, readiness claim, benchmark claim, production claim, or superiority claim.

The capture harness remains a local lab notebook, not a runner. The operator generates outputs outside the console and pastes them into the local capture file outside this panel. Any future paste storage, capture editor, browser automation, or API automation must be separately authorized.

## Code targets

- `alpha/webapp/routes/operator_console.py`
- `tests/test_operator_console.py`
- `docs/OPERATOR_CONSOLE.md`
- `.specs/INDEX.md`
- `.specs/UI-ALPHA-OPERATOR-CONSOLE-CHATGPT-COPY-PASTE-CAPTURE-001.md`

## Manual workflow states

`current_capture_stage` is a bounded label:

- `no_capture` — safe artifact summary reports missing capture.
- `capture_invalid` — safe artifact summary reports invalid JSON or invalid structure.
- `capture_scaffolded` — capture is structurally valid and all slots are still pending.
- `capture_in_progress` — capture is structurally valid with captured or excluded slots plus remaining pending work.
- `capture_all_excluded` — capture is structurally valid but has `captured == 0`, `excluded > 0`, and `pending == 0`; it is not export-ready and needs at least one captured case or a revised case packet/capture file.
- `capture_export_ready` — capture is export-ready and no digest-valid evidence packet is present.
- `evidence_packet_available` — evidence packet summary reports a digest-valid packet.

These states are workflow hints only. They do not display raw prompts or outputs and do not assert answer quality, validation, readiness, benchmark, production, billing, or superiority.

## Copy/paste checklist

The status payload and UI expose safe checklist labels only:

- `author_case_packet`
- `run_anchor_preflight_from_terminal`
- `scaffold_capture_from_terminal`
- `collect_plain_chatgpt_output_manually`
- `collect_routed_alpha_output_manually`
- `paste_outputs_into_capture_file`
- `record_observed_route_metadata`
- `validate_capture_from_terminal`
- `run_lift_preflight_from_terminal`
- `export_evidence_packet_from_terminal`
- `save_local_receipt_snapshot_optional`

The placeholder-only slot template is limited to field names and placeholders such as `<task_id>`, `<paste plain ChatGPT output into local capture file>`, `<paste routed Alpha output into local capture file>`, `<observed route/provenance facts only>`, `captured or excluded`, and `<required only when excluded>`.

## Route metadata guidance

Route metadata is for observed route/provenance facts only. It is not scoring, ranking, winner selection, quality judgment, readiness, benchmark, validation, production, billing, or superiority evidence. The UI avoids model-comparison or proof language and uses bounded no-claim labels.

## Test plan

- Verify the status JSON includes `chatgpt_copy_paste_capture` and all disabled/manual-only boundary fields.
- Verify missing, invalid, scaffolded, in-progress, all-excluded, export-ready, and evidence-available stages.
- Verify the stage mapper consumes only safe artifact summaries.
- Verify checklist, template, route metadata guidance, unsafe-action labels, terminal command snippets, and boundary text render safely.
- Verify no raw prompts, raw outputs, raw route metadata, provider payloads, fake secrets, or raw environment sentinels appear in HTML or JSON.
- Verify no new POST route is added and the existing receipt POST route remains unchanged.
- Verify provider constructors patched to raise do not affect page/status routes.
- Verify source scans show no execution/network/provider/browser/solve imports.
- Run focused console tests, relevant capture/API tests, the full test suite, ruff, and narrative claim-safety checks.

## Definition of Done

- The Operator Console has a display-only ChatGPT Copy/Paste Capture card.
- The status JSON exposes bounded manual-only fields and safe stage labels.
- Stage derivation uses only safe local artifact summaries.
- The UI and docs state the manual-only, no-automation, no-provider, no-browser, no-solve, no-CLI/subprocess, no-capture-mutation, no-raw-output-storage boundary.
- The docs state the no-raw, no-secret, no-readiness, no-validation, no-benchmark, no-production, no-superiority, no-scoring, no-ranking, no-winner-selection, and no-model-comparison boundaries.
- Tests cover the required behavior and existing Operator Console panels continue to pass.
