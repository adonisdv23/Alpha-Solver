from __future__ import annotations
import asyncio
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from .jsonl_logger import JSONLLogger
from .telemetry import TelemetryExporter
from .replay import ReplayHarness
from .accessibility import AccessibilityChecker
from .loader import parse_yaml_lite


@dataclass
class ObservabilityConfig:
    enable_logging: bool = True
    log_path: str = "artifacts/logs/events.jsonl"
    enable_telemetry: bool = False
    enable_replay: bool = True
    enable_accessibility: bool = False
    telemetry_endpoint: Optional[str] = None
    replay_dir: str = "artifacts/replay"

    @classmethod
    def load(cls, path: str | Path = "config/observability.yaml") -> "ObservabilityConfig":
        p = Path(path)
        data: Dict[str, Any] = {}
        if p.exists():
            data = parse_yaml_lite(p.read_text(encoding="utf-8")) or {}
        return cls(**{k: data.get(k, getattr(cls, k)) for k in cls.__annotations__.keys()})


class ObservabilityManager:
    def __init__(self, config: ObservabilityConfig | None = None):
        self.config = config or ObservabilityConfig.load()
        self.logger: Optional[JSONLLogger] = None
        if self.config.enable_logging:
            self.logger = JSONLLogger(self.config.log_path)

        self.telemetry: Optional[TelemetryExporter] = None
        if self.config.enable_telemetry and self.config.telemetry_endpoint:
            async def sender(batch):
                # placeholder sender that writes to a file
                path = Path(self.config.log_path).with_name("telemetry.jsonl")
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("a", encoding="utf-8") as f:
                    for item in batch:
                        f.write(json.dumps(item) + "\n")
            self.telemetry = TelemetryExporter(sender)

        self.replay: Optional[ReplayHarness] = None
        if self.config.enable_replay:
            self.replay = ReplayHarness(self.config.replay_dir)

        self.accessibility: Optional[AccessibilityChecker] = None
        if self.config.enable_accessibility:
            self.accessibility = AccessibilityChecker.from_config()

    def log_event(self, event: Dict[str, Any]) -> None:
        if self.logger:
            self.logger.log(event)
        if self.replay:
            self.replay.record(event)

    async def emit_telemetry(self, event: Dict[str, Any]) -> None:
        if self.telemetry:
            await self.telemetry.emit(event)

    def check_text(self, text: str) -> Optional[Dict[str, Any]]:
        if self.accessibility:
            return self.accessibility.check_text(text)
        return None

    def close(self) -> Optional[str]:
        if self.logger:
            self.logger.close()
        if self.telemetry:
            asyncio.run(self.telemetry.close())
        session_id: Optional[str] = None
        if self.replay:
            session_id = self.replay.save()
        return session_id
