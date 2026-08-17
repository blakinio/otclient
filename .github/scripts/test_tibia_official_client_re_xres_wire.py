#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import struct
import sys
import unittest

WIRE_SCRIPT = Path(__file__).with_name("tibia-official-client-re-xres-wire.py")
SPEC = importlib.util.spec_from_file_location("track_a_xres_wire", WIRE_SCRIPT)
assert SPEC and SPEC.loader
wire = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = wire
SPEC.loader.exec_module(wire)

MAJOR_OPCODE = 150
RESOURCE_XID = 0x00C00011
RESOURCE_CLIENT_BASE = 0x00C00000
PID = 4242
PHYSICAL_V2_PID = 13648
SEQUENCE = 0x1234
PHYSICAL_V2_REPLY = bytes.fromhex(
    "0100030004000000010000000000000000000000000000000000000000000000"
    "0000c000020000000400000050350000"
)


def version_reply(
    byte_order: str = "little",
    *,
    response_type: int = 1,
    sequence: int = SEQUENCE,
    length_words: int = 0,
    major: int = 1,
    minor: int = 2,
) -> bytes:
    prefix = "<" if byte_order == "little" else ">"
    return struct.pack(
        prefix + "BBHIHH20s",
        response_type,
        0,
        sequence,
        length_words,
        major,
        minor,
        b"\0" * 20,
    )


def client_ids_reply(
    records: list[tuple[int, int, tuple[int, ...]]],
    byte_order: str = "little",
    *,
    response_type: int = 1,
    sequence: int = SEQUENCE,
    declared_words: int | None = None,
    declared_num_ids: int | None = None,
) -> bytes:
    prefix = "<" if byte_order == "little" else ">"
    payload = b"".join(
        struct.pack(prefix + "III", client, mask, len(values) * 4)
        + (struct.pack(prefix + f"{len(values)}I", *values) if values else b"")
        for client, mask, values in records
    )
    length_words = len(payload) // 4 if declared_words is None else declared_words
    num_ids = len(records) if declared_num_ids is None else declared_num_ids
    return struct.pack(
        prefix + "BBHII20s",
        response_type,
        0,
        sequence,
        length_words,
        num_ids,
        b"\0" * 20,
    ) + payload


class XResQueryVersionTests(unittest.TestCase):
    def test_encode_little_endian_exact_fixture(self) -> None:
        self.assertEqual(
            wire.encode_query_version(MAJOR_OPCODE, "little"),
            bytes.fromhex("96 00 02 00 01 02 00 00"),
        )

    def test_encode_big_endian_exact_fixture(self) -> None:
        self.assertEqual(
            wire.encode_query_version(MAJOR_OPCODE, "big"),
            bytes.fromhex("96 00 00 02 01 02 00 00"),
        )

    def test_rejects_non_extension_opcode(self) -> None:
        with self.assertRaises(wire.XResWireError):
            wire.encode_query_version(127, "little")

    def test_rejects_unknown_byte_order(self) -> None:
        with self.assertRaises(wire.XResWireError):
            wire.encode_query_version(MAJOR_OPCODE, "native")

    def test_parse_little_endian_reply(self) -> None:
        reply = wire.parse_query_version_reply(
            version_reply(),
            "little",
            expected_sequence=SEQUENCE,
        )
        self.assertEqual(reply.sequence, SEQUENCE)
        self.assertEqual((reply.server_major, reply.server_minor), (1, 2))
        wire.require_xres_1_2(reply)

    def test_parse_big_endian_reply(self) -> None:
        reply = wire.parse_query_version_reply(
            version_reply("big"),
            "big",
            expected_sequence=SEQUENCE,
        )
        self.assertEqual((reply.server_major, reply.server_minor), (1, 2))

    def test_rejects_truncated_reply(self) -> None:
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_version_reply(version_reply()[:-1], "little")

    def test_rejects_non_reply_response(self) -> None:
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_version_reply(version_reply(response_type=0), "little")

    def test_rejects_unexpected_declared_payload(self) -> None:
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_version_reply(version_reply(length_words=1), "little")

    def test_rejects_sequence_mismatch(self) -> None:
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_version_reply(
                version_reply(),
                "little",
                expected_sequence=SEQUENCE + 1,
            )

    def test_rejects_server_version_below_1_2(self) -> None:
        reply = wire.parse_query_version_reply(version_reply(major=1, minor=1), "little")
        with self.assertRaises(wire.XResWireError):
            wire.require_xres_1_2(reply)


class XResQueryClientIdsTests(unittest.TestCase):
    def test_encode_little_endian_exact_fixture(self) -> None:
        self.assertEqual(
            wire.encode_query_client_ids(MAJOR_OPCODE, RESOURCE_XID, "little"),
            bytes.fromhex(
                "96 04 04 00 01 00 00 00 11 00 c0 00 02 00 00 00"
            ),
        )

    def test_encode_big_endian_exact_fixture(self) -> None:
        self.assertEqual(
            wire.encode_query_client_ids(MAJOR_OPCODE, RESOURCE_XID, "big"),
            bytes.fromhex(
                "96 04 00 04 00 00 00 01 00 c0 00 11 00 00 00 02"
            ),
        )

    def test_rejects_zero_resource_xid(self) -> None:
        with self.assertRaises(wire.XResWireError):
            wire.encode_query_client_ids(MAJOR_OPCODE, 0, "little")

    def test_local_pid_wire_length_is_four_bytes(self) -> None:
        data = client_ids_reply(
            [(RESOURCE_XID, wire.XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID, (PID,))]
        )
        self.assertEqual(struct.unpack_from("<I", data, 40)[0], 4)
        self.assertEqual(len(data), 48)

    def test_parse_and_extract_single_local_pid(self) -> None:
        data = client_ids_reply(
            [(RESOURCE_XID, wire.XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID, (PID,))]
        )
        records = wire.parse_query_client_ids_reply(
            data,
            "little",
            expected_sequence=SEQUENCE,
        )
        self.assertEqual(
            records,
            (
                wire.ClientIdValue(
                    RESOURCE_XID,
                    wire.XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID,
                    (PID,),
                ),
            ),
        )
        self.assertEqual(wire.extract_local_client_pid(records, RESOURCE_XID), PID)

    def test_parse_big_endian_single_local_pid(self) -> None:
        data = client_ids_reply(
            [(RESOURCE_XID, wire.XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID, (PID,))],
            "big",
        )
        records = wire.parse_query_client_ids_reply(
            data,
            "big",
            expected_sequence=SEQUENCE,
        )
        self.assertEqual(wire.extract_local_client_pid(records, RESOURCE_XID), PID)

    def test_accepts_returned_owner_client_base_for_requested_resource(self) -> None:
        records = (
            wire.ClientIdValue(
                RESOURCE_CLIENT_BASE,
                wire.XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID,
                (PID,),
            ),
        )
        self.assertEqual(wire.extract_local_client_pid(records, RESOURCE_XID), PID)

    def test_accepts_retained_physical_v2_reply_client_base(self) -> None:
        records = wire.parse_query_client_ids_reply(
            PHYSICAL_V2_REPLY,
            "little",
            expected_sequence=3,
        )
        self.assertEqual(
            records,
            (
                wire.ClientIdValue(
                    RESOURCE_CLIENT_BASE,
                    wire.XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID,
                    (PHYSICAL_V2_PID,),
                ),
            ),
        )
        self.assertEqual(
            wire.extract_local_client_pid(records, RESOURCE_XID),
            PHYSICAL_V2_PID,
        )

    def test_zero_id_reply_is_unresolved_not_fabricated(self) -> None:
        records = wire.parse_query_client_ids_reply(client_ids_reply([]), "little")
        self.assertEqual(records, ())
        self.assertIsNone(wire.extract_local_client_pid(records, RESOURCE_XID))

    def test_rejects_truncated_fixed_reply(self) -> None:
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_client_ids_reply(client_ids_reply([])[:-1], "little")

    def test_rejects_non_reply_response(self) -> None:
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_client_ids_reply(
                client_ids_reply([], response_type=0),
                "little",
            )

    def test_rejects_declared_length_mismatch(self) -> None:
        data = client_ids_reply(
            [(RESOURCE_XID, 2, (PID,))],
            declared_words=3,
        )
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_client_ids_reply(data, "little")

    def test_rejects_declared_id_count_without_record(self) -> None:
        data = client_ids_reply([], declared_num_ids=1)
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_client_ids_reply(data, "little")

    def test_rejects_value_payload_truncation(self) -> None:
        data = client_ids_reply([(RESOURCE_XID, 2, (PID,))])
        shortened = data[:-4]
        fixed = bytearray(shortened)
        struct.pack_into("<I", fixed, 4, (len(shortened) - 32) // 4)
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_client_ids_reply(bytes(fixed), "little")

    def test_rejects_non_card32_aligned_value_byte_length(self) -> None:
        data = bytearray(client_ids_reply([(RESOURCE_XID, 2, (PID,))]))
        struct.pack_into("<I", data, 40, 3)
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_client_ids_reply(bytes(data), "little")

    def test_rejects_unparsed_trailing_payload(self) -> None:
        data = client_ids_reply([], declared_words=1) + b"\0\0\0\0"
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_client_ids_reply(data, "little")

    def test_rejects_reply_over_size_cap(self) -> None:
        data = client_ids_reply(
            [(RESOURCE_XID, 2, tuple(range(20)))],
        )
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_client_ids_reply(data, "little", max_reply_bytes=64)

    def test_rejects_id_count_over_cap(self) -> None:
        records = [(RESOURCE_XID + i, 2, (PID + i,)) for i in range(2)]
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_client_ids_reply(
                client_ids_reply(records),
                "little",
                max_ids=1,
            )

    def test_rejects_value_count_over_cap(self) -> None:
        data = client_ids_reply([(RESOURCE_XID, 2, (1, 2))])
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_client_ids_reply(
                data,
                "little",
                max_values_per_id=1,
            )

    def test_rejects_sequence_mismatch(self) -> None:
        with self.assertRaises(wire.XResWireError):
            wire.parse_query_client_ids_reply(
                client_ids_reply([]),
                "little",
                expected_sequence=SEQUENCE + 1,
            )

    def test_rejects_target_record_wrong_mask(self) -> None:
        records = (wire.ClientIdValue(RESOURCE_XID, 1, (PID,)),)
        with self.assertRaises(wire.XResWireError):
            wire.extract_local_client_pid(records, RESOURCE_XID)

    def test_rejects_target_record_wrong_value_shape(self) -> None:
        records = (wire.ClientIdValue(RESOURCE_XID, 2, (PID, PID + 1)),)
        with self.assertRaises(wire.XResWireError):
            wire.extract_local_client_pid(records, RESOURCE_XID)

    def test_rejects_zero_pid(self) -> None:
        records = (wire.ClientIdValue(RESOURCE_XID, 2, (0,)),)
        with self.assertRaises(wire.XResWireError):
            wire.extract_local_client_pid(records, RESOURCE_XID)

    def test_rejects_duplicate_target_records(self) -> None:
        records = (
            wire.ClientIdValue(RESOURCE_XID, 2, (PID,)),
            wire.ClientIdValue(RESOURCE_XID, 2, (PID,)),
        )
        with self.assertRaises(wire.XResWireError):
            wire.extract_local_client_pid(records, RESOURCE_XID)

    def test_rejects_extra_non_target_record_even_with_target(self) -> None:
        records = (
            wire.ClientIdValue(RESOURCE_XID, 2, (PID,)),
            wire.ClientIdValue(RESOURCE_XID + 1, 2, (PID + 1,)),
        )
        with self.assertRaises(wire.XResWireError):
            wire.extract_local_client_pid(records, RESOURCE_XID)

    def test_rejects_zero_returned_client_identifier(self) -> None:
        records = (
            wire.ClientIdValue(0, wire.XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID, (PID,)),
        )
        with self.assertRaises(wire.XResWireError):
            wire.extract_local_client_pid(records, RESOURCE_XID)


if __name__ == "__main__":
    unittest.main(verbosity=2)
