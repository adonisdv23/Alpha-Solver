# Forbidden artifact content

Future Self Operator artifacts must never persist:

- Secrets.
- Credentials.
- Provider outputs.
- Billing data.
- External API responses.
- Browser data.
- Deployment output.
- Evidence-promotion labels.
- Source-artifact mutations.
- Hosted fallback records.

If any forbidden content would be captured, the future runner must stop and write only a redacted local stop-state artifact if that behavior is explicitly authorized.
