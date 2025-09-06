import json
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Decision:
    decision: str  # "allow" | "block" | "warn"
    reason: str


class PolicyEngine:
    """Minimal governance engine with deterministic budgets and audit logging."""

    def __init__(
        self,
        *,
        max_steps: int = 0,
        max_seconds: float = 0.0,
        breaker_max_fails: int = 0,
        dry_run: bool = False,
        data_policy_path: Optional[str] = None,
        run_id: Optional[str] = None,
        audit_path: str = "artifacts/policy_audit.jsonl",
    ) -> None:
        self.max_steps = int(max_steps)
        self.max_seconds = float(max_seconds)
        self.breaker_max_fails = int(breaker_max_fails)
        self.dry_run = bool(dry_run)
        self.run_id = run_id or uuid.uuid4().hex
        self.audit_path = Path(audit_path)
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)

        self.start_time = time.time()
        self.steps = 0
        self.fails = 0

        self.now_utc = (
            datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )
        self._header_written = False

        self.data_policy = {
            "deny": {"families": [], "tags": []},
            "allow": {"families": [], "tags": []},
        }
        path = Path(data_policy_path or "data_policy.json")
        if path.exists():
            try:
                with path.open("r", encoding="utf-8") as f:
                    dp = json.load(f)
                if isinstance(dp, dict):
                    deny = dp.get("deny", {}) or {}
                    allow = dp.get("allow", {}) or {}
                    self.data_policy = {
                        "deny": {
                            "families": list(deny.get("families", [])),
                            "tags": list(deny.get("tags", [])),
                        },
                        "allow": {
                            "families": list(allow.get("families", [])),
                            "tags": list(allow.get("tags", [])),
                        },
                    }
            except Exception:
                pass

        self._write_header()

    # ------------------------------------------------------------------
    # internal helpers
    def _write_header(self) -> None:
        if self._header_written:
            return
        rec = {"run_id": self.run_id, "now_utc": self.now_utc}
        # attempt to include code version; ignore on failure
        try:
            import subprocess

            rec["code_version"] = (
                subprocess.check_output(["git", "rev-parse", "HEAD"], text=True)
                .strip()
            )
        except Exception:
            pass
        with self.audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self._header_written = True

    def _log(self, rec: Dict[str, object]) -> None:
        rec = dict(rec)
        rec["timestamp"] = datetime.now(timezone.utc).isoformat().replace(
            "+00:00", "Z"
        )
        with self.audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # ------------------------------------------------------------------
    def decide(
        self,
        *,
        query: str = "",
        region: str = "",
        tool_id: str = "",
        family: str = "",
        tags: Optional[List[str]] = None,
    ) -> Decision:
        """Return policy decision for the next step and audit it."""

        step_index = self.steps + 1
        tags = tags or []
        elapsed = time.time() - self.start_time

        data_status = "allow"
        if family in self.data_policy["deny"]["families"] or any(
            t in self.data_policy["deny"]["tags"] for t in tags
        ):
            data_status = "deny"

        budget = {
            "steps": step_index,
            "max_steps": self.max_steps,
            "elapsed_s": round(elapsed, 3),
            "max_seconds": self.max_seconds,
        }
        breaker_state = {
            "fails": self.fails,
            "max_fails": self.breaker_max_fails,
            "tripped": self.breaker_max_fails > 0
            and self.fails >= self.breaker_max_fails,
        }
        data_class = {"family": family, "tags": tags, "status": data_status}

        decision = "allow"
        reason = ""
        if self.max_steps and step_index > self.max_steps:
            decision = "block"
            reason = "max_steps exceeded"
        elif self.max_seconds and elapsed > self.max_seconds:
            decision = "block"
            reason = "max_seconds exceeded"
        elif breaker_state["tripped"]:
            decision = "block"
            reason = "circuit breaker tripped"
        elif data_status == "deny":
            decision = "block"
            reason = "data policy deny"

        audit_decision = decision
        if self.dry_run and decision == "block":
            audit_decision = "warn"
            decision = "allow"

        rec = {
            "run_id": self.run_id,
            "step_index": step_index,
            "query": query,
            "region": region,
            "tool_id": tool_id,
            "decision": audit_decision,
            "reason": reason,
            "budget": budget,
            "breaker": breaker_state,
            "data_class": data_class,
        }
        self._log(rec)
        return Decision(audit_decision if self.dry_run else decision, reason)

    def record_step_result(self, success: bool) -> None:
        """Update counters based on step success or failure."""
        if success:
            self.fails = 0
        else:
            self.fails += 1
        self.steps += 1
