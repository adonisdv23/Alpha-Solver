# UI-KEYS-001 · Dashboard: API Keys Management

## Goal
Implement Dashboard: API Keys Management in track RES_Dash with enforceable tests.

## Acceptance Criteria
- Create, update and delete provider API keys (OpenAI/Claude/etc.).
- Mask provider secrets on read (****last4) and persist via a secrets backend shim.
- Emit an audit log entry for every change while keeping plaintext out of the log.
- Provide automated tests that verify the UI behaviour (10/10 passing).

## Code Targets
- `alpha/webapp/routes/settings.py`
- `alpha/webapp/templates/settings.html`
- `tests/ui/test_settings.py`

## Notes
- Settings page supports provider API key lifecycle management.
- Persistence occurs through a lightweight secrets backend (env/kv, gitignored).
- Templates follow `ui_keys_v1` baseline.
