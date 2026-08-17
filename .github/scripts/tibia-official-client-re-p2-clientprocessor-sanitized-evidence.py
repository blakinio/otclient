#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import subprocess
import tempfile
from pathlib import Path

EXPECTED_VERSION = "15.32.df7b29"
EXPECTED_SIZE = 51965216
EXPECTED_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"

CLIENT_PROCESSOR_AP = 0x02F6A208
CLIENT_PROCESSOR_ENTRY = 0x00C2DF80
RAW_PROCESSOR_AP = 0x02F6A230
RAW_PROCESSOR_ENTRY = 0x00B47130

WINDOWS = {
    "setup_graph": (0x01970C80, 0x019716C0),
    "invoker": (0x007DD630, 0x007DD720),
    "client_processor": (0x00C2DF80, 0x00C2E080),
    "raw_processor": (0x00B47130, 0x00B47320),
}


class Elf64:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = path.read_bytes()
        require(self.data[:4] == b"\x7fELF", "elf_magic")
        require(self.data[4] == 2 and self.data[5] == 1, "elf64_little_endian")
        phoff = struct.unpack_from("<Q", self.data, 32)[0]
        phentsize = struct.unpack_from("<H", self.data, 54)[0]
        phnum = struct.unpack_from("<H", self.data, 56)[0]
        self.loads: list[tuple[int, int, int]] = []
        for index in range(phnum):
            off = phoff + index * phentsize
            p_type, _flags, p_offset, p_vaddr, _paddr, p_filesz, p_memsz, _align = struct.unpack_from(
                "<IIQQQQQQ", self.data, off
            )
            if p_type == 1 and p_filesz:
                self.loads.append((p_vaddr, min(p_memsz, p_filesz), p_offset))
        require(bool(self.loads), "load_segments")

    def file_offset(self, va: int, size: int = 1) -> int:
        for vaddr, memsz, offset in self.loads:
            if vaddr <= va and va + size <= vaddr + memsz:
                result = offset + (va - vaddr)
                require(result + size <= len(self.data), f"file_backed_{va:x}")
                return result
        raise ValueError(f"unmapped VA 0x{va:x}")

    def read(self, va: int, size: int) -> bytes:
        off = self.file_offset(va, size)
        return self.data[off : off + size]

    def u64(self, va: int) -> int:
        return struct.unpack("<Q", self.read(va, 8))[0]


def require(value: bool, marker: str) -> None:
    if not value:
        raise SystemExit(f"P2_CLIENTPROCESSOR_FAIL={marker}")
    print(f"P2_CLIENTPROCESSOR_OK={marker}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_mode(args: argparse.Namespace) -> int:
    client = args.client
    require(client.is_file() and not client.is_symlink(), "source_regular_file")
    require(client.stat().st_size == EXPECTED_SIZE, "exact_client_size")
    digest = sha256(client)
    require(digest == EXPECTED_SHA256, "exact_client_sha256")
    elf = Elf64(client)

    windows: dict[str, dict[str, object]] = {}
    total_bytes = 0
    for name, (start, stop) in WINDOWS.items():
        payload = elf.read(start, stop - start)
        total_bytes += len(payload)
        windows[name] = {
            "start_address": f"0x{start:08x}",
            "stop_address": f"0x{stop:08x}",
            "byte_count": len(payload),
            "bytes_hex": payload.hex(),
        }

    vtable_words: dict[str, dict[str, str]] = {}
    for name, ap in (("client_processor", CLIENT_PROCESSOR_AP), ("raw_processor", RAW_PROCESSOR_AP)):
        words: dict[str, str] = {}
        for rel in (-0x10, -0x08, 0x00, 0x08, 0x10, 0x18, 0x20, 0x28):
            words[f"{rel:+#x}"] = f"0x{elf.u64(ap + rel):016x}"
        vtable_words[name] = {
            "address_point": f"0x{ap:08x}",
            **words,
        }

    result = {
        "schema": "track-a-p2-clientprocessor-sanitized-source-v1",
        "task_id": "OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence",
        "consumer_pr": 310,
        "client": {
            "version": EXPECTED_VERSION,
            "size": EXPECTED_SIZE,
            "sha256": digest,
            "source_candidate_index": args.candidate_index,
        },
        "policy": {
            "runtime_access": "none",
            "client_executed": False,
            "client_process_accessed": False,
            "process_memory_accessed": False,
            "canonical_state_accessed": False,
            "x11_vnc_accessed": False,
            "login_session_accessed": False,
            "gameplay_accessed": False,
            "client_bytes_mutated": False,
            "raw_client_uploaded": False,
            "source_disassembly_performed": False,
            "source_semantic_classification_performed": False,
            "owner_funded_ai_api_used": False,
            "bounded_sanitized_output_only": True,
        },
        "requested_setup_subset": {
            "start": "0x01970c80",
            "stop": "0x019710b5",
            "contained_in_setup_graph": True,
        },
        "code_window_raw_bytes": total_bytes,
        "code_windows": windows,
        "vtable_words": vtable_words,
        "hosted_disassembly_required": True,
    }

    out = args.outdir
    out.mkdir(parents=True, exist_ok=True)
    (out / "source-evidence.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "source-fence.txt").write_text(
        "\n".join(
            [
                f"P2_CLIENTPROCESSOR_CLIENT_VERSION={EXPECTED_VERSION}",
                f"P2_CLIENTPROCESSOR_CLIENT_SIZE={EXPECTED_SIZE}",
                f"P2_CLIENTPROCESSOR_CLIENT_SHA256={digest}",
                "P2_CLIENTPROCESSOR_RUNTIME_ACCESS=none",
                "P2_CLIENTPROCESSOR_CLIENT_EXECUTED=false",
                "P2_CLIENTPROCESSOR_PROCESS_MEMORY_ACCESSED=false",
                "P2_CLIENTPROCESSOR_CANONICAL_STATE_ACCESSED=false",
                "P2_CLIENTPROCESSOR_SOURCE_DISASSEMBLY=false",
                "P2_CLIENTPROCESSOR_SOURCE_SEMANTIC_CLASSIFICATION=false",
                "P2_CLIENTPROCESSOR_RAW_CLIENT_UPLOADED=false",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"P2_CLIENTPROCESSOR_SOURCE_WINDOW_BYTES={total_bytes}")
    print("P2_CLIENTPROCESSOR_SOURCE_SANITIZED=true")
    return 0


def disassemble_blob(start: int, data: bytes) -> str:
    with tempfile.NamedTemporaryFile() as handle:
        handle.write(data)
        handle.flush()
        proc = subprocess.run(
            [
                "objdump",
                "-D",
                "-b",
                "binary",
                "-m",
                "i386:x86-64",
                "-Mintel",
                "--no-show-raw-insn",
                f"--adjust-vma=0x{start:x}",
                handle.name,
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )
    return proc.stdout


def instruction_map(text: str) -> dict[int, str]:
    result: dict[int, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\s*([0-9a-f]+):\s*(.*)$", line, re.I)
        if match:
            result[int(match.group(1), 16)] = match.group(2).strip()
    return result


def at(insns: dict[int, str], address: int, *needles: str) -> bool:
    line = insns.get(address, "").lower()
    return bool(line) and all(needle.lower() in line for needle in needles)


def lines_with(insns: dict[int, str], *needles: str) -> list[str]:
    out: list[str] = []
    for address, line in sorted(insns.items()):
        lowered = line.lower()
        if all(needle.lower() in lowered for needle in needles):
            out.append(f"{address:08x}: {line}")
    return out


def hosted_mode(args: argparse.Namespace) -> int:
    bundle = args.bundle_dir
    source_path = bundle / "source-evidence.json"
    fence_path = bundle / "source-fence.txt"
    require(source_path.is_file() and fence_path.is_file(), "source_bundle_present")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    require(source.get("schema") == "track-a-p2-clientprocessor-sanitized-source-v1", "source_schema")
    client = source["client"]
    require(client["version"] == EXPECTED_VERSION, "bundle_client_version")
    require(client["size"] == EXPECTED_SIZE, "bundle_client_size")
    require(client["sha256"] == EXPECTED_SHA256, "bundle_client_sha256")
    policy = source["policy"]
    for key in (
        "client_executed",
        "client_process_accessed",
        "process_memory_accessed",
        "canonical_state_accessed",
        "x11_vnc_accessed",
        "login_session_accessed",
        "gameplay_accessed",
        "client_bytes_mutated",
        "raw_client_uploaded",
        "source_disassembly_performed",
        "source_semantic_classification_performed",
        "owner_funded_ai_api_used",
    ):
        require(policy[key] is False, f"policy_{key}_false")
    require(policy["runtime_access"] == "none", "policy_runtime_access_none")
    require(policy["bounded_sanitized_output_only"] is True, "policy_bounded_output")

    decoded: dict[str, str] = {}
    maps: dict[str, dict[int, str]] = {}
    for name, spec in source["code_windows"].items():
        start = int(spec["start_address"], 16)
        stop = int(spec["stop_address"], 16)
        data = bytes.fromhex(spec["bytes_hex"])
        require(len(data) == spec["byte_count"] == stop - start, f"window_size_{name}")
        text = disassemble_blob(start, data)
        decoded[name] = text
        maps[name] = instruction_map(text)

    setup = maps["setup_graph"]
    inv = maps["invoker"]
    cp = maps["client_processor"]
    raw = maps["raw_processor"]

    # Missing load-bearing identity link from PR #310: exact persistent-QBuffer scratch
    # is reloaded and stored at allocation+0x28 while the actual processor object is
    # allocation+0x10, therefore object this+0x18 receives the same pointer.
    setup_checks = {
        "persistent_qbuffer_object_pointer": at(setup, 0x01970C96, "lea", "r15,[rax+0x10]"),
        "persistent_qbuffer_saved_scratch": at(setup, 0x01970CA6, "[rbp-0x218]", "r15"),
        "client_processor_actual_object_pointer": at(setup, 0x0197104F, "lea", "rdx,[rax+0x10]"),
        "client_processor_ap_loaded": at(setup, 0x01971056, "2f6a208"),
        "client_processor_vptr_store": at(setup, 0x0197105D, "[rax+0x10]", "rcx"),
        "same_qbuffer_reloaded": at(setup, 0x01971084, "rsi", "[rbp-0x218]"),
        "same_qbuffer_stored_object_plus18": at(setup, 0x0197108F, "[rax+0x28]", "rsi"),
        "outer_retains_client_processor": at(setup, 0x019710A7, "[rcx+0xa00]", "rdx"),
    }
    for name, value in setup_checks.items():
        require(value, f"setup_{name}")

    words = source["vtable_words"]
    require(int(words["client_processor"]["+0x10"], 16) == CLIENT_PROCESSOR_ENTRY, "client_processor_vslot_10")
    require(int(words["raw_processor"]["+0x10"], 16) == RAW_PROCESSOR_ENTRY, "raw_processor_vslot_10")

    invoker_checks = {
        "message_object_is_rsp": at(inv, 0x007DD66C, "mov", "rbp,rsp"),
        "message_to_client_sret": at(inv, 0x007DD672, "rdi,rbp"),
        "client_outer_a00": at(inv, 0x007DD675, "rsi", "[rax+0xa00]"),
        "client_virtual_plus10": at(inv, 0x007DD67F, "call", "[rax+0x10]"),
        "same_message_to_raw": at(inv, 0x007DD686, "rsi,rbp"),
        "raw_outer_a10": at(inv, 0x007DD689, "rdi", "[rax+0xa10]"),
        "raw_virtual_plus10": at(inv, 0x007DD693, "call", "[rax+0x10]"),
        "same_message_to_dual80": at(inv, 0x007DD69A, "rsi,rbp"),
        "dual80_outer_c18": at(inv, 0x007DD69D, "rdi", "[rax+0xc18]"),
        "dual_virtual_plus80": at(inv, 0x007DD6A7, "call", "[rax+0x80]"),
        "same_message_to_dual78": at(inv, 0x007DD6B1, "rsi,rbp"),
        "dual78_outer_c18": at(inv, 0x007DD6B4, "rdi", "[rax+0xc18]"),
        "dual_virtual_plus78": at(inv, 0x007DD6BE, "call", "[rax+0x78]"),
    }
    for name, value in invoker_checks.items():
        require(value, f"invoker_{name}")

    client_checks = {
        "reads_object_plus18": at(cp, 0x00C2DFA5, "rdi", "[rbp+0x18]"),
        "qiodevice_readall_target": at(cp, 0x00C2DFD5, "call", "4ded50"),
        "output_qbytearray_field": at(cp, 0x00C2DFEB, "lea", "rbp,[rbx+0x8]"),
        "qbytearray_assignment_target": at(cp, 0x00C2E012, "call", "4dd3a0"),
    }
    for name, value in client_checks.items():
        require(value, f"client_{name}")

    raw_checks = {
        "message_qbytearray_pointer": at(raw, 0x00B47132, "lea", "rax,[rsi+0x8]"),
        "qbytearray_insert_target": at(raw, 0x00B47189, "call", "4de730"),
        "qbytearray_append_target": at(raw, 0x00B47206, "call", "4df070"),
        "qbytearray_assign_in_place_target": at(raw, 0x00B47300, "call", "4dd3a0"),
    }
    for name, value in raw_checks.items():
        require(value, f"raw_{name}")

    ap_mentions = {
        "client_processor_ap": lines_with(setup, "2f6a208"),
        "raw_processor_ap": lines_with(setup, "2f6a230"),
        "outer_a00": lines_with(setup, "+0xa00"),
        "outer_a10": lines_with(setup, "+0xa10"),
        "outer_c18": lines_with(setup, "+0xc18"),
    }

    result = {
        "schema": "track-a-p2-clientprocessor-sanitized-final-v1",
        "consumer_pr": 310,
        "source_task": source["task_id"],
        "exact_client": {
            "version": EXPECTED_VERSION,
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
        },
        "checks": {
            "setup_identity": setup_checks,
            "invoker_same_message": invoker_checks,
            "client_processor": client_checks,
            "raw_processor": raw_checks,
        },
        "vtable_words": words,
        "setup_anchor_mentions": ap_mentions,
        "classification": {
            "persistent_qbuffer_to_clientprocessor_this_plus_0x18": "PROVEN",
            "clientprocessor_vslot_plus_0x10_entry": "PROVEN:0x00c2df80",
            "clientprocessor_direct_qiodevice_readall": "PROVEN",
            "same_stack_message_stage_slot_order": "PROVEN",
            "rawprocessor_vslot_plus_0x10_entry": "PROVEN:0x00b47130",
            "rawprocessor_inplace_qbytearray_transform": "PROVEN",
            "typed_protocol_stage_order": "PROVEN_PARTIAL",
            "framing": "UNKNOWN",
            "sequence": "UNKNOWN",
            "compression": "UNKNOWN",
            "encryption": "UNKNOWN",
            "final_binary_egress": "UNKNOWN",
            "final_socket_ownership": "UNKNOWN",
        },
        "negative_controls": {
            "generic_qt_census_used_as_proof": False,
            "vtable_adjacency_used_as_temporal_order": False,
            "quarantined_run_31944051248_used_as_proof": False,
            "historical_final_socket_evidence_used_as_proof": False,
            "rawprocessor_labeled_framing_compression_or_encryption": False,
            "dual_slots_labeled_final_egress": False,
        },
    }

    out = args.outdir
    out.mkdir(parents=True, exist_ok=True)
    (out / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    evidence_lines: list[str] = []
    for name in ("setup_graph", "invoker", "client_processor", "raw_processor"):
        evidence_lines.extend([f"# {name}", decoded[name].rstrip(), ""])
    (out / "evidence.txt").write_text("\n".join(evidence_lines), encoding="utf-8")
    (out / "hosted-validation.txt").write_text(
        "\n".join(
            [
                "P2_CLIENTPROCESSOR_HOSTED_VALIDATION=PASS",
                f"P2_CLIENTPROCESSOR_CLIENT_VERSION={EXPECTED_VERSION}",
                f"P2_CLIENTPROCESSOR_CLIENT_SIZE={EXPECTED_SIZE}",
                f"P2_CLIENTPROCESSOR_CLIENT_SHA256={EXPECTED_SHA256}",
                "P2_CLIENTPROCESSOR_PERSISTENT_QBUFFER_IDENTITY=PROVEN",
                "P2_CLIENTPROCESSOR_DIRECT_READALL=PROVEN",
                "P2_CLIENTPROCESSOR_SAME_MESSAGE_STAGE_ORDER=PROVEN",
                "P2_CLIENTPROCESSOR_RAW_TRANSFORM=PROVEN",
                "P2_CLIENTPROCESSOR_TYPED_PROTOCOL_STAGE_ORDER=PROVEN_PARTIAL",
                "P2_CLIENTPROCESSOR_FRAMING=UNKNOWN",
                "P2_CLIENTPROCESSOR_SEQUENCE=UNKNOWN",
                "P2_CLIENTPROCESSOR_COMPRESSION=UNKNOWN",
                "P2_CLIENTPROCESSOR_ENCRYPTION=UNKNOWN",
                "P2_CLIENTPROCESSOR_FINAL_BINARY_EGRESS=UNKNOWN",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print("P2_CLIENTPROCESSOR_HOSTED_VALIDATION=PASS")
    print("P2_CLIENTPROCESSOR_RESULT=OBJECT_IDENTITY_GAP_CLOSED")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    source = sub.add_parser("source")
    source.add_argument("--client", type=Path, required=True)
    source.add_argument("--candidate-index", type=int, required=True)
    source.add_argument("--outdir", type=Path, required=True)
    hosted = sub.add_parser("hosted")
    hosted.add_argument("--bundle-dir", type=Path, required=True)
    hosted.add_argument("--outdir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "source":
        return source_mode(args)
    return hosted_mode(args)


if __name__ == "__main__":
    raise SystemExit(main())
