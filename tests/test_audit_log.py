import json
import time
from io import StringIO

from service.audit import audit_log, exporter
from service.audit.hash_chain import ZERO_HASH


CTX = {"principal": {"tenant_id": "t1", "sub": "user"}}


def test_integrity_and_corruption_detection():
    log = audit_log.AuditLog()
    for i in range(5):
        log.record("system.start", {"i": i}, CTX)
    assert audit_log.verify(log.iter_entries()) is None

    entries = log.iter_entries()
    entries[2]["payload"]["i"] = 999  # mutate
    assert audit_log.verify(entries) == 2


def test_redaction_rules():
    payload = {
        "email": "user@example.com",
        "phone": "555-123-4567",
        "token": "secret-token-abc",
    }
    log = audit_log.AuditLog()
    entry = log.record("auth.login", payload, CTX)
    stored = entry["payload"]
    assert "example.com" not in json.dumps(stored)
    assert "555" not in json.dumps(stored)
    assert "secret" not in json.dumps(stored)


def test_perf_p95_under_budget():
    log = audit_log.AuditLog()
    times = []
    for i in range(1000):
        start = time.monotonic()
        log.record("auth.login", {"n": i}, CTX)
        times.append(time.monotonic() - start)
    times.sort()
    p95 = times[int(0.95 * len(times))]
    assert p95 <= 0.05


def test_retention_compaction():
    log = audit_log.AuditLog(retention_days=1)
    first = log.record("system.start", {}, CTX)
    # simulate old entry
    log._entries[0]["ts"] = time.time() - 2 * 24 * 3600
    second = log.record("system.ready", {}, CTX)
    entries = log.iter_entries()
    assert len(entries) == 1
    assert entries[0]["id"] == second["id"]
    assert entries[0]["prev_hash"] == ZERO_HASH


def test_export_jsonl_manifest():
    log = audit_log.AuditLog()
    log.record("auth.login", {}, CTX)
    time.sleep(0.01)
    log.record("policy.deny", {}, {"principal": {"tenant_id": "t2"}})

    start = 0
    end = time.time() + 1
    buf = StringIO()
    manifest = exporter.export(
        log.iter_entries(), buf, start_ts=start, end_ts=end, tenant_id="t1"
    )
    lines = [json.loads(l) for l in buf.getvalue().strip().splitlines()]
    assert manifest["count"] == len(lines) == 1
    assert lines[0]["tenant_id"] == "t1"
    assert manifest["head"] == manifest["tail"] == lines[0]["hash"]
