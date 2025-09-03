"""Simple orchestrator"""
from typing import Dict, List
from .loader import REGISTRY_CACHE

def plan(playbook_id: str, shortlist: List[Dict]) -> Dict:
    playbooks = REGISTRY_CACHE.get("playbooks", {}).get("playbooks", {})
    return playbooks.get(playbook_id, {})
