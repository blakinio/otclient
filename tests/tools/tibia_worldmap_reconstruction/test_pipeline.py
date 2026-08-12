import unittest

from tools.tibia_worldmap_reconstruction.pipeline import (
    CATALOG_SCHEMA,
    MAPPING_SCHEMA,
    OBS_SCHEMA,
    REFERENCE_SCHEMA,
    ReconstructionError,
    SNAPSHOT_SCHEMA,
    build_otbm_plan,
    compare,
    reconstruct,
)


CLIENT_VERSION = "15.32.df7b29"
OTB_VERSION = "test-otb-v1"


class ReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.catalog = {
            "schema": CATALOG_SCHEMA,
            "client_version": CLIENT_VERSION,
            "appearances": [
                {"client_id": 100, "roles": ["ground"], "evidence": "synthetic ground fixture"},
                {"client_id": 200, "roles": ["border", "static"], "evidence": "synthetic border fixture"},
                {"client_id": 300, "roles": ["static"], "evidence": "synthetic static fixture"},
                {"client_id": 900, "roles": ["creature", "dynamic"], "evidence": "synthetic creature fixture"},
            ],
        }
        self.mapping = {
            "schema": MAPPING_SCHEMA,
            "client_version": CLIENT_VERSION,
            "otb_version": OTB_VERSION,
            "mappings": [
                {"client_id": 100, "otb_id": 1100, "evidence": "synthetic mapping"},
                {"client_id": 200, "otb_id": 1200, "evidence": "synthetic mapping"},
                {"client_id": 300, "otb_id": 1300, "evidence": "synthetic mapping"},
            ],
        }

    def observations(self, contents):
        record = {
            "position": {"x": 32000, "y": 32001, "z": 7},
            "contents": contents,
            "provenance": {"source": "synthetic-test", "capture_id": "capture-1"},
        }
        return {
            "schema": OBS_SCHEMA,
            "client_version": CLIENT_VERSION,
            "observations": [record, dict(record)],
        }

    def reference(self, items=(1200, 1300)):
        return {
            "schema": REFERENCE_SCHEMA,
            "source": "synthetic-reference",
            "otb_version": OTB_VERSION,
            "tiles": [
                {
                    "position": {"x": 32000, "y": 32001, "z": 7},
                    "ground_otb_id": 1100,
                    "static_otb_ids": list(items),
                }
            ],
        }

    def test_full_pipeline_match(self):
        snapshot = reconstruct(self.observations([100, 200, 300, 900]), self.catalog, self.mapping)
        tile = snapshot["tiles"][0]
        self.assertEqual("OK", tile["status"])
        self.assertEqual(CLIENT_VERSION, snapshot["client_version"])
        self.assertEqual(OTB_VERSION, snapshot["otb_version"])
        self.assertEqual(100, tile["ground_client_id"])
        self.assertEqual(1100, tile["ground_otb_id"])
        self.assertEqual([200, 300], tile["static_client_ids"])
        self.assertEqual([1200, 1300], tile["static_otb_ids"])
        self.assertEqual([900], tile["dynamic_client_ids"])

        diff = compare(snapshot, self.reference())
        self.assertEqual("MATCH", diff["diffs"][0]["status"])
        plan = build_otbm_plan(snapshot)
        self.assertTrue(plan["exportable"])
        self.assertEqual(1, len(plan["tiles"]))

    def test_conflicting_observations_block_export(self):
        doc = self.observations([100, 200])
        doc["observations"][1] = {
            "position": {"x": 32000, "y": 32001, "z": 7},
            "contents": [100, 300],
            "provenance": {"source": "synthetic-test", "capture_id": "capture-2"},
        }
        snapshot = reconstruct(doc, self.catalog, self.mapping)
        self.assertEqual("CONFLICT", snapshot["tiles"][0]["status"])
        self.assertFalse(build_otbm_plan(snapshot)["exportable"])

    def test_missing_ground_blocks_export(self):
        snapshot = reconstruct(self.observations([200, 300]), self.catalog, self.mapping)
        self.assertEqual("GROUND_UNRESOLVED", snapshot["tiles"][0]["status"])
        self.assertFalse(build_otbm_plan(snapshot)["exportable"])

    def test_unmapped_id_blocks_export(self):
        mapping = {
            "schema": MAPPING_SCHEMA,
            "client_version": CLIENT_VERSION,
            "otb_version": OTB_VERSION,
            "mappings": [{"client_id": 100, "otb_id": 1100, "evidence": "synthetic mapping"}],
        }
        snapshot = reconstruct(self.observations([100, 200]), self.catalog, mapping)
        self.assertEqual("UNMAPPED_ID", snapshot["tiles"][0]["status"])
        self.assertEqual([200], snapshot["tiles"][0]["unmapped_client_ids"])
        self.assertFalse(build_otbm_plan(snapshot)["exportable"])

    def test_stack_order_mismatch_is_distinct(self):
        snapshot = reconstruct(self.observations([100, 200, 300]), self.catalog, self.mapping)
        self.assertEqual(
            "STACK_ORDER_MISMATCH",
            compare(snapshot, self.reference(items=(1300, 1200)))["diffs"][0]["status"],
        )

    def test_unknown_role_is_not_reported_as_match(self):
        snapshot = reconstruct(self.observations([100, 777]), self.catalog, self.mapping)
        self.assertEqual("UNKNOWN_ROLE", snapshot["tiles"][0]["status"])
        diff = compare(
            snapshot,
            {
                "schema": REFERENCE_SCHEMA,
                "source": "synthetic-reference",
                "otb_version": OTB_VERSION,
                "tiles": [
                    {
                        "position": {"x": 32000, "y": 32001, "z": 7},
                        "ground_otb_id": 1100,
                        "static_otb_ids": [],
                    }
                ],
            },
        )
        self.assertEqual("UNKNOWN_ROLE", diff["diffs"][0]["status"])
        self.assertFalse(build_otbm_plan(snapshot)["exportable"])

    def test_client_version_mismatch_fails_closed(self):
        observations = self.observations([100])
        observations["client_version"] = "different"
        with self.assertRaises(ReconstructionError):
            reconstruct(observations, self.catalog, self.mapping)

    def test_missing_provenance_fails_closed(self):
        observations = self.observations([100])
        del observations["observations"][0]["provenance"]
        with self.assertRaises(ReconstructionError):
            reconstruct(observations, self.catalog, self.mapping)

    def test_conflicting_mapping_fails_closed(self):
        mapping = dict(self.mapping)
        mapping["mappings"] = list(self.mapping["mappings"]) + [
            {"client_id": 100, "otb_id": 9999, "evidence": "conflicting synthetic mapping"}
        ]
        with self.assertRaises(ReconstructionError):
            reconstruct(self.observations([100]), self.catalog, mapping)

    def test_conflicting_role_combination_fails_closed(self):
        catalog = dict(self.catalog)
        catalog["appearances"] = list(self.catalog["appearances"]) + [
            {"client_id": 999, "roles": ["ground", "creature"], "evidence": "bad synthetic evidence"}
        ]
        with self.assertRaises(ReconstructionError):
            reconstruct(self.observations([100]), catalog, self.mapping)

    def test_reference_otb_version_mismatch_fails_closed(self):
        snapshot = reconstruct(self.observations([100, 200, 300]), self.catalog, self.mapping)
        reference = self.reference()
        reference["otb_version"] = "other"
        with self.assertRaises(ReconstructionError):
            compare(snapshot, reference)

    def test_empty_snapshot_is_not_exportable(self):
        snapshot = {
            "schema": SNAPSHOT_SCHEMA,
            "client_version": CLIENT_VERSION,
            "otb_version": OTB_VERSION,
            "tiles": [],
        }
        plan = build_otbm_plan(snapshot)
        self.assertFalse(plan["exportable"])
        self.assertEqual("NO_TILES", plan["blockers"][0]["reason"])


if __name__ == "__main__":
    unittest.main()
