"""Region policy utilities"""
from typing import List, Dict

class RegionPolicy:
    def __init__(self, registries: Dict):
        self.regions = registries.get("regions", {}).get("regions", [])

    def _get_region(self, region: str) -> Dict:
        for r in self.regions:
            if r.get("id") == region:
                return r
        return {}

    def allowed(self, vendor_id: str, region: str) -> bool:
        if not vendor_id:
            return True
        r = self._get_region(region)
        if not r:
            return True
        allowed = r.get("allowed_vendors", [])
        return vendor_id in allowed if allowed else True

    def notes(self, vendor_id: str, region: str) -> List[str]:
        notes: List[str] = []
        r = self._get_region(region)
        if not r:
            notes.append(f"region {region} not defined")
            return notes
        rules = r.get("sovereignty_rules", [])
        if rules:
            notes.extend(rules)
        allowed = r.get("allowed_vendors", [])
        if vendor_id and allowed and vendor_id not in allowed:
            notes.append("vendor not allowed")
        blocked = r.get("blocked_endpoints", [])
        if vendor_id in blocked:
            notes.append("vendor endpoint blocked")
        return notes
