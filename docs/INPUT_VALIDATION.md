# Input Validation & Sanitization

Incoming requests are first sanitized then validated against a strict JSON schema.

## Schema

Required fields:

- `prompt` – string, 1-1000 characters.
- `task` – string enum: `solve` or `plan`.
- `opts` – optional object. Known keys:
  - `strategy` – enum: `react`, `cot`, `tot`.
  - `timeout` – number 0-60 seconds.

No additional top-level properties are allowed.

## Sanitizer

The sanitizer removes or redacts dangerous input before validation:

- Strips `<script>` tags, event handlers like `onload=`, and `javascript:` URLs.
- Removes SQL injection markers such as `;`, `--`, `DROP TABLE`.
- Collapses control characters and excessive whitespace.
- Redacts obvious secrets (`api`, `token`, `key` patterns) and masks emails/phones.

Sanitization happens before schema validation. Sanitized values are passed to
downstream handlers and stored in place of the original payload.

### Examples

Input:
```json
{"prompt": "<script>alert(1)</script> contact me test@example.com", "task": "solve"}
```

Output:
```json
{"prompt": "contact me t***@e***.com", "task": "solve"}
```
