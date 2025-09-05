import csv
from pathlib import Path
from alpha.core import selector, orchestrator


def setup_canon(tmp_path):
    path = Path('artifacts/tools_canon.csv')
    path.parent.mkdir(exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['key','id','vendor_id','router_value','tier','category','popularity','sentiment'])
        writer.writeheader()
        writer.writerow({'key':'t1:','id':'t1','vendor_id':'','router_value':1,'tier':1,'category':'cat','popularity':0.5,'sentiment':0.2})
    return path


def test_enrichment_and_bonus(tmp_path):
    setup_canon(tmp_path)
    tools = [{"id": "t1", "router_value": 0.5}]
    shortlist = selector.rank_region(tools, region="US", top_k=1)
    item = shortlist[0]
    assert item["enrichment"]["category"] == "cat"
    assert item["reasons"]["popularity_bonus"] <= 0.1
    plan = orchestrator.build_plan("q", "US", 1, shortlist, None, seed=123)
    assert plan.steps[0].enrichment.get("category") == "cat"
