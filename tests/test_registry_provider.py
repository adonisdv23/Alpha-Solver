
import json, math, pathlib

SEED_PATH = pathlib.Path(__file__).resolve().parents[1] / "registries" / "registry_seed_v0_7_0.jsonl"

def _load_seed():
    rows = []
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line: 
                continue
            rows.append(json.loads(line))
    return rows

def _score(row, query):
    q = query.lower()
    fields = [
        row.get("bucket","") or "",
        row.get("category","") or "",
        row.get("primary_use_case","") or "",
        " ".join(row.get("capabilities",[]) or []),
        " ".join(row.get("best_integration_scenarios",[]) or []),
    ]
    text = " ".join(fields).lower()
    fit = 1.0 if any(tok in text for tok in q.split()) else 0.4
    sentiment = row.get("sentiment_score_0_10") or 7.0
    sentiment_prior = 0.6 + (sentiment/10.0)*0.6  # 0.6..1.2
    adoption = (row.get("adoption_level") or "growing").lower()
    adoption_map = {"niche":0.9,"growing":1.0,"established":1.05,"dominant":1.1}
    adoption_prior = adoption_map.get(adoption,1.0)
    risks = len(row.get("risk_flags") or [])
    risk_penalty = min(0.15, 0.03*risks)
    cost_tier = (row.get("cost_tier") or "").lower()
    cost_bonus = 0.05 if "free" in cost_tier else (0.03 if "freemium" in cost_tier else 0.0)
    return fit * sentiment_prior * adoption_prior * (1.0 - risk_penalty) + cost_bonus

def _rank(query, k=5):
    rows = _load_seed()
    scored = [(r, _score(r, query)) for r in rows]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]

def test_image_fallbacks_present():
    rows = [r for r,_ in _rank("image generation photorealistic")]
    names = [r["name"].lower() for r in rows]
    assert any("nano banana" in n for n in names) or any("midjourney" in n for n in names)

def test_code_ranking_prefers_claude_code_or_codestral():
    rows = [r for r,_ in _rank("refactor typescript monorepo code")]
    names = [r["name"].lower() for r in rows]
    assert any("claude code" in n or "codestral" in n for n in names)

def test_rpa_agent_path_suggested():
    rows = [r for r,_ in _rank("place orders on vendor site no api browser automation puppeteer")]
    names = [r["name"].lower() for r in rows]
    assert any("minimax" in n or "n8n" in n or "pipedream" in n for n in names)
