from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).parents[2] / ".github" / "scripts" / "tibia-official-client-re-reconstruct.py"
os.environ.setdefault("TIBIA_PACKAGE_OUT", str(Path(tempfile.gettempdir()) / "track-a-test-runtime"))
SPEC = importlib.util.spec_from_file_location("track_a_reconstruct", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReconstructTests(unittest.TestCase):
    def test_safe_path_accepts_relative_manifest_path(self) -> None:
        self.assertEqual(str(MODULE.safe_path("assets/subarea-1.bmp.lzma")), "assets/subarea-1.bmp.lzma")

    def test_safe_path_rejects_escape_and_absolute_path(self) -> None:
        for value in ("../secret", "/absolute", "a/../../secret", ""):
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                MODULE.safe_path(value)

    def test_missing_unpacked_hash_is_preserved_only_for_assets(self) -> None:
        packed = b"packed"
        self.assertEqual(MODULE.decode(packed, "asset.lzma", None, True), (packed, "asset.lzma"))
        with self.assertRaises(RuntimeError):
            MODULE.decode(packed, "package.lzma", None, False)

    def test_identity_transform_requires_exact_hash(self) -> None:
        data = b"plain"
        self.assertEqual(MODULE.decode(data, "bin/plain", MODULE.sha256(data), False), (data, "bin/plain"))


if __name__ == "__main__":
    unittest.main()
