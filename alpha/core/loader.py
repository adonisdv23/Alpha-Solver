"""Simple registry loader using standard library only"""
import json
from pathlib import Path

REGISTRY_CACHE = {}

FILES = {
    "sections": "sections.yaml",
    "questions": "questions.json",
    "risks": "risks.json",
    "playbooks": "templates.playbooks.yaml",
    "policy_routes": "policy.routes.yaml",
    "tools": "tools.json",
}

def load_all(path="registries"):
    base = Path(path)
    for key, fname in FILES.items():
        file_path = base / fname
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                REGISTRY_CACHE[key] = json.load(f)
        else:
            REGISTRY_CACHE[key] = {}
    return REGISTRY_CACHE
