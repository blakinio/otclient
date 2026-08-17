#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import struct
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("tibia-official-client-re-p0-runtime-snapshot.py")


def load():
    spec = importlib.util.spec_from_file_location("p0_runtime_snapshot_tested", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


snapshot = load()


class Tests(unittest.TestCase):
    def test_parse_process_start_ticks_handles_spaces_in_comm(self) -> None:
        fields_3_to_22 = [
            "S", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "10", "11", "12", "13", "14", "15", "16", "17", "18", "424242",
        ]
        text = "123 (Tibia Client Worker) " + " ".join(fields_3_to_22) + " 99 100\n"
        self.assertEqual(snapshot.parse_process_start_ticks(text), 424242)

    def test_decode_direct_xyz_is_signed_i32(self) -> None:
        blob = struct.pack("<iii", 32123, 31999, 7)
        self.assertEqual(snapshot.decode_direct_xyz(blob), (32123, 31999, 7))
        negative = struct.pack("<iii", -1, 2, 3)
        self.assertEqual(snapshot.decode_direct_xyz(negative), (-1, 2, 3))

    def test_find_typed_object_and_direct_offsets(self) -> None:
        expected_vptr = 0x1122334455667788
        data = bytearray(0x300)
        object_address = 0x40
        private_data = 0x180
        struct.pack_into("<Q", data, object_address, expected_vptr)
        struct.pack_into("<Q", data, object_address + 8, private_data)
        struct.pack_into("<iii", data, object_address + 0x78, 33001, 32002, 6)

        with tempfile.NamedTemporaryFile() as handle:
            handle.write(data)
            handle.flush()
            fd = os.open(handle.name, os.O_RDONLY)
            try:
                regions = [snapshot.Region(0, len(data), "rw-p", 0, "")]
                hits = snapshot.find_typed_objects(fd, regions, expected_vptr)
                self.assertEqual(hits, [(object_address, private_data)])
                result = snapshot.read_direct_snapshot(fd, object_address, private_data)
            finally:
                os.close(fd)

        self.assertEqual((result.x, result.y, result.z), (33001, 32002, 6))
        self.assertEqual(result.object_address, object_address)
        self.assertEqual(result.private_data_pointer, private_data)

    def test_rejects_vptr_when_private_pointer_is_not_rw(self) -> None:
        expected_vptr = 0x8877665544332211
        data = bytearray(0x200)
        struct.pack_into("<Q", data, 0x40, expected_vptr)
        struct.pack_into("<Q", data, 0x48, 0x999999)
        with tempfile.NamedTemporaryFile() as handle:
            handle.write(data)
            handle.flush()
            fd = os.open(handle.name, os.O_RDONLY)
            try:
                regions = [snapshot.Region(0, len(data), "rw-p", 0, "")]
                self.assertEqual(snapshot.find_typed_objects(fd, regions, expected_vptr), [])
            finally:
                os.close(fd)

    def test_payload_is_explicitly_nonsemantic_and_read_only(self) -> None:
        typed = snapshot.TypedSnapshot(0x1000, 0x2000, 1, 2, 3)
        payload = snapshot.build_payload(
            label="before",
            pid=123,
            start_ticks=456,
            boot_hash="a" * 64,
            client=Path("/tmp/client"),
            client_sha256="b" * 64,
            client_size=51965216,
            main_image_base=0x400000,
            expected_vptr=0x348CA70,
            snapshots=[typed],
            wall_time_ns=1,
            monotonic_ns=2,
        )
        self.assertEqual(payload["process_memory_access"], "read_only")
        self.assertEqual(payload["process_memory_writes"], 0)
        self.assertFalse(payload["semantic_player_xyz_proven"])
        self.assertEqual(payload["typed_object_count"], 1)
        self.assertEqual(payload["typed_objects"][0]["offsets"], [0x78, 0x7C, 0x80])

    def test_source_contains_no_process_memory_write_primitives(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("os.pwrite", source)
        self.assertNotIn("O_RDWR", source)
        self.assertNotIn("O_WRONLY", source)
        self.assertIn("os.O_RDONLY | os.O_CLOEXEC", source)
        self.assertIn("process_memory_writes\": 0", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
