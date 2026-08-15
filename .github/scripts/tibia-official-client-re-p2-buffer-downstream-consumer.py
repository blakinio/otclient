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
INTERMEDIATE_PREFIX = (0x7DE7F0, 0x7DFD60, 0xC10960, 0xC20290, 0xC20C70)
CONNECTION_SITE = 0x19716A3
INVOKER_LEA = 0x1971670
SIGNAL_META_LEA = 0x1971677
OUTER_CAPTURE_STORE = 0x197168D
INVOKER = 0x7DD630
SIGNAL_META = 0x3085B60
CONNECT_IMPL = 0x4DD800
CLIENT_MESSAGE_PROCESSOR = 0xC2DF80
RAW_DATA_PROCESSOR = 0xB47130
DUAL_ENTRY_78 = 0xB56970
DUAL_ENTRY_80 = 0xB56D60
DUAL_PRECONDITION = 0xB40370


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

    def rip_target(self, site: int, length: int = 7, disp_offset: int = 3) -> int:
        raw = self.read(site, length)
        disp = struct.unpack_from("<i", raw, disp_offset)[0]
        return (site + length + disp) & 0xFFFFFFFFFFFFFFFF

    def call_target(self, site: int) -> int:
        raw = self.read(site, 5)
        require(raw[0] == 0xE8, f"direct_call_opcode_{site:x}")
        return (site + 5 + struct.unpack_from("<i", raw, 1)[0]) & 0xFFFFFFFFFFFFFFFF


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def disassemble(objdump: Path, client: Path, lo: int, hi: int) -> str:
    p = subprocess.run(
        [str(objdump), "-d", "-Mintel", "--no-show-raw-insn", f"--start-address=0x{lo:x}", f"--stop-address=0x{hi:x}", str(client)],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    return p.stdout


def insn_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if re.match(r"^[0-9a-f]+:", line.strip(), re.I)]


def bounded_relevant(text: str) -> list[str]:
    needles = (
        "call", "+0xa00", "+0xa08", "+0xa10", "+0xa18", "+0xc18", "+0xc20",
        "QBuffer", "QDataStream", "QIODevice", "QByteArray", "write", "send", "compress", "encrypt",
        "+0x18", "+0x20", "+0x28", "+0x30",
    )
    return [line for line in insn_lines(text) if any(n.lower() in line.lower() for n in needles)][:200]


def actual_vtable_slots(elf: Elf64, ap: int, maximum: int) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for index in range(maximum):
        value = elf.u64(ap + index * 8)
        is_exec = elf.executable(value)
        out.append({"index": index, "va": f"0x{value:x}", "executable": is_exec})
        if not is_exec:
            break
    return out


def body_flags(text: str) -> dict[str, object]:
    lowered = text.lower()
    return {
        "outer_a00": bool(re.search(r"\+0xa00\]", lowered)),
        "outer_a10": bool(re.search(r"\+0xa10\]", lowered)),
        "outer_c18": bool(re.search(r"\+0xc18\]", lowered)),
        "qbuffer": "qbuffer" in lowered,
        "qdatastream": "qdatastream" in lowered,
        "qiodevice": "qiodevice" in lowered,
        "qbytearray": "qbytearray" in lowered,
        "write_text": "write" in lowered,
        "send_text": "send" in lowered,
        "compress_text": "compress" in lowered,
        "encrypt_text": "encrypt" in lowered,
        "calls": [line for line in insn_lines(text) if "call" in line.lower()][:80],
    }


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

    for ap, rtti, name in (
        (WRITER_AP, WRITER_RTTI, "writer"),
        (IODEVICE_WRITER_AP, IODEVICE_WRITER_RTTI, "iodevice_writer"),
        (INTERMEDIATE_AP, INTERMEDIATE_RTTI, "intermediate"),
    ):
        require(elf.u64(ap - 16) == 0, f"{name}_offset_to_top_zero")
        require(elf.u64(ap - 8) == rtti, f"{name}_rtti")

    writer_slots = actual_vtable_slots(elf, WRITER_AP, 12)
    require([int(str(x["va"]), 16) for x in writer_slots[:4]] == [0x7E3C10, 0x7E3CA0, 0xC262B0, 0xC21EC0], "writer_real_slots_0_3")
    require(len(writer_slots) == 5 and writer_slots[4]["va"] == "0x0" and not writer_slots[4]["executable"], "writer_vtable_stops_at_slot4_zero")
    require(elf.u64(WRITER_AP + 5 * 8) == 0x3080738, "writer_neighbor_rtti_not_slot")
    require(elf.u64(WRITER_AP + 8 * 8) == 0xD114C0, "historical_false_positive_address_present_but_not_writer_slot")

    for i, expected in enumerate(INTERMEDIATE_PREFIX):
        require(elf.u64(INTERMEDIATE_AP + i * 8) == expected, f"intermediate_slot_{i}")
        require(elf.executable(expected), f"intermediate_slot_{i}_exec")

    require(elf.rip_target(INVOKER_LEA) == INVOKER, "connection_invoker_target")
    require(elf.rip_target(SIGNAL_META_LEA) == SIGNAL_META, "connection_signal_meta_target")
    require(elf.call_target(CONNECTION_SITE) == CONNECT_IMPL, "connection_connectimpl_target")

    connection = disassemble(args.objdump, args.client, 0x1971635, 0x19716A8)
    connection_lines = insn_lines(connection)
    require(any(line.lower().startswith("197168d:") and "+0x10" in line.lower() for line in connection_lines), "connection_captures_outer_at_slotobject_plus10")

    targets = {
        "invoker_0x7dd630": (INVOKER, 0x7DD9A0),
        "client_message_processor_0xc2df80": (CLIENT_MESSAGE_PROCESSOR, 0xC2E680),
        "raw_data_processor_0xb47130": (RAW_DATA_PROCESSOR, 0xB47880),
        "dual_entry_0xb56970": (DUAL_ENTRY_78, 0xB56D60),
        "dual_entry_0xb56d60": (DUAL_ENTRY_80, 0xB57280),
        "dual_precondition_0xb40370": (DUAL_PRECONDITION, 0xB40880),
    }
    bodies: dict[str, dict[str, object]] = {}
    for name, (lo, hi) in targets.items():
        require(elf.executable(lo), f"target_exec_{lo:x}")
        text = disassemble(args.objdump, args.client, lo, hi)
        bodies[name] = {
            "start": f"0x{lo:x}",
            "stop": f"0x{hi:x}",
            "flags": body_flags(text),
            "relevant": bounded_relevant(text),
            "instruction_count": len(insn_lines(text)),
        }

    inv_flags = bodies["invoker_0x7dd630"]["flags"]
    proc_flags = bodies["client_message_processor_0xc2df80"]["flags"]
    raw_flags = bodies["raw_data_processor_0xb47130"]["flags"]
    exact_processor_graph_signal = bool(inv_flags["outer_a00"] or inv_flags["outer_a10"] or proc_flags["outer_a10"])
    concrete_byte_type_signal = any(
        bool(flags[key])
        for flags in (inv_flags, proc_flags, raw_flags)
        for key in ("qbuffer", "qbytearray", "qiodevice")
    )

    # A targeted capture is not itself a downstream proof. Only an explicit byte/container signal on
    # the exact processor path earns CANDIDATE; otherwise the byte consumer remains UNKNOWN.
    first_downstream = "CANDIDATE" if exact_processor_graph_signal and concrete_byte_type_signal else "UNKNOWN"
    result = {
        "schema_version": 2,
        "exact_client": {"sha256": digest, "size": EXPECTED_SIZE, "version_mapping": "15.32.df7b29", "platform": "official_native_linux_only"},
        "writer_vtable": writer_slots,
        "false_positive_correction": {
            "writer_stops_at_slot4_zero": True,
            "writer_ap_plus_0x28_is_neighbor_rtti_0x3080738": True,
            "0xd114c0_is_not_tprotocolwriter_slot8": True,
            "fixed_0x280_window_candidates_from_run_31904191629_are_not_semantic_proof": True,
        },
        "connection": {
            "site": "0x19716a3",
            "invoker": "0x7dd630",
            "signal_meta": "0x3085b60",
            "connect_impl": "0x4dd800",
            "outer_capture_store": "0x197168d",
            "relevant": bounded_relevant(connection),
        },
        "targets": bodies,
        "classification": {
            "exact_processor_graph_signal": exact_processor_graph_signal,
            "concrete_byte_type_signal": concrete_byte_type_signal,
            "first_downstream_consumer": first_downstream,
            "protocol_stage_order": "UNKNOWN",
            "framing": "UNKNOWN",
            "sequence": "UNKNOWN",
            "compression": "UNKNOWN",
            "encryption": "UNKNOWN",
            "final_binary_egress": "UNKNOWN",
        },
        "negative_controls": {
            "generic_qiodevice_census_used_as_proof": False,
            "generic_qbuffer_census_used_as_proof": False,
            "vtable_adjacency_used_as_temporal_proof": False,
            "historical_final_socket_run_used_as_proof": False,
            "direct_dualconnection_writer_ownership_assumed": False,
        },
        "semantic_result": "TARGETED_PROCESSOR_FLOW_CAPTURED",
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.output_text.write_text("\n".join([
        "P2_DOWNSTREAM_RESULT=TARGETED_PROCESSOR_FLOW_CAPTURED",
        f"CLIENT_SHA256={digest}",
        f"CLIENT_SIZE={EXPECTED_SIZE}",
        "TPROTOCOLWRITER_SLOT_BOUNDARY=PROVEN_SLOT4_ZERO",
        "CONNECTION_INVOKER_EDGE=PROVEN",
        f"EXACT_PROCESSOR_GRAPH_SIGNAL={'true' if exact_processor_graph_signal else 'false'}",
        f"CONCRETE_BYTE_TYPE_SIGNAL={'true' if concrete_byte_type_signal else 'false'}",
        f"FIRST_DOWNSTREAM_CONSUMER={first_downstream}",
        "PROTOCOL_STAGE_ORDER=UNKNOWN",
        "PROTOCOL_FRAMING=UNKNOWN",
        "SEQUENCE=UNKNOWN",
        "COMPRESSION=UNKNOWN",
        "ENCRYPTION=UNKNOWN",
        "FINAL_BINARY_EGRESS=UNKNOWN",
    ]) + "\n", encoding="utf-8")

    lines = [
        "# Corrected TProtocolWriter vtable boundary",
        json.dumps(writer_slots, indent=2),
        "",
        "# Exact connection edge 0x19716a3",
        *connection_lines,
    ]
    for name, body in bodies.items():
        lines.extend(["", f"# {name} {body['start']}..{body['stop']}", *body["relevant"]])
    args.evidence.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("P2_DOWNSTREAM_COMPLETE=true")
    print("P2_DOWNSTREAM_RESULT=TARGETED_PROCESSOR_FLOW_CAPTURED")
    print("P2_DOWNSTREAM_TPROTOCOLWRITER_SLOT_BOUNDARY=PROVEN_SLOT4_ZERO")
    print("P2_DOWNSTREAM_CONNECTION_INVOKER_EDGE=PROVEN")
    print(f"P2_DOWNSTREAM_FIRST_DOWNSTREAM_CONSUMER={first_downstream}")
    print("P2_DOWNSTREAM_PROTOCOL_STAGE_ORDER=UNKNOWN")
    print("P2_DOWNSTREAM_FINAL_BINARY_EGRESS=UNKNOWN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
