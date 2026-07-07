# UI-ALPHA-OPERATOR-CONSOLE-LOCAL-ARTIFACT-STATUS-001 · Operator Console Local Artifact Status

Status: Implemented

## Goal

Make the read-only Operator Console more useful by showing whether local
operator artifacts (capture, evidence packet, anchor/lift preflight reports)
exist under a fixed local directory and whether they are structurally valid —
without executing any workflow, provider, model, `/v1/solve`, MCP, browser
automation, network call, or CLI command. This is an artifact-status lane, not
a workbench-action lane.

## Motivation

The console shell (`UI-ALPHA-OPERATOR-CONSOLE-MVP-001`) renders route/trace and
evidence/receipt fields as static "not run yet" placeholders. Operators already
produce local capture and export artifacts with the operator run capture
harness, but the console could not tell them whether those artifacts exist or
whether they are structurally valid. This lane wires the console to read a
narrow, fixed local directory and display compact, safe status for the four
known artifact files, reusing the harness's own validation and digest helpers.

## Scope

- `alpha/webapp/operator_console_artifacts.py` (new): read-only helper.
  - `resolve_artifact_root()` returns the fixed `local/operator_console/`
    directory under the repo root. An optional override env
    (`ALPHA_OPERATOR_CONSOLE_ARTIFACT_ROOT`) is honored only when it resolves to
    a path inside the repository root; path-traversal and outside-root values
    are rejected and the fixed default is used.
  - `summarize_capture` / `summarize_evidence_packet` /
    `summarize_anchor_preflight` / `summarize_lift_preflight` read at most one
    fixed file each and return counts/states/schema-version/id/digest only.
    Missing files report `missing`; malformed JSON reports `invalid_json`;
    structurally invalid JSON reports `invalid_structure`.
  - Capture reuses `operator_run_capture.validate_capture`; the evidence packet
    reuses `operator_run_capture.verify_packet_digest`
    (`digest_valid` / `digest_invalid` / `digest_unverifiable`).
  - `build_artifact_status()` assembles the four summaries plus the artifact
    root, a `detected` flag, and the boundary statements.
- `alpha/webapp/routes/operator_console.py`: adds a `local_artifacts` section to
  the status payload and surfaces artifact-derived rows in the Route and Trace,
  Preflight and Capture, and Evidence and Receipt cards, plus the boundary
  statements. When nothing is detected the cards remain stable and show
  "No local operator artifacts detected."
- `.gitignore`: ignore `local/` so operator artifacts stay untracked.
- `docs/OPERATOR_CONSOLE.md`: artifact-status section, root/path policy, and the
  raw-output non-display and no-execution boundaries.
- Tests in `tests/test_operator_console.py`.

## Non-goals and boundaries

- No provider, hosted-model, local-model, MCP, tool, browser, network, or
  `/v1/solve` call; no CLI execution from the UI.
- No create, modify, delete, upload, edit, or save of any artifact; the four
  files are read-only inputs.
- No raw prompts, baseline outputs, routed outputs, raw route metadata, system
  prompts, or provider payloads are displayed by default. Only counts, states,
  schema versions, ids, and the content digest (a hash) are surfaced.
- No API key storage or raw/partial key display; existing categorical key
  status is preserved.
- No change to `alpha_solver_portable.py`, provider runtime, model routing,
  `/v1/solve` execution, the capture/export schemas, or the
  `operator_run_capture.py` CLI semantics.
- No scoring, ranking, winner fields, blind labels, source maps, identity maps,
  A/B identity keys, or model-comparison UI.
- No benchmark, readiness, production, provider-validation, local-model, or
  superiority claims. A preflight report being present is not a quality or
  readiness signal.

## Boundary statements

The UI and status JSON include language equivalent to:

- Local artifacts are structural support artifacts only.
- This console does not execute providers, models, /v1/solve, MCP, tools,
  browser automation, or CLI commands.
- No raw prompts or raw outputs are displayed by default.
- No answer-quality, benchmark, readiness, production, validation, or
  superiority claim is made.

## Code Targets

- `alpha/webapp/operator_console_artifacts.py`
- `alpha/webapp/routes/operator_console.py`
- `tests/test_operator_console.py`
- `docs/OPERATOR_CONSOLE.md`
- `.gitignore`

## Test Plan

`tests/test_operator_console.py`: no local artifacts (renders, status reports
not detected); a valid capture (schema version, packet id, total/captured/
excluded/pending counts, route-metadata presence count, no raw case content);
invalid JSON and structurally invalid capture fail safe with no server error; a
valid evidence packet (id, schema, counts, content digest, digest verified); a
tampered packet reports `digest_invalid` and a digest-less packet reports
`digest_unverifiable`; anchor/lift preflight reports surface needs-attention and
state counts without raw case detail; the override env rejects outside-root and
traversal paths and honors an inside-repo path; a fake `OPENAI_API_KEY` never
appears in HTML or JSON; recognizable raw prompt/baseline/routed/route-metadata
text never appears in HTML or JSON; and no provider client is constructed or
executed when artifacts are present.

## Validation

- `python -m pytest tests/test_operator_console.py -q`
- `python -m pytest tests/test_operator_run_capture.py -q`
- `python -m pytest tests/test_api_endpoints.py -q`
- `python -m pytest -q`
- `ruff check alpha/webapp/operator_console_artifacts.py alpha/webapp/routes/operator_console.py tests/test_operator_console.py`
- `python scripts/check_narrative_claim_safety.py docs/OPERATOR_CONSOLE.md .specs/UI-ALPHA-OPERATOR-CONSOLE-LOCAL-ARTIFACT-STATUS-001.md`

## Definition of Done

The helper, console wiring, docs, tests, and this spec merged; all validation
commands pass; the console reads only the fixed local directory (or a safe
inside-repo override); missing and malformed artifacts fail safe; no raw
prompt, output, route metadata, or secret is displayed; and no provider-call
path is exercised. Reporting an artifact as structurally valid or a digest as
valid means only that the configured structural rules or the recorded hash
held; it is not a quality, benchmark, readiness, or superiority judgment.
