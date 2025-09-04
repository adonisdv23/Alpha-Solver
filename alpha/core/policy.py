"""Simple policy engine for enterprise guardrails"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from collections import deque


class PolicyEngine:
    def __init__(self, registries: dict):
        self.registries = registries
        self.sla_active = {}
        self.sla_records = {}
        self.cb_state = {}
        rules = registries.get("circuit_breakers", {}).get("rules", [])
        self.circuit_rules = {r.get("key"): r for r in rules}

    def check_budget(self, ctx: dict) -> dict:
        limits = self.registries.get("budget_controls", {}).get("limits", {})
        per_call = limits.get("per_call_usd")
        cost = ctx.get("cost_estimate", 0)
        ok = True
        action = "allow"
        reason = ""
        if per_call is not None and cost > per_call:
            ok = False
            action = self.registries.get("budget_controls", {}).get("actions", {}).get("on_breach", "halt")
            reason = "cost estimate exceeds per-call limit"
        return {"ok": ok, "action": action, "reason": reason}

    def get_secret(self, vendor_id: str) -> str:
        secrets = self.registries.get("secrets_vault", {}).get("secrets", [])
        for s in secrets:
            if vendor_id.split('.')[0] in s.get("id", ""):
                return s.get("token", "<redacted-token>")
        return "<redacted-token>"

    def classify(self, data_tags):
        rules = self.registries.get("data_classification", {}).get("rules", [])
        allow = True
        masked = False
        notes = []
        for tag in data_tags:
            for rule in rules:
                if rule.get("match") == tag:
                    action = rule.get("action")
                    if action == "deny":
                        allow = False
                        notes.append(f"denied:{tag}")
                    elif action == "mask":
                        masked = True
                        notes.append(f"masked:{tag}")
        return {"allow": allow, "masked": masked, "notes": notes}

    def circuit_guard(self, key: str) -> dict:
        full_key = key if key.startswith("vendor:") else f"vendor:{key}"
        rule = self.circuit_rules.get(full_key)
        state = self.cb_state.get(full_key, {"state": "closed"})
        allow = state.get("state") != "open"
        return {"state": state.get("state"), "allow": allow}

    def sla_start(self, op: str):
        self.sla_active[op] = time.time()

    def sla_stop(self, op: str, ms: float):
        dq = self.sla_records.setdefault(op, deque(maxlen=100))
        dq.append(ms)
        self.sla_active.pop(op, None)

    def audit(self, event: dict):
        path = Path('registries/audit_trail.json')
        try:
            with path.open('r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = {"version": "0.1.0", "events": []}
        event = dict(event)
        event["timestamp"] = datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
        data.setdefault("events", []).append(event)
        with path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
