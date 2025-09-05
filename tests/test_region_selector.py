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
        self.assertGreater(harvey['synergy_bonus'], 0)
        self.assertNotEqual(harvey['score_base'] + harvey['synergy_bonus'], harvey['final_score'])
        self.assertEqual(harvey['final_score'], harvey['score'])
        self.assertIn('region_filter', harvey['reasons'])
        self.assertIn('synergy_notes', harvey['reasons'])
        self.assertIn('ties', harvey['reasons'])
        self.assertGreaterEqual(harvey['confidence'], 0.0)
        self.assertLessEqual(harvey['confidence'], 1.0)
        ranked_no_cluster = selector.rank_region(tools, region='EU', top_k=5, clusters={})
        harvey_no = next(t for t in ranked_no_cluster if t['id'] == 'harvey')
        self.assertGreater(harvey['final_score'], harvey_no['final_score'])
