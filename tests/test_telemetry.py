import asyncio

from alpha.core.telemetry import TelemetryExporter


async def _run_exporter(tmp_path):
    calls = {"count": 0}
    batches = []

    async def sender(batch):
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("fail once")
        batches.append(batch)

    exporter = TelemetryExporter(sender, batch_size=2, retry_seconds=0)
    base = {
        "session_id": "s",
        "event": "test",
        "timestamp": 0,
        "version": "1.0",
        "data": {},
    }
    await exporter.emit(base)
    await exporter.emit({**base, "event": "test2"})
    await exporter.close()
    assert calls["count"] >= 2
    assert batches and len(batches[0]) == 2


def test_telemetry(tmp_path):
    asyncio.run(_run_exporter(tmp_path))
