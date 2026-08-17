#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import struct
import subprocess
import tempfile
from pathlib import Path

EXPECTED_VERSION = "15.32.df7b29"
EXPECTED_SIZE = 51965216
EXPECTED_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"

# These are exact structural anchors already present in accepted evidence.
TARGET_SLOTS = {
    "outer_guard_b3eda0_plus98": (0xB3EDA0, 0x98),
    "outer_guard_b3ed90_plus78": (0xB3ED90, 0x78),
    "intermediate_guard_f45cf0_plus60": (0xF45CF0, 0x60),
    "historical_b40630_plus10": (0xB40630, 0x10),
    "plus80_guard_b57470_plus80": (0xB57470, 0x80),
}

FIXED_CODE_WINDOWS = {
    "dual78_surviving_chain": (0xB56C40, 0xB56D48),
    "outer_guard_methods": (0xB3ED40, 0xB3EE80),
    "intermediate_guard_method": (0xF45C70, 0xF45E20),
    "historical_b40630_method": (0xB405F0, 0xB407A0),
    "plus80_guard_method": (0xB573F0, 0xB57540),
}

MAX_POINTER_OCCURRENCES = 64
MAX_XREFS_PER_CANDIDATE = 32
MAX_TOTAL_XREF_WINDOWS = 96
TABLE_BEFORE = 0x10
TABLE_AFTER = 0xD0
XREF_BEFORE = 0x70
XREF_AFTER = 0xB0


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise SystemExit(f"P2_NESTED_VCALL_FAIL={marker}")
    print(f"P2_NESTED_VCALL_OK={marker}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class Elf64:
    def __init__(self, path: Path) -> None:
        self.path = path
        with path.open("rb") as handle:
            ident = handle.read(16)
            require(ident[:4] == b"\x7fELF", "elf_magic")
            require(ident[4] == 2, "elf64")
            require(ident[5] == 1, "elf_little_endian")
            rest = handle.read(48)
            require(len(rest) == 48, "elf_header_complete")
            (
                _etype,
                _machine,
                _version,
                _entry,
                phoff,
                _shoff,
                _flags,
                _ehsize,
                phentsize,
                phnum,
                _shentsize,
                _shnum,
                _shstrndx,
            ) = struct.unpack("<HHIQQQIHHHHHH", rest)
            require(phentsize >= 56, "program_header_size")
            require(0 < phnum < 128, "program_header_count")
            self.loads: list[dict[str, int]] = []
            for index in range(phnum):
                handle.seek(phoff + index * phentsize)
                row = handle.read(56)
                require(len(row) == 56, f"program_header_{index}_complete")
                p_type, p_flags, p_offset, p_vaddr, _paddr, p_filesz, p_memsz, p_align = struct.unpack(
                    "<IIQQQQQQ", row
                )
                if p_type == 1 and p_filesz:
                    self.loads.append(
                        {
                            "flags": p_flags,
                            "offset": p_offset,
                            "vaddr": p_vaddr,
                            "filesz": p_filesz,
                            "memsz": p_memsz,
                            "align": p_align,
                        }
                    )
        require(bool(self.loads), "load_segments_present")

    def segment_for(self, va: int, size: int = 1) -> dict[str, int] | None:
        for segment in self.loads:
            lo = segment["vaddr"]
            hi = lo + segment["filesz"]
            if va >= lo and va + size <= hi:
                return segment
        return None

    def read(self, va: int, size: int) -> bytes:
        segment = self.segment_for(va, size)
        if segment is None:
            raise ValueError(f"unmapped file-backed VA 0x{va:x}+0x{size:x}")
        offset = segment["offset"] + va - segment["vaddr"]
        with self.path.open("rb") as handle:
            handle.seek(offset)
            data = handle.read(size)
        require(len(data) == size, f"read_complete_{va:x}_{size:x}")
        return data

    def u64(self, va: int) -> int:
        return struct.unpack("<Q", self.read(va, 8))[0]

    def iter_segment_bytes(self):
        with self.path.open("rb") as handle:
            for segment in self.loads:
                handle.seek(segment["offset"])
                data = handle.read(segment["filesz"])
                require(len(data) == segment["filesz"], f"segment_complete_{segment['vaddr']:x}")
                yield segment, data


def window_record(elf: Elf64, start: int, end: int) -> dict[str, object]:
    require(end > start, f"window_order_{start:x}")
    data = elf.read(start, end - start)
    return {
        "start": start,
        "end": end,
        "length": len(data),
        "sha256": sha256_bytes(data),
        "hex": data.hex(),
    }


def bounded_window_in_segment(elf: Elf64, center: int, before: int, after: int) -> tuple[int, int] | None:
    segment = elf.segment_for(center, 1)
    if segment is None:
        return None
    lo = segment["vaddr"]
    hi = lo + segment["filesz"]
    start = max(lo, center - before)
    end = min(hi, center + after)
    if end <= start:
        return None
    return start, end


def pointer_occurrences(elf: Elf64, value: int) -> list[int]:
    needle = struct.pack("<Q", value)
    hits: list[int] = []
    for segment, data in elf.iter_segment_bytes():
        pos = data.find(needle)
        while pos >= 0:
            hits.append(segment["vaddr"] + pos)
            if len(hits) >= MAX_POINTER_OCCURRENCES:
                return hits
            pos = data.find(needle, pos + 1)
    return hits


def candidate_from_slot(elf: Elf64, occurrence: int, slot: int) -> dict[str, object] | None:
    address_point = occurrence - slot
    if elf.segment_for(address_point - TABLE_BEFORE, TABLE_BEFORE + TABLE_AFTER) is None:
        return None
    table = window_record(elf, address_point - TABLE_BEFORE, address_point + TABLE_AFTER)
    record: dict[str, object] = {
        "pointer_occurrence": occurrence,
        "slot_offset": slot,
        "address_point": address_point,
        "table_window": table,
    }
    try:
        offset_to_top = elf.u64(address_point - 0x10)
        rtti = elf.u64(address_point - 0x8)
        record["offset_to_top_raw"] = offset_to_top
        record["rtti_pointer_raw"] = rtti
        if rtti and elf.segment_for(rtti, 0x18) is not None:
            rtti_end = rtti + min(0x40, elf.segment_for(rtti, 1)["vaddr"] + elf.segment_for(rtti, 1)["filesz"] - rtti)
            record["rtti_window"] = window_record(elf, rtti, rtti_end)
            name_pointer = elf.u64(rtti + 8)
            record["rtti_name_pointer_raw"] = name_pointer
            if name_pointer and elf.segment_for(name_pointer, 1) is not None:
                segment = elf.segment_for(name_pointer, 1)
                max_len = min(256, segment["vaddr"] + segment["filesz"] - name_pointer)
                raw = elf.read(name_pointer, max_len)
                nul = raw.find(b"\x00")
                if nul >= 0:
                    raw = raw[: nul + 1]
                record["rtti_name_bytes"] = {
                    "start": name_pointer,
                    "length": len(raw),
                    "sha256": sha256_bytes(raw),
                    "hex": raw.hex(),
                }
    except (ValueError, struct.error):
        record["rtti_followup_available"] = False
    return record


def structural_rip_xrefs(elf: Elf64, targets: set[int]) -> dict[int, list[int]]:
    hits: dict[int, list[int]] = {target: [] for target in targets}
    for segment, data in elf.iter_segment_bytes():
        if not (segment["flags"] & 1):
            continue
        base = segment["vaddr"]
        i = 0
        while i + 7 <= len(data):
            # Structural byte-index only: REX + LEA/MOV r64,[RIP+disp32].
            rex = data[i]
            opcode = data[i + 1]
            modrm = data[i + 2]
            if 0x40 <= rex <= 0x4F and opcode in (0x8D, 0x8B) and (modrm & 0xC7) == 0x05:
                disp = struct.unpack_from("<i", data, i + 3)[0]
                insn_va = base + i
                target = insn_va + 7 + disp
                if target in hits and len(hits[target]) < MAX_XREFS_PER_CANDIDATE:
                    hits[target].append(insn_va)
                i += 7
                continue
            i += 1
    return hits


def source_mode(args: argparse.Namespace) -> int:
    client = args.client.resolve()
    require(client.is_file(), "source_regular_file")
    require(not client.is_symlink(), "source_not_symlink")
    require(stat.S_ISREG(client.stat().st_mode), "source_mode_regular")
    require(client.stat().st_size == EXPECTED_SIZE, "source_exact_size")
    require(sha256_file(client) == EXPECTED_SHA256, "source_exact_sha256")
    elf = Elf64(client)

    fixed_windows = {
        name: window_record(elf, start, end)
        for name, (start, end) in FIXED_CODE_WINDOWS.items()
    }

    target_records: dict[str, object] = {}
    all_candidate_aps: set[int] = set()
    for name, (target, slot) in TARGET_SLOTS.items():
        occurrences = pointer_occurrences(elf, target)
        candidates = []
        for occurrence in occurrences:
            candidate = candidate_from_slot(elf, occurrence, slot)
            if candidate is not None:
                candidates.append(candidate)
                all_candidate_aps.add(int(candidate["address_point"]))
        target_records[name] = {
            "target": target,
            "slot_offset": slot,
            "pointer_occurrences": occurrences,
            "candidate_tables": candidates,
        }

    raw_xrefs = structural_rip_xrefs(elf, all_candidate_aps)
    xref_windows: list[dict[str, object]] = []
    for target_ap in sorted(raw_xrefs):
        for xref in raw_xrefs[target_ap]:
            if len(xref_windows) >= MAX_TOTAL_XREF_WINDOWS:
                break
            bounds = bounded_window_in_segment(elf, xref, XREF_BEFORE, XREF_AFTER)
            if bounds is None:
                continue
            start, end = bounds
            xref_windows.append(
                {
                    "candidate_address_point": target_ap,
                    "structural_xref_va": xref,
                    "window": window_record(elf, start, end),
                }
            )

    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "track-a-p2-dual-nested-vcall-source-v1",
        "exact_client": {
            "version": EXPECTED_VERSION,
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
            "platform": "official_native_linux_only",
        },
        "source_candidate_index": args.candidate_index,
        "source_operation": "bounded_file_byte_mapping_and_structural_index_only",
        "runtime_access": "none",
        "client_process_accessed": False,
        "process_memory_accessed": False,
        "canonical_state_accessed": False,
        "client_executed": False,
        "client_byte_mutated": False,
        "source_disassembly": False,
        "source_semantic_classification": False,
        "raw_client_uploaded": False,
        "load_segments": [
            {k: segment[k] for k in ("flags", "offset", "vaddr", "filesz", "memsz")}
            for segment in elf.loads
        ],
        "fixed_code_windows": fixed_windows,
        "target_records": target_records,
        "structural_rip_xrefs": {f"0x{k:x}": v for k, v in sorted(raw_xrefs.items())},
        "xref_windows": xref_windows,
    }
    (outdir / "source-evidence.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    (outdir / "source-fence.txt").write_text(
        "\n".join(
            [
                f"P2_NESTED_VCALL_CLIENT_VERSION={EXPECTED_VERSION}",
                f"P2_NESTED_VCALL_CLIENT_SIZE={EXPECTED_SIZE}",
                f"P2_NESTED_VCALL_CLIENT_SHA256={EXPECTED_SHA256}",
                "P2_NESTED_VCALL_RUNTIME_ACCESS=none",
                "P2_NESTED_VCALL_SOURCE_OPERATION=bounded_file_byte_mapping_and_structural_index_only",
                "P2_NESTED_VCALL_CLIENT_PROCESS_ACCESSED=false",
                "P2_NESTED_VCALL_PROCESS_MEMORY_ACCESSED=false",
                "P2_NESTED_VCALL_CANONICAL_STATE_ACCESSED=false",
                "P2_NESTED_VCALL_CLIENT_EXECUTED=false",
                "P2_NESTED_VCALL_CLIENT_BYTE_MUTATED=false",
                "P2_NESTED_VCALL_SOURCE_DISASSEMBLY=false",
                "P2_NESTED_VCALL_SOURCE_SEMANTIC_CLASSIFICATION=false",
                "P2_NESTED_VCALL_RAW_CLIENT_UPLOADED=false",
                "",
            ]
        )
    )
    print("P2_NESTED_VCALL_SOURCE=PASS")
    return 0


def disassemble(name: str, start: int, data: bytes) -> str:
    with tempfile.TemporaryDirectory(prefix=f"p2-nested-{name}-") as tempdir:
        path = Path(tempdir) / f"{name}.bin"
        path.write_bytes(data)
        proc = subprocess.run(
            [
                "objdump",
                "-D",
                "-b",
                "binary",
                "-m",
                "i386:x86-64",
                "-M",
                "intel",
                f"--adjust-vma=0x{start:x}",
                str(path),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return proc.stdout


def decode_record(record: dict[str, object]) -> bytes:
    data = bytes.fromhex(str(record["hex"]))
    require(len(data) == int(record["length"]), f"record_length_{record['start']}")
    require(sha256_bytes(data) == record["sha256"], f"record_digest_{record['start']}")
    return data


def printable_name(candidate: dict[str, object]) -> str:
    entry = candidate.get("rtti_name_bytes")
    if not isinstance(entry, dict):
        return "UNKNOWN"
    raw = decode_record(entry).rstrip(b"\x00")
    return raw.decode("utf-8", errors="replace")


def table_qwords(candidate: dict[str, object]) -> list[tuple[int, int]]:
    table = candidate["table_window"]
    data = decode_record(table)
    start = int(table["start"])
    rows = []
    for offset in range(0, len(data) - 7, 8):
        rows.append((start + offset, struct.unpack_from("<Q", data, offset)[0]))
    return rows


def hosted_mode(args: argparse.Namespace) -> int:
    bundle = json.loads((args.bundle_dir / "source-evidence.json").read_text())
    fence = bundle.get("exact_client", {})
    require(fence.get("version") == EXPECTED_VERSION, "hosted_exact_version")
    require(fence.get("size") == EXPECTED_SIZE, "hosted_exact_size")
    require(fence.get("sha256") == EXPECTED_SHA256, "hosted_exact_sha256")
    require(bundle.get("runtime_access") == "none", "hosted_runtime_none")
    require(bundle.get("raw_client_uploaded") is False, "hosted_raw_client_absent")
    require(bundle.get("source_disassembly") is False, "hosted_source_no_disassembly")
    require(bundle.get("source_semantic_classification") is False, "hosted_source_no_semantics")

    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    disassembly_parts: list[str] = []
    for name, record in bundle["fixed_code_windows"].items():
        data = decode_record(record)
        disassembly_parts.append(f"## fixed {name} 0x{int(record['start']):x}..0x{int(record['end']):x}\n")
        disassembly_parts.append(disassemble(name, int(record["start"]), data))
        disassembly_parts.append("\n")

    for index, item in enumerate(bundle["xref_windows"]):
        record = item["window"]
        data = decode_record(record)
        name = f"xref_{index:03d}"
        disassembly_parts.append(
            f"## {name} candidate_ap=0x{int(item['candidate_address_point']):x} "
            f"xref=0x{int(item['structural_xref_va']):x} "
            f"window=0x{int(record['start']):x}..0x{int(record['end']):x}\n"
        )
        disassembly_parts.append(disassemble(name, int(record["start"]), data))
        disassembly_parts.append("\n")
    (outdir / "disassembly.txt").write_text("".join(disassembly_parts))

    table_lines: list[str] = []
    hosted_candidates: dict[str, list[dict[str, object]]] = {}
    for name, target_record in bundle["target_records"].items():
        rows = []
        table_lines.append(
            f"## {name} target=0x{int(target_record['target']):x} slot=0x{int(target_record['slot_offset']):x}\n"
        )
        for candidate in target_record["candidate_tables"]:
            ap = int(candidate["address_point"])
            rtti_name = printable_name(candidate)
            qwords = table_qwords(candidate)
            rows.append(
                {
                    "address_point": ap,
                    "pointer_occurrence": int(candidate["pointer_occurrence"]),
                    "offset_to_top_raw": candidate.get("offset_to_top_raw"),
                    "rtti_pointer_raw": candidate.get("rtti_pointer_raw"),
                    "rtti_name": rtti_name,
                    "qwords": [{"va": va, "value": value} for va, value in qwords],
                }
            )
            table_lines.append(
                f"candidate_ap=0x{ap:x} occurrence=0x{int(candidate['pointer_occurrence']):x} "
                f"offset_to_top={candidate.get('offset_to_top_raw')} "
                f"rtti=0x{int(candidate.get('rtti_pointer_raw', 0)):x} name={rtti_name!r}\n"
            )
            for va, value in qwords:
                table_lines.append(f"  0x{va:x}: 0x{value:x}\n")
        hosted_candidates[name] = rows
        table_lines.append("\n")
    (outdir / "candidate-tables.txt").write_text("".join(table_lines))

    result = {
        "schema": "track-a-p2-dual-nested-vcall-hosted-v1",
        "exact_client": fence,
        "execution_class": "github_hosted",
        "runtime_access": "none",
        "primary_bytes_exact_fenced": True,
        "candidate_tables": hosted_candidates,
        "structural_rip_xrefs": bundle["structural_rip_xrefs"],
        "xref_window_count": len(bundle["xref_windows"]),
        "semantic_classification": {
            "b56c93_same_message_preserved": "FACT_FROM_ACCEPTED_DATAFLOW",
            "b57042_same_message_preserved": "DISPROVEN_FROM_ACCEPTED_DATAFLOW",
            "b56c93_concrete_target": "PENDING_PRIMARY_HOSTED_REVIEW",
            "b56c93_target_equals_b40630": "PENDING_PRIMARY_HOSTED_REVIEW",
            "final_binary_egress": "UNKNOWN",
            "final_socket_ownership": "UNKNOWN",
            "framing": "UNKNOWN",
            "sequence": "UNKNOWN",
            "compression": "UNKNOWN",
            "encryption": "UNKNOWN",
        },
    }
    (outdir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (outdir / "hosted-validation.txt").write_text(
        "\n".join(
            [
                "P2_NESTED_VCALL_HOSTED_VALIDATION=PASS",
                f"P2_NESTED_VCALL_CLIENT_VERSION={EXPECTED_VERSION}",
                f"P2_NESTED_VCALL_CLIENT_SIZE={EXPECTED_SIZE}",
                f"P2_NESTED_VCALL_CLIENT_SHA256={EXPECTED_SHA256}",
                "P2_NESTED_VCALL_EXECUTION_CLASS=github_hosted",
                "P2_NESTED_VCALL_RUNTIME_ACCESS=none",
                "P2_NESTED_VCALL_PRIMARY_BYTES_EXACT_FENCED=true",
                f"P2_NESTED_VCALL_XREF_WINDOWS={len(bundle['xref_windows'])}",
                "P2_NESTED_VCALL_B56C93_TARGET=PENDING_PRIMARY_HOSTED_REVIEW",
                "",
            ]
        )
    )
    print("P2_NESTED_VCALL_HOSTED=PASS")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    source = sub.add_parser("source")
    source.add_argument("--client", type=Path, required=True)
    source.add_argument("--candidate-index", required=True)
    source.add_argument("--outdir", type=Path, required=True)
    hosted = sub.add_parser("hosted")
    hosted.add_argument("--bundle-dir", type=Path, required=True)
    hosted.add_argument("--outdir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "source":
        return source_mode(args)
    if args.mode == "hosted":
        return hosted_mode(args)
    raise AssertionError(args.mode)


if __name__ == "__main__":
    raise SystemExit(main())
