from __future__ import annotations
import asyncio
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
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
    def __init__(
        self,
        config: ObservabilityConfig | None = None,
        *,
        replay_session: str | None = None,
    ):
        self.config = config or ObservabilityConfig.load()
        self.session_id = uuid.uuid4().hex
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
            if replay_session:
                self.replay.load_for_replay(replay_session)

        self.accessibility: Optional[AccessibilityChecker] = None
        if self.config.enable_accessibility:
            self.accessibility = AccessibilityChecker.from_config()
        self._a11y_reports: list[Dict[str, Any]] = []

    def log_event(self, event: Dict[str, Any]) -> None:
        payload = {
            "session_id": self.session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": 1,
            **event,
        }
        if self.replay:
            self.replay.verify(payload)
            self.replay.record(payload)
        if self.logger:
            self.logger.log(payload)

    async def emit_telemetry(self, event: Dict[str, Any]) -> None:
        if self.telemetry:
            await self.telemetry.emit(event)

    def check_text(self, text: str) -> Optional[Dict[str, Any]]:
        if self.accessibility:
            result = self.accessibility.check_text(text)
            self._a11y_reports.append({"text": text, **result})
            return result
        return None

    def export_accessibility(self, base_path: str | Path = "artifacts/reports") -> None:
        if not self._a11y_reports:
            return
        p = Path(base_path)
        p.mkdir(parents=True, exist_ok=True)
        json_path = p / "accessibility.json"
        csv_path = p / "accessibility.csv"
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(self._a11y_reports, f)
        with csv_path.open("w", encoding="utf-8") as f:
            f.write("readability,ok\n")
            for item in self._a11y_reports:
                f.write(f"{item['readability']},{int(item['ok'])}\n")

    def close(self, session_id: str | None = None) -> Optional[str]:
        if self.logger:
            self.logger.close()
        if self.telemetry:
            asyncio.run(self.telemetry.close())
        if self.replay:
            sid = self.replay.save(session_id)
        else:
            sid = None
        self.export_accessibility()
        return sid
