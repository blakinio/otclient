#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

SCRIPT = Path(__file__).with_name("tibia-official-client-re-xres-window-owner.py")
WIRE = Path(__file__).with_name("tibia-official-client-re-xres-wire.py")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


owner = load(SCRIPT, "track_a_xres_window_owner_test")
wire = load(WIRE, "track_a_xres_wire_for_owner_test")

RESOURCE_XID = 0x00C00011
CLIENT_BASE = 0x00C00000
PHYSICAL_PID = 13648


class Tests(unittest.TestCase):
    def test_retained_457_client_base_fixture_resolves_pid(self) -> None:
        records = (
            wire.ClientIdValue(
                CLIENT_BASE,
                wire.XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID,
                (PHYSICAL_PID,),
            ),
        )
        self.assertEqual(
            owner.extract_one_spec_local_pid(
                records, wire.XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID
            ),
            PHYSICAL_PID,
        )

    def test_client_field_need_not_echo_queried_resource_xid(self) -> None:
        self.assertNotEqual(CLIENT_BASE, RESOURCE_XID)
        records = (
            wire.ClientIdValue(
                CLIENT_BASE,
                wire.XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID,
                (PHYSICAL_PID,),
            ),
        )
        self.assertEqual(owner.extract_one_spec_local_pid(records, 2), PHYSICAL_PID)

    def test_rejects_zero_returned_client_identifier(self) -> None:
        records = (wire.ClientIdValue(0, 2, (PHYSICAL_PID,)),)
        with self.assertRaises(owner.WindowOwnerError):
            owner.extract_one_spec_local_pid(records, 2)

    def test_rejects_multiple_one_spec_records(self) -> None:
        records = (
            wire.ClientIdValue(CLIENT_BASE, 2, (PHYSICAL_PID,)),
            wire.ClientIdValue(CLIENT_BASE + 0x200000, 2, (9999,)),
        )
        with self.assertRaises(owner.WindowOwnerError):
            owner.extract_one_spec_local_pid(records, 2)

    def test_rejects_wrong_mask_or_value_shape(self) -> None:
        with self.assertRaises(owner.WindowOwnerError):
            owner.extract_one_spec_local_pid(
                (wire.ClientIdValue(CLIENT_BASE, 1, (PHYSICAL_PID,)),), 2
            )
        with self.assertRaises(owner.WindowOwnerError):
            owner.extract_one_spec_local_pid(
                (wire.ClientIdValue(CLIENT_BASE, 2, (PHYSICAL_PID, 1)),), 2
            )

    def test_unique_expected_pid_candidate_is_selected(self) -> None:
        candidates = (
            owner.WindowCandidate(RESOURCE_XID, 1920, 1080),
            owner.WindowCandidate(0x01000011, 1920, 1080),
        )
        pids = {RESOURCE_XID: PHYSICAL_PID, 0x01000011: 9999}
        self.assertEqual(
            owner.select_owned_xid(candidates, PHYSICAL_PID, pids.get),
            RESOURCE_XID,
        )

    def test_no_match_is_unresolved(self) -> None:
        candidates = (owner.WindowCandidate(RESOURCE_XID, 1920, 1080),)
        self.assertIsNone(
            owner.select_owned_xid(candidates, PHYSICAL_PID, lambda _xid: 9999)
        )

    def test_multiple_owned_candidates_fail_closed(self) -> None:
        candidates = (
            owner.WindowCandidate(RESOURCE_XID, 1920, 1080),
            owner.WindowCandidate(RESOURCE_XID + 1, 1920, 1080),
        )
        with self.assertRaises(owner.WindowOwnerError):
            owner.select_owned_xid(candidates, PHYSICAL_PID, lambda _xid: PHYSICAL_PID)


if __name__ == "__main__":
    unittest.main(verbosity=2)
