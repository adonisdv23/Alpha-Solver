from __future__ import annotations

"""Helpers for producing deterministic tuning reports."""

from typing import Dict, Any


def build_report(
    before: Dict[str, Any],
    after: Dict[str, Any],
    before_weights: Dict[str, float],
    after_weights: Dict[str, float],
) -> Dict[str, Any]:
    """Return a machine friendly report dictionary."""
    delta_acc = after["accuracy"] - before["accuracy"]
    factors = sorted(set(before_weights) | set(after_weights))
    weight_delta = {
        f: after_weights.get(f, 0.0) - before_weights.get(f, 0.0) for f in factors
    }
    before_payload = dict(before)
    before_payload["weights"] = before_weights
    after_payload = dict(after)
    after_payload["weights"] = after_weights
    return {
        "before": before_payload,
        "after": after_payload,
        "delta_accuracy": delta_acc,
        "weight_delta": weight_delta,
        "confusion_before": before.get("confusion", {}),
        "confusion_after": after.get("confusion", {}),
    }


def to_text(report: Dict[str, Any]) -> str:
    """Render *report* into a human friendly multi-line string."""
    lines = [
        f"BEFORE accuracy: {report['before']['accuracy']:.3f}",
        f"AFTER  accuracy: {report['after']['accuracy']:.3f}",
        f"DELTA  accuracy: {report['delta_accuracy']:.3f}",
    ]
    lines.append("Weights:")
    for name, delta in report["weight_delta"].items():
        before = report["before"].get("weights", {}).get(name, 0.0)
        after = report["after"].get("weights", {}).get(name, 0.0)
        lines.append(f"  {name}: {before:.3f} -> {after:.3f} (Δ {delta:+.3f})")
    return "\n".join(lines)
