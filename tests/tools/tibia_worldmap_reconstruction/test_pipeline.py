import unittest

from tools.tibia_worldmap_reconstruction.pipeline import (
    CATALOG_SCHEMA,
    MAPPING_SCHEMA,
    OBS_SCHEMA,
    REFERENCE_SCHEMA,
    build_otbm_plan,
    compare,
    reconstruct,
)


class ReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.catalog = {
            "schema": CATALOG_SCHEMA,
            "appearances": [
                {"client_id": 100, "roles": ["ground"]},
                {"client_id": 200, "roles": ["border", "static"]},
                {"client_id": 300, "roles": ["static"]},
                {"client_id": 900, "roles": ["creature", "dynamic"]},
            ],
        }
        self.mapping = {
            "schema": MAPPING_SCHEMA,
            "mappings": [
                {"client_id": 100, "otb_id": 1100},
                {"client_id": 200, "otb_id": 1200},
                {"client_id": 300, "otb_id": 1300},
            ],
        }

    def observations(self, contents):
        return {
            "schema": OBS_SCHEMA,
            "observations": [
                {"position": {"x": 32000, "y": 32001, "z": 7}, "contents": contents},
                {"position": {"x": 32000, "y": 32001, "z": 7}, "contents": contents},
            ],
        }

    def test_full_pipeline_match(self):
        snapshot = reconstruct(self.observations([100, 200, 300, 900]), self.catalog, self.mapping)
        tile = snapshot["tiles"][0]
        self.assertEqual("OK", tile["status"])
        self.assertEqual(100, tile["ground_client_id"])
        self.assertEqual(1100, tile["ground_otb_id"])
        self.assertEqual([200, 300], tile["static_client_ids"])
        self.assertEqual([1200, 1300], tile["static_otb_ids"])
        self.assertEqual([900], tile["dynamic_client_ids"])

        reference = {
            "schema": REFERENCE_SCHEMA,
            "tiles": [
                {
                    "position": {"x": 32000, "y": 32001, "z": 7},
                    "ground_otb_id": 1100,
                    "static_otb_ids": [1200, 1300],
                }
            ],
        }
        diff = compare(snapshot, reference)
        self.assertEqual("MATCH", diff["diffs"][0]["status"])
        plan = build_otbm_plan(snapshot)
        self.assertTrue(plan["exportable"])
        self.assertEqual(1, len(plan["tiles"]))

    def test_conflicting_observations_block_export(self):
        doc = {
            "schema": OBS_SCHEMA,
            "observations": [
                {"position": {"x": 1, "y": 2, "z": 7}, "contents": [100, 200]},
                {"position": {"x": 1, "y": 2, "z": 7}, "contents": [100, 300]},
            ],
        }
        snapshot = reconstruct(doc, self.catalog, self.mapping)
        self.assertEqual("CONFLICT", snapshot["tiles"][0]["status"])
        self.assertFalse(build_otbm_plan(snapshot)["exportable"])

    def test_missing_ground_blocks_export(self):
        snapshot = reconstruct(self.observations([200, 300]), self.catalog, self.mapping)
        self.assertEqual("GROUND_UNRESOLVED", snapshot["tiles"][0]["status"])
        self.assertFalse(build_otbm_plan(snapshot)["exportable"])

    def test_unmapped_id_blocks_export(self):
        mapping = {"schema": MAPPING_SCHEMA, "mappings": [{"client_id": 100, "otb_id": 1100}]}
        snapshot = reconstruct(self.observations([100, 200]), self.catalog, mapping)
        self.assertEqual("UNMAPPED_ID", snapshot["tiles"][0]["status"])
        self.assertEqual([200], snapshot["tiles"][0]["unmapped_client_ids"])
        self.assertFalse(build_otbm_plan(snapshot)["exportable"])

    def test_stack_order_mismatch_is_distinct(self):
        snapshot = reconstruct(self.observations([100, 200, 300]), self.catalog, self.mapping)
        reference = {
            "schema": REFERENCE_SCHEMA,
            "tiles": [
                {
                    "position": {"x": 32000, "y": 32001, "z": 7},
                    "ground_otb_id": 1100,
                    "static_otb_ids": [1300, 1200],
                }
            ],
        }
        self.assertEqual("STACK_ORDER_MISMATCH", compare(snapshot, reference)["diffs"][0]["status"])

    def test_unknown_role_blocks_export(self):
        snapshot = reconstruct(self.observations([100, 777]), self.catalog, self.mapping)
        self.assertEqual("UNKNOWN_ROLE", snapshot["tiles"][0]["status"])
        self.assertFalse(build_otbm_plan(snapshot)["exportable"])


if __name__ == "__main__":
    unittest.main()
