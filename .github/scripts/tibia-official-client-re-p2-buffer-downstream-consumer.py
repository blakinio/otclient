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

# Coordinator-promoted #308 exact type / retained-writer fence.
WRITER_AP = 0x2F69DD0
WRITER_RTTI = 0x3080728
IODEVICE_WRITER_AP = 0x2F69D48
IODEVICE_WRITER_RTTI = 0x3080718
INTERMEDIATE_AP = 0x2F69E30
INTERMEDIATE_RTTI = 0x3080748

# Exact setup / processor graph on the fenced client.
CLIENT_PROCESSOR_AP = 0x2F6A208
RAW_PROCESSOR_AP = 0x2F6A230
CLIENT_PROCESSOR_ENTRY = 0xC2DF80
RAW_PROCESSOR_ENTRY = 0xB47130
CONNECTION_INVOKER = 0x7DD630
DUAL_PRECONDITION = 0xB40370
DUAL_ENTRY_80 = 0xB56D60
DUAL_ENTRY_78 = 0xB56970


def require(value: bool, marker: str) -> None:
    if not value:
        print(f"P2_DOWNSTREAM_FAIL={marker}", file=sys.stderr)
        raise SystemExit(2)
    print(f"P2_DOWNSTREAM_OK={marker}")


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
            if p_type == 1 and p_filesz:
                self.loads.append((p_vaddr, min(p_memsz, p_filesz), p_offset, p_flags))
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
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def disassemble(objdump: Path, client: Path, lo: int, hi: int) -> str:
    p = subprocess.run(
        [
            str(objdump), "-d", "-Mintel", "--no-show-raw-insn",
            f"--start-address=0x{lo:x}", f"--stop-address=0x{hi:x}", str(client),
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    return p.stdout


def instruction_map(text: str) -> dict[int, str]:
    out: dict[int, str] = {}
    for line in text.splitlines():
        m = re.match(r"^\s*([0-9a-f]+):\s*(.*)$", line, re.I)
        if m:
            out[int(m.group(1), 16)] = m.group(2).strip()
    return out


def at(insns: dict[int, str], addr: int, *needles: str) -> bool:
    line = insns.get(addr, "").lower()
    return bool(line) and all(n.lower() in line for n in needles)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--client", type=Path, required=True)
    p.add_argument("--objdump", type=Path, required=True)
    p.add_argument("--output-json", type=Path, required=True)
    p.add_argument("--output-text", type=Path, required=True)
    p.add_argument("--evidence", type=Path, required=True)
    args = p.parse_args()

    require(args.client.is_file(), "client_present")
    require(args.objdump.is_file(), "objdump_present")
    require(args.client.stat().st_size == EXPECTED_SIZE, "exact_client_size")
    digest = sha256(args.client)
    require(digest == EXPECTED_SHA256, "exact_client_sha256")
    elf = Elf64(args.client)

    # Revalidate promoted type anchors and correct the false-positive writer vtable bleed from run #1.
    for ap, rtti, name in (
        (WRITER_AP, WRITER_RTTI, "writer"),
        (IODEVICE_WRITER_AP, IODEVICE_WRITER_RTTI, "iodevice_writer"),
        (INTERMEDIATE_AP, INTERMEDIATE_RTTI, "intermediate"),
    ):
        require(elf.u64(ap - 16) == 0, f"{name}_offset_to_top_zero")
        require(elf.u64(ap - 8) == rtti, f"{name}_rtti")
    require([elf.u64(WRITER_AP + i * 8) for i in range(5)] == [0x7E3C10, 0x7E3CA0, 0xC262B0, 0xC21EC0, 0], "writer_real_vtable_boundary")
    require(elf.u64(WRITER_AP + 5 * 8) == 0x3080738, "writer_neighbor_rtti_not_slot")
    require(elf.u64(WRITER_AP + 8 * 8) == 0xD114C0, "historical_bleed_address_present_not_writer_slot")

    # Exact processor vtable identities: this turns the invoker's indirect calls into typed edges.
    require(elf.u64(CLIENT_PROCESSOR_AP + 0x10) == CLIENT_PROCESSOR_ENTRY, "client_processor_virtual_plus10")
    require(elf.u64(RAW_PROCESSOR_AP + 0x10) == RAW_PROCESSOR_ENTRY, "raw_processor_virtual_plus10")

    setup = disassemble(args.objdump, args.client, 0x1970C80, 0x19710B5)
    setup_i = instruction_map(setup)

    # Persistent QBuffer object provenance from #308: actual QBuffer object is r15 = allocation+0x10.
    require(at(setup_i, 0x1970C96, "lea", "r15,[rax+0x10]"), "persistent_qbuffer_object_pointer")
    require(at(setup_i, 0x1970CAD, "call", "QBufferC2"), "persistent_qbuffer_constructor")
    require(at(setup_i, 0x1970CC6, "call", "QBuffer4open"), "persistent_qbuffer_open")
    require(at(setup_i, 0x1970CA6, "[rbp-0x218]", "r15"), "persistent_qbuffer_saved_rbpm218")

    # TProtocolClientMessageProcessor actual object begins at allocation+0x10.  Its this+0x18
    # receives the SAME saved persistent QBuffer object from rbp-0x218.
    require(at(setup_i, 0x197104F, "lea", "rdx,[rax+0x10]"), "client_processor_actual_object_pointer")
    require(at(setup_i, 0x1971056, "0x2f6a208"), "client_processor_ap_loaded")
    require(at(setup_i, 0x197105D, "[rax+0x10]", "rcx"), "client_processor_vptr_store")
    require(at(setup_i, 0x1971084, "rsi", "[rbp-0x218]"), "client_processor_reloads_same_qbuffer")
    require(at(setup_i, 0x197108F, "[rax+0x28]", "rsi"), "client_processor_this_plus18_qbuffer_store")
    require(at(setup_i, 0x19710A7, "[rcx+0xa00]", "rdx"), "outer_retains_client_processor")

    invoker = disassemble(args.objdump, args.client, 0x7DD630, 0x7DD720)
    inv_i = instruction_map(invoker)
    client_proc = disassemble(args.objdump, args.client, 0xC2DF80, 0xC2E080)
    cp_i = instruction_map(client_proc)
    raw_proc = disassemble(args.objdump, args.client, 0xB47130, 0xB47320)
    rp_i = instruction_map(raw_proc)

    # Exact invoker pipeline. rbp=rsp is the same stack message object across all downstream calls.
    require(at(inv_i, 0x7DD66C, "mov", "rbp,rsp"), "invoker_message_object_is_rsp")
    require(at(inv_i, 0x7DD66F, "rdx,r12"), "invoker_signal_argument_to_client_processor")
    require(at(inv_i, 0x7DD672, "rdi,rbp"), "invoker_client_processor_sret_message")
    require(at(inv_i, 0x7DD675, "rsi", "[rax+0xa00]"), "invoker_client_processor_this")
    require(at(inv_i, 0x7DD67F, "call", "[rax+0x10]"), "invoker_calls_client_processor_plus10")
    require(at(inv_i, 0x7DD686, "rsi,rbp"), "invoker_same_message_to_raw_processor")
    require(at(inv_i, 0x7DD689, "rdi", "[rax+0xa10]"), "invoker_raw_processor_this")
    require(at(inv_i, 0x7DD693, "call", "[rax+0x10]"), "invoker_calls_raw_processor_plus10")
    require(at(inv_i, 0x7DD69A, "rsi,rbp"), "invoker_same_message_to_dual_plus80")
    require(at(inv_i, 0x7DD69D, "rdi", "[rax+0xc18]"), "invoker_dual_this_plus80")
    require(at(inv_i, 0x7DD6A7, "call", "[rax+0x80]"), "invoker_calls_dual_plus80")
    require(at(inv_i, 0x7DD6B1, "rsi,rbp"), "invoker_same_message_to_dual_plus78")
    require(at(inv_i, 0x7DD6B4, "rdi", "[rax+0xc18]"), "invoker_dual_this_plus78")
    require(at(inv_i, 0x7DD6BE, "call", "[rax+0x78]"), "invoker_calls_dual_plus78")

    # Client processor exact ABI/data flow: (sret message, this, signal arg).
    require(at(cp_i, 0xC2DF86, "r12,rdx"), "client_processor_captures_signal_arg")
    require(at(cp_i, 0xC2DF8A, "rbp,rsi"), "client_processor_captures_this")
    require(at(cp_i, 0xC2DF8E, "rbx,rdi"), "client_processor_captures_sret_message")
    require(at(cp_i, 0xC2DF95, "rdi", "[rsi+0x8]"), "client_processor_retained_intermediate_this")
    require(at(cp_i, 0xC2DF99, "rsi,rdx"), "client_processor_signal_to_intermediate")
    require(at(cp_i, 0xC2DFA2, "call", "[rax+0x10]"), "client_processor_invokes_retained_intermediate")

    # This is the first exact consumer of the promoted persistent QBuffer: same this+0x18 pointer
    # established above is passed to QIODevice::readAll().
    require(at(cp_i, 0xC2DFA5, "rdi", "[rbp+0x18]"), "client_processor_reads_persistent_qbuffer_member")
    require(at(cp_i, 0xC2DFD5, "call", "QIODevice7readAll"), "persistent_qbuffer_qiodevice_readall")
    require(at(cp_i, 0xC2DFEB, "lea", "rbp,[rbx+0x8]"), "client_processor_output_qbytearray_field")
    require(at(cp_i, 0xC2E012, "call", "QByteArrayaSERKS"), "client_processor_assigns_qbytearray_output")
    require(at(cp_i, 0xC2E040, "rax,rbx"), "client_processor_returns_message_object")

    # RawDataProcessor consumes the SAME message object and transforms its QByteArray at +0x8 in place.
    require(at(rp_i, 0xB47132, "lea", "rax,[rsi+0x8]"), "raw_processor_message_qbytearray_pointer")
    require(at(rp_i, 0xB47151, "[rsp+0x8]", "rax"), "raw_processor_saves_input_qbytearray_pointer")
    require(at(rp_i, 0xB47189, "call", "QByteArray6insert"), "raw_processor_qbytearray_insert")
    require(at(rp_i, 0xB47206, "call", "QByteArray6append"), "raw_processor_qbytearray_append")
    require(at(rp_i, 0xB47287, "[r12+0x28]"), "raw_processor_reads_same_message_state")
    require(at(rp_i, 0xB472F8, "rdi", "[rsp+0x8]"), "raw_processor_reloads_input_qbytearray_pointer")
    require(at(rp_i, 0xB47300, "call", "QByteArrayaSERKS"), "raw_processor_assigns_transformed_qbytearray_in_place")

    result = {
        "schema_version": 3,
        "exact_client": {
            "sha256": digest,
            "size": EXPECTED_SIZE,
            "version_mapping": "15.32.df7b29",
            "platform": "official_native_linux_only",
        },
        "false_positive_correction": {
            "tprotocolwriter_real_slots": ["0x7e3c10", "0x7e3ca0", "0xc262b0", "0xc21ec0"],
            "tprotocolwriter_slot4": "0x0",
            "0xd114c0_is_not_tprotocolwriter_slot8": True,
            "run_31904191629_fixed_window_candidates_rejected": True,
        },
        "provenance": {
            "persistent_qbuffer_saved_at_setup_scratch": "rbp-0x218",
            "persistent_qbuffer_stored_in_client_processor_member": "this+0x18",
            "client_processor_outer_member": "outer+0xa00",
            "raw_processor_outer_member": "outer+0xa10",
            "dualconnection_outer_member": "outer+0xc18",
        },
        "stage_order": [
            {
                "stage": "TProtocolClientMessageProcessor virtual +0x10",
                "entry": "0xc2df80",
                "input": "signal argument",
                "effect": "invoke retained intermediate, then QIODevice::readAll on exact persistent QBuffer at this+0x18, assign bytes to output QByteArray at message+0x8",
            },
            {
                "stage": "TGameserverNetworkPacketRawDataProcessor virtual +0x10",
                "entry": "0xb47130",
                "input": "same message object",
                "effect": "QByteArray insert/append/reallocation path and in-place assignment back to message+0x8",
            },
            {
                "stage": "TGameserverDualConnection virtual +0x80",
                "entry": "0xb56d60",
                "input": "same post-raw message object",
                "effect": "consumer call proven; transport semantics not classified here",
            },
            {
                "stage": "TGameserverDualConnection virtual +0x78",
                "entry": "0xb56970",
                "input": "same post-raw message object",
                "effect": "consumer call proven; transport semantics not classified here",
            },
        ],
        "classification": {
            "persistent_qbuffer_direct_readall": "PROVEN",
            "first_downstream_consumer": "PROVEN:TProtocolClientMessageProcessor+0x10@0xc2df80",
            "first_downstream_transform": "PROVEN:TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130",
            "same_message_handoff_to_dualconnection": "PROVEN",
            "protocol_stage_order": "PROVEN_PARTIAL",
            "framing": "UNKNOWN",
            "sequence": "UNKNOWN",
            "compression": "UNKNOWN",
            "encryption": "UNKNOWN",
            "final_binary_egress": "UNKNOWN",
            "causal_local_harness": "UNKNOWN",
        },
        "negative_controls": {
            "generic_qiodevice_census_used_as_proof": False,
            "generic_qbuffer_census_used_as_proof": False,
            "vtable_adjacency_used_as_temporal_proof": False,
            "historical_final_socket_run_used_as_proof": False,
            "direct_dualconnection_writer_ownership_assumed": False,
            "dual_plus80_or_plus78_labeled_final_egress": False,
            "raw_byte_transform_labeled_framing_without_semantics": False,
        },
        "semantic_result": "POST_SERIALIZATION_PROCESSOR_CHAIN_PROVEN",
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.output_text.write_text(
        "\n".join(
            [
                "P2_DOWNSTREAM_RESULT=POST_SERIALIZATION_PROCESSOR_CHAIN_PROVEN",
                f"CLIENT_SHA256={digest}",
                f"CLIENT_SIZE={EXPECTED_SIZE}",
                "TPROTOCOLWRITER_SLOT_BOUNDARY=PROVEN_SLOT4_ZERO",
                "PERSISTENT_QBUFFER_DIRECT_READALL=PROVEN",
                "FIRST_DOWNSTREAM_CONSUMER=PROVEN:TProtocolClientMessageProcessor+0x10@0xc2df80",
                "FIRST_DOWNSTREAM_TRANSFORM=PROVEN:TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130",
                "SAME_MESSAGE_HANDOFF_TO_DUALCONNECTION=PROVEN",
                "PROTOCOL_STAGE_ORDER=PROVEN_PARTIAL",
                "PROTOCOL_FRAMING=UNKNOWN",
                "SEQUENCE=UNKNOWN",
                "COMPRESSION=UNKNOWN",
                "ENCRYPTION=UNKNOWN",
                "FINAL_BINARY_EGRESS=UNKNOWN",
                "CAUSAL_LOCAL_HARNESS=UNKNOWN",
            ]
        ) + "\n",
        encoding="utf-8",
    )

    evidence = [
        "# Persistent QBuffer -> ClientMessageProcessor setup",
        *[f"{a:x}: {setup_i[a]}" for a in sorted(setup_i) if a in {
            0x1970C96,0x1970CA6,0x1970CAD,0x1970CC6,0x197104F,0x1971056,0x197105D,
            0x1971084,0x197108F,0x19710A7,
        }],
        "",
        "# Exact invoker stage order",
        *[f"{a:x}: {inv_i[a]}" for a in sorted(inv_i)],
        "",
        "# TProtocolClientMessageProcessor exact downstream read",
        *[f"{a:x}: {cp_i[a]}" for a in sorted(cp_i)],
        "",
        "# TGameserverNetworkPacketRawDataProcessor exact in-place transform",
        *[f"{a:x}: {rp_i[a]}" for a in sorted(rp_i)],
    ]
    args.evidence.write_text("\n".join(evidence) + "\n", encoding="utf-8")

    print("P2_DOWNSTREAM_COMPLETE=true")
    print("P2_DOWNSTREAM_RESULT=POST_SERIALIZATION_PROCESSOR_CHAIN_PROVEN")
    print("P2_DOWNSTREAM_PERSISTENT_QBUFFER_DIRECT_READALL=PROVEN")
    print("P2_DOWNSTREAM_FIRST_CONSUMER=PROVEN")
    print("P2_DOWNSTREAM_FIRST_TRANSFORM=PROVEN")
    print("P2_DOWNSTREAM_SAME_MESSAGE_TO_DUALCONNECTION=PROVEN")
    print("P2_DOWNSTREAM_PROTOCOL_STAGE_ORDER=PROVEN_PARTIAL")
    print("P2_DOWNSTREAM_PROTOCOL_FRAMING=UNKNOWN")
    print("P2_DOWNSTREAM_FINAL_BINARY_EGRESS=UNKNOWN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
