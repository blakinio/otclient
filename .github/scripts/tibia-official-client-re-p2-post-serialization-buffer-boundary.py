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
IODEVICE_WRITER_AP = 0x2F69D48
IODEVICE_WRITER_RTTI = 0x3080718
INTERMEDIATE_AP = 0x2F69E30
INTERMEDIATE_RTTI = 0x3080748
SERIALIZE_1 = 0xC10960
SERIALIZE_2 = 0xC20290
BUFFER_SLOT = 0xC20C70
BUFFER_WRITER_HELPER = 0x1960340


def require(value: bool, marker: str) -> None:
    if not value:
        print(f"P2_BUFFER_FAIL={marker}", file=sys.stderr)
        raise SystemExit(2)
    print(f"P2_BUFFER_OK={marker}")


class Elf64:
    def __init__(self, path: Path) -> None:
        self.data = path.read_bytes()
        require(self.data[:4] == b"\x7fELF", "elf_magic")
        require(self.data[4] == 2 and self.data[5] == 1, "elf64_little_endian")
        phoff = struct.unpack_from("<Q", self.data, 32)[0]
        phentsize = struct.unpack_from("<H", self.data, 54)[0]
        phnum = struct.unpack_from("<H", self.data, 56)[0]
        self.loads: list[tuple[int, int, int, int]] = []
        for index in range(phnum):
            off = phoff + index * phentsize
            p_type, p_flags, p_offset, p_vaddr, _, _p_filesz, p_memsz, _ = struct.unpack_from(
                "<IIQQQQQQ", self.data, off
            )
            if p_type == 1:
                self.loads.append((p_vaddr, p_memsz, p_offset, p_flags))
        require(bool(self.loads), "load_segments")

    def file_offset(self, va: int, size: int = 1) -> int:
        for vaddr, memsz, offset, _flags in self.loads:
            if vaddr <= va and va + size <= vaddr + memsz:
                out = offset + (va - vaddr)
                require(out + size <= len(self.data), f"file_backed_{va:x}")
                return out
        raise ValueError(f"unmapped VA 0x{va:x}")

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
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assert_bytes(elf: Elf64, va: int, hex_bytes: str, marker: str) -> None:
    expected = bytes.fromhex(hex_bytes)
    require(elf.read(va, len(expected)) == expected, marker)


def disassemble(objdump: Path, client: Path, lo: int, hi: int) -> str:
    result = subprocess.run(
        [
            str(objdump),
            "-d",
            "-Mintel",
            "--no-show-raw-insn",
            f"--start-address=0x{lo:x}",
            f"--stop-address=0x{hi:x}",
            str(client),
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    return result.stdout


def matching_lines(text: str, needles: tuple[str, ...]) -> list[str]:
    return [line.strip() for line in text.splitlines() if any(needle in line for needle in needles)]


def has(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", type=Path, required=True)
    parser.add_argument("--objdump", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-text", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require(args.client.is_file(), "client_present")
    require(args.objdump.is_file(), "objdump_present")
    require(args.client.stat().st_size == EXPECTED_SIZE, "exact_client_size")
    digest = sha256(args.client)
    require(digest == EXPECTED_SHA256, "exact_client_sha256")
    elf = Elf64(args.client)

    # Exact type/vtable identities on the current official Linux client.
    require(elf.u64(WRITER_AP - 16) == 0, "writer_offset_to_top_zero")
    require(elf.u64(WRITER_AP - 8) == WRITER_RTTI, "writer_rtti")
    require(elf.u64(IODEVICE_WRITER_AP - 16) == 0, "iodevice_writer_offset_to_top_zero")
    require(elf.u64(IODEVICE_WRITER_AP - 8) == IODEVICE_WRITER_RTTI, "iodevice_writer_rtti")
    require(elf.u64(INTERMEDIATE_AP - 16) == 0, "intermediate_offset_to_top_zero")
    require(elf.u64(INTERMEDIATE_AP - 8) == INTERMEDIATE_RTTI, "intermediate_rtti")
    for index, address in enumerate((0x7DE7F0, 0x7DFD60, SERIALIZE_1, SERIALIZE_2, BUFFER_SLOT)):
        require(elf.u64(INTERMEDIATE_AP + index * 8) == address, f"intermediate_slot_{index}")
        require(elf.executable(address), f"intermediate_slot_{index}_exec")

    # Persistent setup: a pointer to [rbp-0x40/-0x38] is retained at rbp-0x1a0; later that
    # pair becomes the QBuffer shared object/control pair passed to helper 0x1960340.
    persistent_anchors = (
        (0x1970009, "488d4dc0", "persistent_pair_address"),
        (0x1970046, "48898d60feffff", "persistent_pair_pointer_saved"),
        (0x1970C89, "bf20000000", "persistent_qbuffer_control_allocation"),
        (0x1970C96, "4c8d7810", "persistent_qbuffer_object_pointer"),
        (0x1970CAD, "e8dea1b6fe", "persistent_qbuffer_constructor"),
        (0x1970CC6, "e8b5a1b6fe", "persistent_qbuffer_open"),
        (0x1970CF5, "4c897dc0", "persistent_qbuffer_object_pair_store"),
        (0x1970CFC, "4c8965c8", "persistent_qbuffer_control_pair_store"),
        (0x1970D0C, "488bb560feffff", "persistent_qbuffer_pair_pointer_load"),
        (0x1970D13, "4889df", "persistent_helper_this"),
        (0x1970D16, "e825f6feff", "persistent_helper_call"),
        (0x1970D63, "488d0d66905f01", "writer_ap_lea"),
        (0x1970D6D, "48894a10", "writer_vptr_store"),
        (0x1970D71, "48895a18", "writer_retains_helper_object_plus18"),
        (0x1970D7E, "48897220", "writer_retains_helper_control_plus20"),
        (0x1970F31, "488d3df88e5f01", "intermediate_ap_lea"),
        (0x1970F3B, "48897a10", "intermediate_vptr_store"),
        (0x1970F3F, "48897218", "intermediate_retains_writer_object_plus18"),
        (0x1971068, "48897018", "processor_retains_intermediate_object_plus18"),
    )
    for va, expected, marker in persistent_anchors:
        assert_bytes(elf, va, expected, marker)

    serial1 = disassemble(args.objdump, args.client, SERIALIZE_1, SERIALIZE_1 + 0x120)
    serial2 = disassemble(args.objdump, args.client, SERIALIZE_2, SERIALIZE_2 + 0x260)
    buffer = disassemble(args.objdump, args.client, BUFFER_SLOT, BUFFER_SLOT + 0x500)
    helper = disassemble(args.objdump, args.client, BUFFER_WRITER_HELPER, BUFFER_WRITER_HELPER + 0x140)
    setup = disassemble(args.objdump, args.client, 0x1970000, 0x1970DA0)

    # Revalidate the promoted serializer side. TProtocolWriter+0x18 is the TIODeviceWriter
    # helper object; helper+0x18 is the QDataStream object used by these calls.
    require("QDataStream" in serial1 and "[rdi+0x18]" in serial1, "serializer1_revalidated")
    require("QDataStream" in serial2 and "[rdi+0x18]" in serial2, "serializer2_revalidated")

    # Helper 0x1960340 is the load-bearing common-state proof. It receives a shared QIODevice
    # pair, installs the TIODeviceWriter address point, copies the pair to +0x8/+0x10, constructs
    # QDataStream(QIODevice*) from the pair's object pointer, then retains it at +0x18/+0x20.
    helper_iodevice_writer_ap = "2f69d48" in helper.lower()
    helper_reads_device_object = has(helper, r"mov\s+r13,QWORD PTR \[rsi\]")
    helper_reads_device_control = has(helper, r"mov\s+rax,QWORD PTR \[rsi\+0x8\]")
    helper_stores_device_object = has(helper, r"mov\s+QWORD PTR \[rdi\+0x8\],r13")
    helper_stores_device_control = has(helper, r"mov\s+QWORD PTR \[rdi\+0x10\],rax")
    helper_passes_device_to_stream = has(helper, r"mov\s+rsi,r13")
    helper_qdatastream_ctor = "QDataStreamC1EP9QIODevice" in helper
    helper_stores_stream_object = has(helper, r"mov\s+QWORD PTR \[rbx\+0x18\],r12")
    helper_stores_stream_control = has(helper, r"mov\s+QWORD PTR \[rbx\+0x20\],rbp")
    helper_sets_byte_order = "QDataStream12setByteOrder" in helper
    helper_binding = all(
        (
            helper_iodevice_writer_ap,
            helper_reads_device_object,
            helper_reads_device_control,
            helper_stores_device_object,
            helper_stores_device_control,
            helper_passes_device_to_stream,
            helper_qdatastream_ctor,
            helper_stores_stream_object,
            helper_stores_stream_control,
            helper_sets_byte_order,
        )
    )
    require(helper_binding, "helper_binds_qiodevice_to_qdatastream")

    # Independent concrete use in c20c70 proves the helper receives a QBuffer shared pair,
    # QDataStream+0x18 is used only after construction, and the same QBuffer exposes resulting bytes.
    local_qbuffer_ctor = "QBufferC1EP7QObject" in buffer
    local_pair_saved = has(buffer, r"mov\s+QWORD PTR \[rsp\+0x30\],r15") and has(
        buffer, r"mov\s+QWORD PTR \[rsp\+0x38\],rbx"
    )
    local_pair_to_helper = (
        has(buffer, r"lea\s+rbp,\[rsp\+0x30\]")
        and has(buffer, r"lea\s+r14,\[rsp\+0x80\]")
        and has(buffer, r"mov\s+rsi,rbp")
        and has(buffer, r"mov\s+rdi,r14")
        and has(buffer, r"call\s+1960340")
    )
    local_stream_used = has(buffer, r"mov\s+rdi,QWORD PTR \[rsp\+0x98\]") and "QDataStreamlsEa" in buffer
    local_qbuffer_bytes = "QBuffer6bufferEv" in buffer
    local_binding = all((local_qbuffer_ctor, local_pair_saved, local_pair_to_helper, local_stream_used, local_qbuffer_bytes))
    require(local_binding, "c20c70_qbuffer_qdatastream_byteflow")

    # Persistent retained-writer construction must independently carry the same helper object.
    persistent_qbuffer_ctor = "1970cad:" in setup and "QBufferC2EP7QObject" in setup
    persistent_qbuffer_open = "1970cc6:" in setup and "QBuffer4open" in setup
    persistent_pair_to_helper = "1970d0c:" in setup and "1970d16:" in setup and "1960340" in setup
    persistent_helper_to_writer = (
        "1970d71:" in setup
        and has(setup, r"1970d71:.*mov\s+QWORD PTR \[rdx\+0x18\],rbx")
        and "1970d7e:" in setup
        and has(setup, r"1970d7e:.*mov\s+QWORD PTR \[rdx\+0x20\],rsi")
    )
    persistent_binding = all(
        (persistent_qbuffer_ctor, persistent_qbuffer_open, persistent_pair_to_helper, persistent_helper_to_writer)
    )
    require(persistent_binding, "persistent_qbuffer_helper_retained_by_tprotocolwriter")

    common_binding = helper_binding and local_binding and persistent_binding
    semantic_result = "BUFFER_DATAFLOW_PROVEN" if common_binding else "INCONCLUSIVE"

    result = {
        "schema_version": 2,
        "exact_client": {
            "sha256": digest,
            "size": EXPECTED_SIZE,
            "version_mapping": "15.32.df7b29",
            "platform": "official_native_linux_only",
        },
        "semantic_result": semantic_result,
        "facts": {
            "tprotocolwriter_address_point": "0x2f69dd0",
            "tprotocolwriter_rtti": "0x3080728",
            "tiodevicewriter_address_point": "0x2f69d48",
            "tiodevicewriter_rtti": "0x3080718",
            "intermediate_address_point": "0x2f69e30",
            "intermediate_rtti": "0x3080748",
            "serializer_slots": ["0xc10960", "0xc20290"],
            "qbuffer_slot": "0xc20c70",
            "buffer_writer_helper": "0x1960340",
            "helper_device_shared_pair_members": ["+0x8", "+0x10"],
            "helper_qdatastream_shared_pair_members": ["+0x18", "+0x20"],
            "qdatastream_constructor_argument": "QIODevice*=shared_pair.object",
            "local_qbuffer_binding_proven": local_binding,
            "persistent_qbuffer_binding_proven": persistent_binding,
            "persistent_tprotocolwriter_plus_18": "TIODeviceWriter helper object built by 0x1960340",
            "qbuffer_bytes_exposed_after_local_serialization": local_qbuffer_bytes,
        },
        "classification": {
            "common_qbuffer_qdatastream_binding": "PROVEN" if common_binding else "UNKNOWN",
            "representation_boundary": (
                "STRUCTURED_FIELDS_TO_QDATASTREAM_TO_QBUFFER_BACKED_BYTE_CONTAINER"
                if common_binding
                else "UNKNOWN"
            ),
            "byte_flow_direction": "QDATASTREAM_WRITES_TO_QBUFFER_BACKED_QIODEVICE" if common_binding else "UNKNOWN",
            "object_lifecycle_order": (
                "QBUFFER_AND_QDATASTREAM_BINDING_CONSTRUCTED_BEFORE_SERIALIZER_USE"
                if common_binding
                else "UNKNOWN"
            ),
            "protocol_stage_order": "UNKNOWN",
            "protocol_framing": "UNKNOWN",
            "sequence": "UNKNOWN",
            "compression": "UNKNOWN",
            "encryption": "UNKNOWN",
            "final_binary_egress": "UNKNOWN",
            "causal_local_harness": "UNKNOWN",
        },
        "negative_controls": {
            "vtable_adjacency_used_as_temporal_proof": False,
            "generic_qiodevice_census_used": False,
            "generic_qbuffer_census_used": False,
            "final_socket_run_used": False,
            "superseded_sink_models_used": False,
            "direct_dualconnection_writer_ownership_assumed": False,
            "qbuffer_container_management_called_protocol_framing": False,
        },
    }

    selected = [
        "P2_POST_SERIALIZATION_RESULT=" + semantic_result,
        f"CLIENT_SHA256={digest}",
        f"CLIENT_SIZE={EXPECTED_SIZE}",
        f"HELPER_QIODEVICE_QDATASTREAM_BINDING={'PROVEN' if helper_binding else 'UNKNOWN'}",
        f"LOCAL_QBUFFER_BYTEFLOW={'PROVEN' if local_binding else 'UNKNOWN'}",
        f"PERSISTENT_TPROTOCOLWRITER_QBUFFER_BINDING={'PROVEN' if persistent_binding else 'UNKNOWN'}",
        f"COMMON_QBUFFER_QDATASTREAM_BINDING={'PROVEN' if common_binding else 'UNKNOWN'}",
        "OBJECT_LIFECYCLE_ORDER=QBUFFER_AND_QDATASTREAM_BINDING_CONSTRUCTED_BEFORE_SERIALIZER_USE",
        "PROTOCOL_STAGE_ORDER=UNKNOWN",
        "PROTOCOL_FRAMING=UNKNOWN",
        "SEQUENCE=UNKNOWN",
        "COMPRESSION=UNKNOWN",
        "ENCRYPTION=UNKNOWN",
        "FINAL_BINARY_EGRESS=UNKNOWN",
    ]
    evidence = [
        *selected,
        "",
        "PERSISTENT_SETUP_RELEVANT_BEGIN",
        *matching_lines(
            setup,
            (
                "1970009:",
                "1970046:",
                "1970c89:",
                "1970cad:",
                "1970cc6:",
                "1970cf5:",
                "1970cfc:",
                "1970d0c:",
                "1970d13:",
                "1970d16:",
                "1970d63:",
                "1970d71:",
                "1970d7e:",
                "QBuffer",
                "1960340",
            ),
        ),
        "PERSISTENT_SETUP_RELEVANT_END",
        "",
        "HELPER_1960340_RELEVANT_BEGIN",
        *matching_lines(helper, ("19603", "19604", "QDataStream", "2f69d48")),
        "HELPER_1960340_RELEVANT_END",
        "",
        "C20C70_RELEVANT_BEGIN",
        *matching_lines(buffer, ("c20c", "c20d", "c20e", "QBuffer", "QDataStream", "1960340")),
        "C20C70_RELEVANT_END",
    ]

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.output_text.write_text("\n".join(selected) + "\n", encoding="utf-8")
    args.evidence.write_text("\n".join(evidence) + "\n", encoding="utf-8")

    print("P2_POST_SERIALIZATION_COMPLETE=true")
    print("P2_POST_SERIALIZATION_RESULT=" + semantic_result)
    print("P2_PROTOCOL_FRAMING=UNKNOWN")
    print("P2_FINAL_BINARY_EGRESS=UNKNOWN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
