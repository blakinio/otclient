from pathlib import Path
import unittest

from tools.tibia_re_surveyor.coverage import CoverageParseError, expand_cell, parse_critical_dependencies, parse_matrix, rank_next, status_counts

ROOT = Path(__file__).resolve().parents[3]
MATRIX = ROOT / "docs/agents/reports/OTCLIENT-20260818-full-client-re-matrix.md"
CHECKLIST = ROOT / "docs/agents/reports/OTCLIENT-20260818-full-client-re-100-percent-checklist.md"


class CoverageTests(unittest.TestCase):
    def test_range_expansion(self):
        self.assertEqual(["A10", "A11", "A12", "A13"], expand_cell("`A10–A13`"))
        self.assertEqual([], expand_cell("—"))

    def test_real_canonical_matrix_is_complete(self):
        rows = parse_matrix(MATRIX.read_text(encoding="utf-8"), CHECKLIST.read_text(encoding="utf-8"))
        self.assertEqual(169, len(rows))
        self.assertEqual({"DONE": 14, "PARTIAL": 95, "NOT_STARTED": 56, "BLOCKED": 4}, status_counts(rows))
        by_id = {row.row_id: row for row in rows}
        self.assertEqual("BLOCKED", by_id["A15"].status)
        self.assertEqual("Authoritative local-player XYZ", by_id["C10"].title)

    def test_critical_dependencies_and_ranking_are_canonical_only(self):
        text = MATRIX.read_text(encoding="utf-8")
        rows = parse_matrix(text, CHECKLIST.read_text(encoding="utf-8"))
        ranked = rank_next(rows, parse_critical_dependencies(text), limit=4)
        self.assertEqual(["A15", "C10", "F08", "F10"], [item["row_id"] for item in ranked])
        self.assertTrue(all(item["canonical_dependencies"] for item in ranked))

    def test_incomplete_matrix_fails_closed(self):
        with self.assertRaises(CoverageParseError):
            parse_matrix("| **A** | `A01` | — | — | — |")


if __name__ == "__main__":
    unittest.main()
