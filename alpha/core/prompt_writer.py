"""Write prompts to disk"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

class PromptWriter:
    def __init__(self, base_dir: str = "artifacts/prompts"):
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.root = Path(base_dir) / ts
        self.root.mkdir(parents=True, exist_ok=True)

    def write(self, index: int, prompt: Dict[str, object]) -> Path:
        step_dir = self.root / f"step_{index}"
        step_dir.mkdir(parents=True, exist_ok=True)
        (step_dir / "system.txt").write_text(str(prompt.get("system", "")), encoding="utf-8")
        (step_dir / "user.txt").write_text(str(prompt.get("user", "")), encoding="utf-8")
        (step_dir / "schema.json").write_text(json.dumps(prompt.get("schema", {}), ensure_ascii=False), encoding="utf-8")
        return step_dir
