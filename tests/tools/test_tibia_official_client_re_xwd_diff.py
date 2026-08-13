import importlib.util
import pathlib
import struct
import unittest


SCRIPT = pathlib.Path(__file__).parents[2] / ".github" / "scripts" / "tibia-official-client-re-xwd-diff.py"
SPEC = importlib.util.spec_from_file_location("xwd_diff", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def xwd(pixels: bytes) -> bytes:
    width, height, pixel_bytes = 2, 2, 4
    fields = [100, 7, 2, 24, width, height, 0, 0, 32, 0, 32, 32, width * pixel_bytes, 4, 0, 0, 0, 8, 256, 0, width, height, 0, 0, 0]
    return struct.pack(">25I", *fields) + pixels


class XwdDiffTests(unittest.TestCase):
    def test_counts_changed_pixels_not_bytes(self):
        before = xwd(b"\0\0\0\0" * 4)
        after = xwd(b"\1\2\3\4" + b"\0\0\0\0" * 3)
        self.assertEqual(MODULE.changed_pixels(before, after), 1)

    def test_rejects_geometry_mismatch(self):
        with self.assertRaises(ValueError):
            MODULE.changed_pixels(xwd(b"\0" * 16), b"short")
