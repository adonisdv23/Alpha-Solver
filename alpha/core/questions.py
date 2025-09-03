"""Question utilities"""
from typing import Dict, List, Optional
from .loader import REGISTRY_CACHE

def get_required_questions(domains: Optional[List[str]] = None) -> Dict[str, List[Dict]]:
    data = REGISTRY_CACHE.get("questions", {}).get("questions", {})
    if domains:
        return {k: data.get(k, []) for k in domains}
    return data
