# Expected output format

Future static tests should emit deterministic assertion messages. A failure record should contain:

```json
{
  "id": "SELF_OPERATOR_PROVIDER_CALL_BLOCKED",
  "path": "relative/path.py",
  "reason": "provider invocation pattern is forbidden in the first-code lane",
  "blocked_surface": "provider_calls",
  "recommended_stop_state": "SELF_OPERATOR_PROVIDER_CALL_BLOCKED"
}
```

The test suite may use Python assertions instead of writing JSON artifacts, but review notes must preserve equivalent information.
