# Audit Logging (Immutable)

The audit log records security‐relevant events in an append‐only, hash‐chained
sequence.  Each entry contains:

```json
{
  "ts": <float seconds>,
  "id": <sequential int>,
  "tenant_id": "<tenant>",
  "type": "<event type>",
  "payload": {"…"},
  "prev_hash": "<sha256>",
  "hash": "<sha256>"
}
```

The hash is computed as `SHA256(canonical_json(entry_without_hash) + prev_hash)`
providing tamper–evidence.  Retention is enforced on write based on
`retention_days` from `service/config/audit.yaml`.

## Usage

```python
from service.audit import audit_log, exporter

ctx = {"principal": {"tenant_id": "t1", "sub": "user"}}
audit_log.record("auth.login", {"ip": "1.2.3.4"}, ctx)

# verify existing log
assert audit_log.verify(audit_log._audit_log.iter_entries()) is None
```

## Export

```python
from io import StringIO
from service.audit import exporter

buf = StringIO()
manifest = exporter.export(audit_log._audit_log.iter_entries(), buf)
print(manifest)
print(buf.getvalue())  # JSONL
```

## Troubleshooting

* **Verification fails** – `verify()` returns the index of the first corrupt
  entry.  Inspect or rebuild the log from backups.
* **Secrets in payloads** – ensure all sensitive fields match the basic
  redaction rules (emails, phone numbers, token/password like substrings).
* **Performance** – writes should complete in <50ms p95; if exceeded, check
  disk or locking contention.
