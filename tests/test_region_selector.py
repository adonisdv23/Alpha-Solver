import unittest
from alpha.core import loader, selector

class RegionSelectorTest(unittest.TestCase):
    def test_region_filter_and_synergy(self):
        registries = loader.load_all('registries')
        tools = [
            {"id": "harvey", "router_value": 0.5, "tier": 1},
            {"id": "cn_tool", "router_value": 0.6, "tier": 1, "vendor_id": "cn_state_cloud"},
        ]
        clusters = registries.get('clusters', {})
        ranked = selector.rank_region(tools, region='EU', top_k=5, clusters=clusters)
        ids = [t['id'] for t in ranked]
        self.assertNotIn('cn_tool', ids)
        harvey = next(t for t in ranked if t['id'] == 'harvey')
        self.assertGreater(harvey['reasons']['synergy_bonus'], 0)
        ranked_no_cluster = selector.rank_region(tools, region='EU', top_k=5, clusters={})
        harvey_no = next(t for t in ranked_no_cluster if t['id'] == 'harvey')
        self.assertGreater(harvey['score'], harvey_no['score'])
