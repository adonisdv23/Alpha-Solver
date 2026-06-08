# Transcript Enrichment Hub Provider vs Local Mac Worker Method Safety Checklist

## 1. Purpose

This docs-only checklist documents the safety boundary for presenting **Provider** and **Local Mac Worker** as two Transcript Enrichment Hub methods. It is intended to guide UI copy, smoke coverage, and review expectations without changing provider activation, provider token handling, local worker assumptions, import behavior, or any runtime code.

This checklist does not deploy, configure provider tokens, mutate Secret Manager, run live provider calls, or authorize changes to `app.py`, `monitor.py`, tests, tools, or scripts.

## 2. Product model

- **Enrichment** is the umbrella workflow for improving transcript-related evidence and metadata.
- **Provider** and **Local Mac Worker** are Enrichment methods, not separate product destinations.
- **Imports** remain a **Preview → Apply** flow.
- **Videos** remains the verification and library destination after accepted enrichment output is applied.
- **Exports** remains the output destination for operator-controlled downstream use.

## 3. Provider method safety

- Show provider status at a high level only, such as disabled, not configured, configured, unavailable, or ready according to existing safe status signals.
- Never display provider token values, secret values, partial tokens, credential payloads, or Secret Manager contents.
- Make disabled or not configured states clear to the operator.
- Do not trigger live provider calls from page load, refresh, tab selection, method selection, status rendering, or passive polling.
- Do not trigger live provider calls unless existing gated controls are intentionally submitted by the operator.
- Do not expose provider activation as a normal action from the primary Enrichment UI.
- Keep live smoke and preflight behavior in Admin/Advanced surfaces, not the primary Enrichment method presentation.

## 4. Local Mac Worker method safety

- Clearly state that Local Mac Worker leaves the browser and requires operator-controlled local execution outside the web page.
- Keep queue or runner download behavior operator controlled.
- Return uploaded local worker results to the existing **Preview → Apply** import flow.
- Do not auto-apply Local Mac Worker results.
- Do not imply or add browser automation.
- Do not imply or add cookies or proxies.
- Do not imply or add media download.
- Do not imply or add Whisper/OpenAI transcription.
- Do not imply or add Native Messaging or a localhost helper.

## 5. Import safety

- Results are previewed before apply.
- Apply requires explicit operator action.
- Failure-only rows do not become success transcript evidence.
- Notes-only rows remain labeled as notes-only rows.
- Raw JSON and detailed evidence payloads stay controlled and should not be overexposed on the primary page.

## 6. UX safety language

- Keep safety copy short on the primary page.
- Use collapsed details for long operational notes.
- Do not hide critical confirmation language needed to prevent accidental apply, provider calls, or unsafe local-worker assumptions.
- Avoid exposing provider activation complexity on the primary page.

## 7. Required test/smoke coverage

Future implementation or UI-change PRs that present Provider and Local Mac Worker as Enrichment methods should preserve or add coverage confirming:

- Provider method visible.
- Local Mac Worker method visible.
- **Preview → Apply** marker visible.
- No auto-apply markers preserved.
- Provider disabled or not configured marker visible.
- Local Worker / Download Mac Local Runner markers preserved.
- Old `/mvp` and `/transcript-rescue` routes reachable.

## 8. Do-not-merge-if list

Do not merge a future implementation or UI-change PR if any of the following are true:

- Provider token values or secret-like values are visible.
- Live call behavior is changed or newly triggered by page load, method selection, status rendering, passive polling, or any ungated action.
- Provider activation is exposed as a normal primary Enrichment UI action.
- Local worker copy or flow implies browser automation, cookies, proxies, media download, Whisper/OpenAI transcription, Native Messaging, or a localhost helper.
- **Preview → Apply** is hidden, weakened, bypassed, or made ambiguous.
- Old `/mvp` or `/transcript-rescue` routes are broken.
- Tests or smoke coverage are weakened.
