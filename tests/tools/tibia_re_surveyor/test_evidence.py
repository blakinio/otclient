from pathlib import Path
import tempfile
import unittest

from tools.tibia_re_surveyor.evidence import LocalRepoReader


class EvidenceIndexTests(unittest.TestCase):
    def test_mentions_are_indexed_without_status_promotion(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            evidence = root / "docs/agents/evidence/example"
            evidence.mkdir(parents=True)
            sha = "a" * 64
            (evidence / "result.md").write_text(f"D09 evidence on {sha}; C10 remains UNKNOWN", encoding="utf-8")
            (evidence / "other.json").write_text('{"row":"D09"}', encoding="utf-8")
            index = LocalRepoReader(root).scan_evidence_mentions(["D09", "C10", "F08"], sha)
            self.assertEqual(2, index["D09"]["mention_count"])
            self.assertEqual(1, index["D09"]["current_sha_match_count"])
            self.assertEqual(1, index["C10"]["mention_count"])
            self.assertEqual(0, index["F08"]["mention_count"])

    def test_list_paths_is_sorted_bounded_and_rejects_escape(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            profiles = root / "profiles"
            profiles.mkdir()
            (profiles / "b.json").write_text("{}", encoding="utf-8")
            (profiles / "a.json").write_text("{}", encoding="utf-8")
            (profiles / "ignore.txt").write_text("x", encoding="utf-8")
            reader = LocalRepoReader(root)
            self.assertEqual(["profiles/a.json", "profiles/b.json"], reader.list_paths("profiles", ".json"))
            with self.assertRaises(Exception):
                reader.list_paths("../outside", ".json")

    def test_large_evidence_file_is_not_scanned(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            evidence = root / "docs/agents/evidence/example"
            evidence.mkdir(parents=True)
            (evidence / "large.txt").write_text("D09" + "x" * 1_000_001, encoding="utf-8")
            index = LocalRepoReader(root).scan_evidence_mentions(["D09"], "a" * 64)
            self.assertEqual(0, index["D09"]["mention_count"])


if __name__ == "__main__":
    unittest.main()
