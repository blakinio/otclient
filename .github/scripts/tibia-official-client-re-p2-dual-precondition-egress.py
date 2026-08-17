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

WINDOWS = {
    "dual_precondition": (0xB40370, 0xB40880),
    "dual_entry_78": (0xB56970, 0xB56D60),
    "dual_entry_80": (0xB56D60, 0xB57280),
}

EXPECTED_ANCHORS = {
    "dual_precondition": {
        0xB40643: ("call", "[rax+0x78]"),
        0xB40656: ("call", "4dac00"),
        0xB4066B: ("call", "4de370"),
        0xB406BB: ("call", "4dda80"),
        0xB40714: ("call", "4ded50"),
        0xB40735: ("call", "[rax+0x10]"),
    },
    "dual_entry_78": {
        0xB56AF5: ("call", "4def50"),
        0xB56BC8: ("call", "4def50"),
        0xB56C93: ("call", "[rax+0x10]"),
    },
    "dual_entry_80": {
        0xB56EC8: ("call", "4def50"),
        0xB56F80: ("call", "4def50"),
        0xB57042: ("call", "[rdx+0x10]"),
    },
}


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise SystemExit(f"P2_DUAL_EGRESS_FAIL={marker}")
    print(f"P2_DUAL_EGRESS_OK={marker}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_load_segments(path: Path) -> list[dict[str, int]]:
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
        segments: list[dict[str, int]] = []
        for index in range(phnum):
            handle.seek(phoff + index * phentsize)
            row = handle.read(56)
            require(len(row) == 56, f"program_header_{index}_complete")
            p_type, p_flags, p_offset, p_vaddr, _p_paddr, p_filesz, p_memsz, p_align = struct.unpack(
                "<IIQQQQQQ", row
            )
            if p_type == 1:
                segments.append(
                    {
                        "flags": p_flags,
                        "offset": p_offset,
                        "vaddr": p_vaddr,
                        "filesz": p_filesz,
                        "memsz": p_memsz,
                        "align": p_align,
                    }
                )
        require(bool(segments), "load_segments_present")
        return segments


def read_va_range(path: Path, segments: list[dict[str, int]], start: int, end: int) -> bytes:
    require(end > start, f"range_order_{start:x}")
    for segment in segments:
        lo = segment["vaddr"]
        hi = lo + segment["filesz"]
        if start >= lo and end <= hi:
            offset = segment["offset"] + (start - lo)
            with path.open("rb") as handle:
                handle.seek(offset)
                data = handle.read(end - start)
            require(len(data) == end - start, f"range_complete_{start:x}")
            return data
    raise SystemExit(f"P2_DUAL_EGRESS_FAIL=range_not_file_backed_{start:x}_{end:x}")


def source_mode(args: argparse.Namespace) -> int:
    client = args.client.resolve()
    require(client.is_file(), "source_regular_file")
    require(not client.is_symlink(), "source_not_symlink")
    mode = client.stat().st_mode
    require(stat.S_ISREG(mode), "source_mode_regular")
    require(client.stat().st_size == EXPECTED_SIZE, "source_exact_size")
    require(sha256_file(client) == EXPECTED_SHA256, "source_exact_sha256")

    segments = parse_load_segments(client)
    windows: dict[str, dict[str, object]] = {}
    for name, (start, end) in WINDOWS.items():
        data = read_va_range(client, segments, start, end)
        windows[name] = {
            "start": start,
            "end": end,
            "length": len(data),
            "sha256": sha256_bytes(data),
            "hex": data.hex(),
        }

    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "track-a-p2-dual-egress-source-v1",
        "exact_client": {
            "version": EXPECTED_VERSION,
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
            "platform": "official_native_linux_only",
        },
        "source_candidate_index": args.candidate_index,
        "source_operation": "bounded_file_byte_mapping_only",
        "runtime_access": "none",
        "client_process_accessed": False,
        "process_memory_accessed": False,
        "canonical_state_accessed": False,
        "client_executed": False,
        "client_byte_mutated": False,
        "source_disassembly": False,
        "source_semantic_classification": False,
        "raw_client_uploaded": False,
        "windows": windows,
    }
    (outdir / "source-evidence.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    (outdir / "source-fence.txt").write_text(
        "\n".join(
            [
                f"P2_DUAL_EGRESS_CLIENT_VERSION={EXPECTED_VERSION}",
                f"P2_DUAL_EGRESS_CLIENT_SIZE={EXPECTED_SIZE}",
                f"P2_DUAL_EGRESS_CLIENT_SHA256={EXPECTED_SHA256}",
                "P2_DUAL_EGRESS_RUNTIME_ACCESS=none",
                "P2_DUAL_EGRESS_SOURCE_OPERATION=bounded_file_byte_mapping_only",
                "P2_DUAL_EGRESS_CLIENT_PROCESS_ACCESSED=false",
                "P2_DUAL_EGRESS_PROCESS_MEMORY_ACCESSED=false",
                "P2_DUAL_EGRESS_CANONICAL_STATE_ACCESSED=false",
                "P2_DUAL_EGRESS_CLIENT_EXECUTED=false",
                "P2_DUAL_EGRESS_CLIENT_BYTE_MUTATED=false",
                "P2_DUAL_EGRESS_SOURCE_DISASSEMBLY=false",
                "P2_DUAL_EGRESS_SOURCE_SEMANTIC_CLASSIFICATION=false",
                "P2_DUAL_EGRESS_RAW_CLIENT_UPLOADED=false",
                "",
            ]
        )
    )
    print("P2_DUAL_EGRESS_SOURCE=PASS")
    return 0


def disassemble(name: str, start: int, data: bytes) -> str:
    with tempfile.TemporaryDirectory(prefix=f"p2-{name}-") as tempdir:
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


def instruction_map(disassembly: str) -> dict[int, str]:
    result: dict[int, str] = {}
    for line in disassembly.splitlines():
        match = re.match(r"^\s*([0-9a-fA-F]+):\s+(?:[0-9a-fA-F]{2}\s+)+\s*(.*?)\s*$", line)
        if match:
            result[int(match.group(1), 16)] = match.group(2)
    return result


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

    disassemblies: dict[str, str] = {}
    anchors: dict[str, dict[str, str]] = {}
    for name, (start, end) in WINDOWS.items():
        record = bundle["windows"][name]
        require(record["start"] == start and record["end"] == end, f"{name}_range")
        data = bytes.fromhex(record["hex"])
        require(len(data) == end - start, f"{name}_length")
        require(sha256_bytes(data) == record["sha256"], f"{name}_digest")
        disassembly = disassemble(name, start, data)
        disassemblies[name] = disassembly
        instructions = instruction_map(disassembly)
        anchors[name] = {}
        for address, needles in EXPECTED_ANCHORS[name].items():
            instruction = instructions.get(address, "")
            normalized = instruction.lower().replace(" ", "")
            for needle in needles:
                require(needle.lower().replace(" ", "") in normalized, f"{name}_anchor_{address:x}_{needle}")
            anchors[name][f"0x{address:x}"] = instruction

    combined = []
    for name in WINDOWS:
        start, end = WINDOWS[name]
        combined.append(f"## {name} 0x{start:x}..0x{end:x}\n")
        combined.append(disassemblies[name])
        combined.append("\n")
    (outdir / "disassembly.txt").write_text("".join(combined))

    result = {
        "schema": "track-a-p2-dual-egress-hosted-v1",
        "exact_client": fence,
        "execution_class": "github_hosted",
        "runtime_access": "none",
        "primary_bytes_exact_fenced": True,
        "anchors": anchors,
        "semantic_classification": {
            "qiodevice_write_at_0xb4066b": "FACT_CALLSITE_ONLY",
            "qiodevice_receiver_identity": "UNKNOWN_PENDING_PRIMARY_DISASSEMBLY_REVIEW",
            "payload_relationship_to_promoted_same_message": "UNKNOWN_PENDING_PRIMARY_DISASSEMBLY_REVIEW",
            "final_binary_egress": "UNKNOWN",
            "final_socket_ownership": "UNKNOWN",
            "framing": "UNKNOWN",
            "sequence": "UNKNOWN",
            "compression": "UNKNOWN",
            "encryption": "UNKNOWN",
        },
        "negative_controls": {
            "b46bd0_gameplay_binary_sink": "DISPROVEN",
            "c33259_gameplay_sink": "DISPROVEN",
            "b5b880_gameplay_endpoint": "SUPERSEDED",
            "quarantined_run_31944051248_used_as_proof": False,
        },
    }
    (outdir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (outdir / "hosted-validation.txt").write_text(
        "\n".join(
            [
                "P2_DUAL_EGRESS_HOSTED_VALIDATION=PASS",
                f"P2_DUAL_EGRESS_CLIENT_VERSION={EXPECTED_VERSION}",
                f"P2_DUAL_EGRESS_CLIENT_SIZE={EXPECTED_SIZE}",
                f"P2_DUAL_EGRESS_CLIENT_SHA256={EXPECTED_SHA256}",
                "P2_DUAL_EGRESS_EXECUTION_CLASS=github_hosted",
                "P2_DUAL_EGRESS_RUNTIME_ACCESS=none",
                "P2_DUAL_EGRESS_PRIMARY_BYTES_EXACT_FENCED=true",
                "P2_DUAL_EGRESS_QIODEVICE_WRITE_CALLSITE=FACT_CALLSITE_ONLY",
                "P2_DUAL_EGRESS_QIODEVICE_RECEIVER=UNKNOWN_PENDING_PRIMARY_DISASSEMBLY_REVIEW",
                "P2_DUAL_EGRESS_FINAL_BINARY_EGRESS=UNKNOWN",
                "P2_DUAL_EGRESS_FINAL_SOCKET_OWNERSHIP=UNKNOWN",
                "P2_DUAL_EGRESS_FRAMING=UNKNOWN",
                "P2_DUAL_EGRESS_SEQUENCE=UNKNOWN",
                "P2_DUAL_EGRESS_COMPRESSION=UNKNOWN",
                "P2_DUAL_EGRESS_ENCRYPTION=UNKNOWN",
                "",
            ]
        )
    )
    print("P2_DUAL_EGRESS_HOSTED=PASS")
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
