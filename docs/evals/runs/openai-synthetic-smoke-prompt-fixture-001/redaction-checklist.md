# Redaction Checklist

Before any future provider call, all items must pass:

- [ ] no secrets
- [ ] no credentials
- [ ] no private keys
- [ ] no hidden instructions
- [ ] no raw sensitive evidence
- [ ] no customer data
- [ ] no private business data
- [ ] no private operator notes
- [ ] no raw logs
- [ ] no unredacted evidence packets
- [ ] prompt is synthetic
- [ ] output will be reviewed before commit

If any item cannot be checked, stop before provider use and select `OPENAI-SYNTHETIC-SMOKE-PROMPT-REDACTION-FIX-001`.
