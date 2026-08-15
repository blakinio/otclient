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
            p_type, p_flags, p_offset, p_vaddr, _, p_filesz, p_memsz, _ = struct.unpack_from(
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
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def dyn_symbols(objdump: Path, client: Path) -> list[str]:
    result = subprocess.run(
        [str(objdump), "-T", str(client)],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    needles = ("QDataStream", "QBuffer", "QIODevice", "QByteArray")
    return [line.strip() for line in result.stdout.splitlines() if any(n in line for n in needles)]


def lines(text: str, needles: tuple[str, ...]) -> list[str]:
    return [line.strip() for line in text.splitlines() if any(n in line for n in needles)]


def has(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


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

    # Independently revalidate the promoted identities and concrete serializer slots.
    require(elf.u64(WRITER_AP - 16) == 0, "writer_offset_to_top_zero")
    require(elf.u64(WRITER_AP - 8) == WRITER_RTTI, "writer_rtti")
    require(elf.u64(INTERMEDIATE_AP - 16) == 0, "intermediate_offset_to_top_zero")
    require(elf.u64(INTERMEDIATE_AP - 8) == INTERMEDIATE_RTTI, "intermediate_rtti")
    for index, address in enumerate((0x7DE7F0, 0x7DFD60, SERIALIZE_1, SERIALIZE_2, BUFFER_SLOT)):
        require(elf.u64(INTERMEDIATE_AP + index * 8) == address, f"intermediate_slot_{index}")
        require(elf.executable(address), f"intermediate_slot_{index}_exec")

    # Retention provenance copied only as exact-byte gates from the accepted branch, not as narrative assumptions.
    assert_bytes(elf, 0x1970D63, "488d0d66905f01", "writer_ap_lea")
    assert_bytes(elf, 0x1970D6D, "48894a10", "writer_vptr_store")
    assert_bytes(elf, 0x1970F31, "488d3df88e5f01", "intermediate_ap_lea")
    assert_bytes(elf, 0x1970F3B, "48897a10", "intermediate_vptr_store")
    assert_bytes(elf, 0x1970F3F, "48897218", "intermediate_retains_writer_object_plus18")
    assert_bytes(elf, 0x1971068, "48897018", "processor_retains_intermediate_object_plus18")

    serial1 = disassemble(ns.objdump, ns.client, SERIALIZE_1, SERIALIZE_1 + 0x120)
    serial2 = disassemble(ns.objdump, ns.client, SERIALIZE_2, SERIALIZE_2 + 0x260)
    buffer = disassemble(ns.objdump, ns.client, BUFFER_SLOT, BUFFER_SLOT + 0x900)
    helper = disassemble(ns.objdump, ns.client, BUFFER_WRITER_HELPER, BUFFER_WRITER_HELPER + 0x500)
    symbols = dyn_symbols(ns.objdump, ns.client)

    require("QDataStream" in serial1 and "[rdi+0x18]" in serial1, "serializer1_revalidated")
    require("QDataStream" in serial2 and "[rdi+0x18]" in serial2, "serializer2_revalidated")
    require("QBufferC" in buffer, "qbuffer_constructor_present")
    require("1960340" in buffer.lower(), "qbuffer_pair_passed_to_helper_callsite")
    require("[rsp+0x98]" in buffer and "QDataStream" in buffer, "local_writer_qdatastream_member_used")

    # Direct-control/data-flow observations in c20c70.
    qbuffer_allocated = has(buffer, r"call\s+.*QBufferC[12]EP7QObject")
    pair_saved = has(buffer, r"mov\s+QWORD PTR \[rsp\+0x30\],r15") and has(
        buffer, r"mov\s+QWORD PTR \[rsp\+0x38\],rbx"
    )
    pair_to_helper = (
        has(buffer, r"lea\s+r14,\[rsp\+0x80\]")
        and has(buffer, r"lea\s+rbp,\[rsp\+0x30\]")
        and has(buffer, r"mov\s+rsi,rbp")
        and has(buffer, r"mov\s+rdi,r14")
        and has(buffer, r"call\s+1960340")
    )
    local_stream_used = has(buffer, r"mov\s+rdi,QWORD PTR \[rsp\+0x98\]") and "QDataStream" in buffer

    # The helper is the load-bearing discriminator: prove whether the shared QBuffer-backed device
    # is bound into a QDataStream member of the constructed stack writer/helper object.
    helper_qdatastream_ctor = has(helper, r"QDataStreamC[12]")
    helper_set_device = has(helper, r"QDataStream.*setDevice")
    helper_qiodevice = "QIODevice" in helper
    helper_qbuffer = "QBuffer" in helper
    helper_writer_member_18 = has(helper, r"\+0x18\]") or has(helper, r"\+0x18")

    # Byte-container extraction/consumption within the same c20c70 body is supporting evidence only.
    bytearray_calls = lines(buffer, ("QByteArray", "QBuffer", "QIODevice"))
    qbuffer_data_or_read = any(
        token in line
        for line in bytearray_calls
        for token in ("QBuffer", "readAll", "QByteArray")
    )

    common_binding = qbuffer_allocated and pair_saved and pair_to_helper and local_stream_used and (
        helper_qdatastream_ctor or helper_set_device
    )

    if common_binding:
        semantic_result = "BUFFER_DATAFLOW_PROVEN"
        representation = "QBUFFER_SHARED_DEVICE_TO_LOCAL_QDATASTREAM_SERIALIZATION"
    elif qbuffer_allocated and pair_saved and pair_to_helper and local_stream_used:
        semantic_result = "SERIALIZATION_TARGET_PROVEN_BUFFER_ORDER_UNKNOWN"
        representation = "QBUFFER_AND_QDATASTREAM_SAME_LOCAL_CONSTRUCTION_PATH_BINDING_UNRESOLVED"
    else:
        semantic_result = "INCONCLUSIVE"
        representation = "UNKNOWN"

    # Do not infer protocol framing merely from a local temporary buffer or byte-array operation.
    framing_edge = False

    result = {
        "schema_version": 1,
        "exact_client": {
            "sha256": digest,
            "size": EXPECTED_SIZE,
            "version_mapping": "15.32.df7b29",
            "platform": "official_native_linux_only",
        },
        "semantic_result": semantic_result,
        "facts": {
            "writer_address_point": "0x2f69dd0",
            "writer_rtti": "0x3080728",
            "intermediate_address_point": "0x2f69e30",
            "intermediate_rtti": "0x3080748",
            "serializer_slots": ["0xc10960", "0xc20290"],
            "qbuffer_slot": "0xc20c70",
            "qbuffer_writer_helper": "0x1960340",
            "qbuffer_allocated": qbuffer_allocated,
            "qbuffer_shared_pair_saved_at_stack_30_38": pair_saved,
            "qbuffer_shared_pair_passed_to_helper": pair_to_helper,
            "local_constructed_object_qdatastream_member_at_stack_98_used": local_stream_used,
            "helper_qdatastream_constructor_observed": helper_qdatastream_ctor,
            "helper_qdatastream_set_device_observed": helper_set_device,
            "helper_qiodevice_reference_observed": helper_qiodevice,
            "helper_qbuffer_reference_observed": helper_qbuffer,
            "helper_member_plus_18_reference_observed": helper_writer_member_18,
            "same_body_qbuffer_or_bytearray_use_observed": qbuffer_data_or_read,
        },
        "classification": {
            "representation_boundary": representation,
            "common_qbuffer_qdatastream_binding": "PROVEN" if common_binding else "UNKNOWN",
            "temporal_order": "DIRECT_LOCAL_CONSTRUCTION_BEFORE_LOCAL_SERIALIZATION" if common_binding else "UNKNOWN",
            "protocol_framing": "PROVEN" if framing_edge else "UNKNOWN",
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
        },
    }

    selected = [
        "P2_POST_SERIALIZATION_RESULT=" + semantic_result,
        f"CLIENT_SHA256={digest}",
        f"CLIENT_SIZE={EXPECTED_SIZE}",
        f"QBUFFER_ALLOCATED={str(qbuffer_allocated).lower()}",
        f"QBUFFER_SHARED_PAIR_SAVED={str(pair_saved).lower()}",
        f"QBUFFER_SHARED_PAIR_TO_HELPER={str(pair_to_helper).lower()}",
        f"LOCAL_QDATASTREAM_MEMBER_USED={str(local_stream_used).lower()}",
        f"HELPER_QDATASTREAM_CTOR={str(helper_qdatastream_ctor).lower()}",
        f"HELPER_QDATASTREAM_SET_DEVICE={str(helper_set_device).lower()}",
        f"COMMON_QBUFFER_QDATASTREAM_BINDING={'PROVEN' if common_binding else 'UNKNOWN'}",
        "PROTOCOL_FRAMING=UNKNOWN",
        "SEQUENCE=UNKNOWN",
        "COMPRESSION=UNKNOWN",
        "ENCRYPTION=UNKNOWN",
        "FINAL_BINARY_EGRESS=UNKNOWN",
    ]

    evidence = [
        *selected,
        "",
        "C20C70_RELEVANT_BEGIN",
        *lines(buffer, ("c20c", "c20d", "c20e", "c20f", "c210", "c211", "QBuffer", "QDataStream", "QByteArray", "QIODevice", "1960340")),
        "C20C70_RELEVANT_END",
        "",
        "HELPER_1960340_RELEVANT_BEGIN",
        *lines(helper, ("19603", "19604", "19605", "QDataStream", "QBuffer", "QIODevice", "QByteArray")),
        "HELPER_1960340_RELEVANT_END",
        "",
        "DYNAMIC_QT_SYMBOLS_BEGIN",
        *symbols[:300],
        "DYNAMIC_QT_SYMBOLS_END",
    ]

    ns.output_json.parent.mkdir(parents=True, exist_ok=True)
    ns.output_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ns.output_text.write_text("\n".join(selected) + "\n", encoding="utf-8")
    ns.evidence.write_text("\n".join(evidence) + "\n", encoding="utf-8")

    print("P2_POST_SERIALIZATION_COMPLETE=true")
    print("P2_POST_SERIALIZATION_RESULT=" + semantic_result)
    print("P2_PROTOCOL_FRAMING=UNKNOWN")
    print("P2_FINAL_BINARY_EGRESS=UNKNOWN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
