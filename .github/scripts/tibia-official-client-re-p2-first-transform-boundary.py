#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

EXPECTED_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
EXPECTED_SIZE = 51965216
WRITER_AP = 0x2F69DD0
WRITER_RTTI = 0x3080728
INTERMEDIATE_AP = 0x2F69E30
INTERMEDIATE_RTTI = 0x3080748
PROCESSOR_AP = 0x2F6A208

DTOR_1 = 0x7DE7F0
DTOR_2 = 0x7DFD60
SERIALIZE_1 = 0xC10960
SERIALIZE_2 = 0xC20290
BUFFER_SLOT = 0xC20C70


def require(value: bool, marker: str) -> None:
    if not value:
        print(f"P2_FIRST_TRANSFORM_FAIL={marker}", file=sys.stderr)
        raise SystemExit(2)
    print(f"P2_FIRST_TRANSFORM_OK={marker}")


class Elf64:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = path.read_bytes()
        require(self.data[:4] == b"\x7fELF", "elf_magic")
        require(self.data[4] == 2, "elf_64bit")
        require(self.data[5] == 1, "elf_little_endian")
        self.phoff = struct.unpack_from("<Q", self.data, 32)[0]
        self.phentsize = struct.unpack_from("<H", self.data, 54)[0]
        self.phnum = struct.unpack_from("<H", self.data, 56)[0]
        self.loads: list[tuple[int, int, int, int]] = []
        for index in range(self.phnum):
            off = self.phoff + index * self.phentsize
            p_type, p_flags, p_offset, p_vaddr, _, p_filesz, p_memsz, _ = struct.unpack_from(
                "<IIQQQQQQ", self.data, off
            )
            if p_type == 1:
                self.loads.append((p_vaddr, p_memsz, p_offset, p_flags))
        require(bool(self.loads), "elf_load_segments")

    def file_offset(self, va: int, size: int = 1) -> int:
        for vaddr, memsz, offset, _flags in self.loads:
            if vaddr <= va and va + size <= vaddr + memsz:
                result = offset + (va - vaddr)
                require(result + size <= len(self.data), f"va_file_backed_{va:x}")
                return result
        raise ValueError(f"unmapped virtual address 0x{va:x}")

    def read(self, va: int, size: int) -> bytes:
        off = self.file_offset(va, size)
        return self.data[off : off + size]

    def u64(self, va: int) -> int:
        return struct.unpack("<Q", self.read(va, 8))[0]

    def executable(self, va: int) -> bool:
        for vaddr, memsz, _offset, flags in self.loads:
            if vaddr <= va < vaddr + memsz:
                return bool(flags & 1)
        return False


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_bytes(elf: Elf64, va: int, expected_hex: str, marker: str) -> None:
    expected = bytes.fromhex(expected_hex)
    require(elf.read(va, len(expected)) == expected, marker)


def disassemble(objdump: Path, client: Path, lo: int, hi: int) -> str:
    cmd = [
        str(objdump),
        "-d",
        "-Mintel",
        "--no-show-raw-insn",
        f"--start-address=0x{lo:x}",
        f"--stop-address=0x{hi:x}",
        str(client),
    ]
    result = subprocess.run(cmd, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout


def selected_lines(text: str, needles: tuple[str, ...]) -> list[str]:
    out: list[str] = []
    for line in text.splitlines():
        if any(needle in line for needle in needles):
            cleaned = re.sub(r"^\s+", "", line)
            out.append(cleaned)
    return out


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--client", type=Path, required=True)
    p.add_argument("--objdump", type=Path, required=True)
    p.add_argument("--output-json", type=Path, required=True)
    p.add_argument("--output-text", type=Path, required=True)
    p.add_argument("--evidence", type=Path, required=True)
    return p.parse_args()


def main() -> int:
    ns = parse_args()
    require(ns.client.is_file(), "client_present")
    require(ns.objdump.is_file(), "objdump_present")
    require(ns.client.stat().st_size == EXPECTED_SIZE, "exact_client_size")
    digest = sha256(ns.client)
    require(digest == EXPECTED_SHA256, "exact_client_sha256")

    elf = Elf64(ns.client)

    # Revalidate canonical writer identity and the distinct adjacent intermediate table.
    require(elf.u64(WRITER_AP - 16) == 0, "writer_offset_to_top_zero")
    require(elf.u64(WRITER_AP - 8) == WRITER_RTTI, "writer_rtti_3080728")
    require(elf.u64(WRITER_AP + 0x50) == 0, "adjacent_intermediate_offset_to_top_zero")
    require(elf.u64(WRITER_AP + 0x58) == INTERMEDIATE_RTTI, "adjacent_intermediate_rtti_3080748")
    require(WRITER_AP + 0x60 == INTERMEDIATE_AP, "intermediate_address_point_derived")
    require(elf.u64(INTERMEDIATE_AP - 16) == 0, "intermediate_offset_to_top_zero")
    require(elf.u64(INTERMEDIATE_AP - 8) == INTERMEDIATE_RTTI, "intermediate_rtti_revalidated")

    expected_slots = [DTOR_1, DTOR_2, SERIALIZE_1, SERIALIZE_2, BUFFER_SLOT]
    for index, address in enumerate(expected_slots):
        actual = elf.u64(INTERMEDIATE_AP + index * 8)
        require(actual == address, f"intermediate_slot_{index}_0x{address:x}")
        require(elf.executable(actual), f"intermediate_slot_{index}_executable")

    # Revalidate the exact setup provenance instead of inheriting #301/#305 as assumptions.
    # Writer shared object: control block at rbp-0x1f8, object at +0x10, vptr TProtocolWriter.
    assert_bytes(elf, 0x1970D26, "bf28000000", "writer_control_allocation_0x28")
    assert_bytes(elf, 0x1970D37, "48898508feffff", "writer_control_saved_rbp_1f8")
    assert_bytes(elf, 0x1970D63, "488d0d66905f01", "writer_ap_lea_2f69dd0")
    assert_bytes(elf, 0x1970D6D, "48894a10", "writer_vptr_store_control_plus10")

    # Intermediate shared object: object pointer from writer control +0x10 is retained at +0x18.
    assert_bytes(elf, 0x1970EDD, "bf50020000", "intermediate_control_allocation_0x250")
    assert_bytes(elf, 0x1970EFC, "488d7010", "writer_object_pointer_from_control_plus10")
    assert_bytes(elf, 0x1970F31, "488d3df88e5f01", "intermediate_ap_lea_2f69e30")
    assert_bytes(elf, 0x1970F3B, "48897a10", "intermediate_vptr_store_plus10")
    assert_bytes(elf, 0x1970F3F, "48897218", "intermediate_retains_writer_object_plus18")
    assert_bytes(elf, 0x1970F43, "48894a20", "intermediate_retains_writer_control_plus20")

    # TProtocolClientMessageProcessor retains the intermediate object/control pair at +0x18/+0x20.
    assert_bytes(elf, 0x1970F77, "488d4110", "intermediate_object_pointer_materialized")
    assert_bytes(elf, 0x1971056, "488d0dab915f01", "processor_ap_lea_2f6a208")
    assert_bytes(elf, 0x1971068, "48897018", "processor_retains_intermediate_object_plus18")
    assert_bytes(elf, 0x1971076, "48897020", "processor_retains_intermediate_control_plus20")

    # First non-lifecycle intermediate dispatch: source object -> retained writer -> QDataStream byte.
    serial1 = disassemble(ns.objdump, ns.client, SERIALIZE_1, SERIALIZE_1 + 0x110)
    require("QDataStream" in serial1 and "lsEa" in serial1, "slot_0x10_qdatastream_signed_byte")
    require("[rdi+0x18]" in serial1, "slot_0x10_uses_retained_writer_member")
    require("[rax+0x38]" in serial1, "slot_0x10_reads_message_dispatch_value")

    # Next serializer slot demonstrates structured argument fields being streamed as 16-bit values.
    serial2 = disassemble(ns.objdump, ns.client, SERIALIZE_2, SERIALIZE_2 + 0x180)
    require("QDataStream" in serial2 and "lsEs" in serial2, "slot_0x18_qdatastream_signed_short")
    require("[rsi+0x30]" in serial2, "slot_0x18_reads_argument_field_30")
    require("[rsi+0x34]" in serial2, "slot_0x18_reads_argument_field_34")
    require("[rdi+0x18]" in serial2, "slot_0x18_uses_retained_writer_member")

    # Adjacent concrete byte-buffer construction exists, but ordering relative to the serializer calls
    # is not inferred from vtable adjacency.
    buffer_dis = disassemble(ns.objdump, ns.client, BUFFER_SLOT, BUFFER_SLOT + 0x120)
    require("QBuffer" in buffer_dis, "slot_0x20_constructs_qbuffer")

    # Negative controls: the claimed boundary is neither teardown nor any superseded final sink.
    dtor1 = disassemble(ns.objdump, ns.client, DTOR_1, DTOR_1 + 0x80)
    dtor2 = disassemble(ns.objdump, ns.client, DTOR_2, DTOR_2 + 0x80)
    require("0x2f69e30" in dtor1.lower() or "2f69e30" in dtor1.lower(), "dtor1_resets_intermediate_vptr")
    require("0x2f69e30" in dtor2.lower() or "2f69e30" in dtor2.lower(), "dtor2_resets_intermediate_vptr")
    require(SERIALIZE_1 not in (0xB5B880, 0xB46BD0, 0xC33259), "not_superseded_sink_address")

    slot_values = [elf.u64(INTERMEDIATE_AP + i * 8) for i in range(25)]
    result = {
        "schema_version": 1,
        "exact_client": {
            "sha256": digest,
            "size": EXPECTED_SIZE,
            "version_mapping": "15.32.df7b29",
            "platform": "official_native_linux_only",
        },
        "semantic_result": "SERIALIZATION_ONLY_PROVEN",
        "facts": {
            "tprotocolwriter_address_point": "0x2f69dd0",
            "tprotocolwriter_rtti": "0x3080728",
            "intermediate_address_point": "0x2f69e30",
            "intermediate_rtti": "0x3080748",
            "processor_address_point": "0x2f6a208",
            "processor_retains_intermediate_shared_pair": True,
            "intermediate_retains_writer_shared_pair": True,
            "first_two_intermediate_slots": ["0x7de7f0", "0x7dfd60"],
            "first_concrete_non_lifecycle_slot": "0xc10960",
            "first_concrete_slot_rel": "0x10",
            "first_concrete_slot_reads_retained_writer_member": "+0x18",
            "first_concrete_slot_operation": "QDataStream::operator<<(signed char)",
            "next_concrete_serializer_slot": "0xc20290",
            "next_serializer_reads_argument_fields": ["+0x30", "+0x34"],
            "next_serializer_operation": "QDataStream::operator<<(signed short)",
            "adjacent_buffer_slot": "0xc20c70",
            "adjacent_buffer_fact": "constructs QBuffer",
            "intermediate_first_25_slot_values": [f"0x{x:x}" for x in slot_values],
        },
        "classification": {
            "first_concrete_boundary": "STRUCTURED_OBJECT_ARGUMENT_TO_QDATASTREAM_SERIALIZATION",
            "input_representation": "STRUCTURED_OR_TYPED_OBJECT_ARGUMENT",
            "output_representation": "QDATASTREAM_SERIALIZATION_SINK",
            "temporal_first_in_entire_outbound_pipeline": "UNKNOWN",
            "qbuffer_order_relative_to_serialization": "UNKNOWN",
            "framing_order": "UNKNOWN",
            "sequence_order": "UNKNOWN",
            "compression_order": "UNKNOWN",
            "encryption_order": "UNKNOWN",
            "final_binary_egress": "UNKNOWN",
            "causal_local_harness": "UNKNOWN",
        },
        "negative_controls": {
            "first_two_slots_are_lifecycle_like": True,
            "generic_qiodevice_enumeration_used_as_discriminator": False,
            "vtable_adjacency_alone_used_as_proof": False,
            "b5b880_promoted": False,
            "b46bd0_promoted": False,
            "c33259_promoted": False,
        },
    }

    evidence_lines = [
        "P2_FIRST_TRANSFORM_RESULT=SERIALIZATION_ONLY_PROVEN",
        f"CLIENT_SHA256={digest}",
        f"CLIENT_SIZE={EXPECTED_SIZE}",
        "PROCESSOR_TO_INTERMEDIATE_RETENTION=FACT",
        "INTERMEDIATE_TO_TPROTOCOLWRITER_RETENTION=FACT",
        "INTERMEDIATE_FIRST_NON_LIFECYCLE_SLOT=0xc10960 rel=0x10",
        "INTERMEDIATE_FIRST_NON_LIFECYCLE_OPERATION=QDataStream::operator<<(signed char)",
        "INTERMEDIATE_NEXT_SERIALIZER_SLOT=0xc20290 rel=0x18",
        "INTERMEDIATE_NEXT_SERIALIZER_FIELDS=argument+0x30,argument+0x34",
        "INTERMEDIATE_ADJACENT_QBUFFER_SLOT=0xc20c70 rel=0x20",
        "TEMPORAL_PIPELINE_ORDER=UNKNOWN",
        "FRAMING_ORDER=UNKNOWN",
        "COMPRESSION_ORDER=UNKNOWN",
        "ENCRYPTION_ORDER=UNKNOWN",
        "FINAL_BINARY_EGRESS=UNKNOWN",
        "",
        "SANITIZED_DISASSEMBLY_C10960_BEGIN",
        *selected_lines(serial1, ("c109", "QDataStream")),
        "SANITIZED_DISASSEMBLY_C10960_END",
        "SANITIZED_DISASSEMBLY_C20290_BEGIN",
        *selected_lines(serial2, ("c202", "c203", "QDataStream")),
        "SANITIZED_DISASSEMBLY_C20290_END",
        "SANITIZED_DISASSEMBLY_C20C70_BEGIN",
        *selected_lines(buffer_dis, ("c20c", "c20d", "QBuffer")),
        "SANITIZED_DISASSEMBLY_C20C70_END",
    ]

    ns.output_json.parent.mkdir(parents=True, exist_ok=True)
    ns.output_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    ns.output_text.write_text("\n".join(evidence_lines[:15]) + "\n")
    ns.evidence.write_text("\n".join(evidence_lines) + "\n")

    print("P2_FIRST_TRANSFORM_COMPLETE=true")
    print("P2_FIRST_TRANSFORM_RESULT=SERIALIZATION_ONLY_PROVEN")
    print("P2_FIRST_CONCRETE_SLOT=0xc10960")
    print("P2_FRAMING_ORDER=UNKNOWN")
    print("P2_FINAL_BINARY_EGRESS=UNKNOWN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
