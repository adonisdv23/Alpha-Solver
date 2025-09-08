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
    await exporter.emit({"a": 1})
    await exporter.emit({"b": 2})
    await exporter.close()
    assert calls["count"] >= 2
    assert batches and len(batches[0]) == 2
    for item in batches[0]:
        assert {"event", "properties", "timestamp", "session_id", "version"} <= item.keys()


def test_telemetry(tmp_path):
    asyncio.run(_run_exporter(tmp_path))
