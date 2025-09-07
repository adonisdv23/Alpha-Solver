from __future__ import annotations
import asyncio
from typing import Any, Awaitable, Callable, Dict, List

REQUIRED_FIELDS = {"session_id", "event", "timestamp", "version", "data"}


def validate_event(event: Dict[str, Any]) -> None:
    """Validate telemetry event against the required schema."""
    missing = REQUIRED_FIELDS - event.keys()
    if missing:
        raise ValueError(f"missing telemetry fields: {sorted(missing)}")


class TelemetryExporter:
    """Asynchronous telemetry exporter with batching, retry and validation."""

    def __init__(
        self,
        sender: Callable[[List[Dict[str, Any]]], Awaitable[None]],
        batch_size: int = 10,
        retry_seconds: float = 0.1,
    ):
        self.sender = sender
        self.batch_size = batch_size
        self.retry_seconds = retry_seconds
        self.queue: asyncio.Queue[Dict[str, Any] | None] = asyncio.Queue()
        self._task = asyncio.create_task(self._worker())

    async def _worker(self) -> None:
        batch: List[Dict[str, Any]] = []
        while True:
            item = await self.queue.get()
            if item is None:
                break
            batch.append(item)
            if len(batch) >= self.batch_size:
                await self._flush(batch)
                batch = []
        if batch:
            await self._flush(batch)

    async def _flush(self, batch: List[Dict[str, Any]]) -> None:
        while True:
            try:
                await self.sender(batch)
                break
            except Exception:
                await asyncio.sleep(self.retry_seconds)

    async def emit(self, event: Dict[str, Any]) -> None:
        validate_event(event)
        await self.queue.put(event)

    async def close(self) -> None:
        await self.queue.put(None)
        await self._task
