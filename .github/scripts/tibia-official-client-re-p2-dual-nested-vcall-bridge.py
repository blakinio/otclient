#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import stat
import struct
import subprocess
import tempfile
from pathlib import Path

EXPECTED_VERSION = "15.32.df7b29"
EXPECTED_SIZE = 51965216
EXPECTED_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
START = 0xB4AEA0
END = 0xB4B800


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise SystemExit(f"P2_NESTED_BRIDGE_FAIL={marker}")
    print(f"P2_NESTED_BRIDGE_OK={marker}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_segments(path: Path) -> list[tuple[int, int, int]]:
    with path.open("rb") as f:
        ident = f.read(16)
        require(ident[:4] == b"\x7fELF", "elf_magic")
        require(ident[4] == 2 and ident[5] == 1, "elf64_little")
        rest = f.read(48)
        require(len(rest) == 48, "elf_header_complete")
        fields = struct.unpack("<HHIQQQIHHHHHH", rest)
        phoff = fields[4]
        phentsize = fields[8]
        phnum = fields[9]
        require(phentsize >= 56 and 0 < phnum < 128, "program_headers")
        out: list[tuple[int, int, int]] = []
        for i in range(phnum):
            f.seek(phoff + i * phentsize)
            row = f.read(56)
            require(len(row) == 56, f"ph_{i}_complete")
            p_type, _flags, p_offset, p_vaddr, _paddr, p_filesz, _p_memsz, _align = struct.unpack(
                "<IIQQQQQQ", row
            )
            if p_type == 1 and p_filesz:
                out.append((p_vaddr, p_filesz, p_offset))
        require(bool(out), "load_segments")
        return out


def read_va(path: Path, start: int, end: int) -> bytes:
    require(end > start, "range_order")
    for vaddr, filesz, offset in load_segments(path):
        if start >= vaddr and end <= vaddr + filesz:
            with path.open("rb") as f:
                f.seek(offset + start - vaddr)
                data = f.read(end - start)
            require(len(data) == end - start, "range_complete")
            return data
    raise SystemExit("P2_NESTED_BRIDGE_FAIL=range_not_file_backed")


def source_mode(args: argparse.Namespace) -> int:
    client = args.client.resolve()
    require(client.is_file(), "source_file")
    require(not client.is_symlink(), "source_not_symlink")
    require(stat.S_ISREG(client.stat().st_mode), "source_regular")
    require(client.stat().st_size == EXPECTED_SIZE, "source_exact_size")
    require(sha256_file(client) == EXPECTED_SHA256, "source_exact_sha256")
    data = read_va(client, START, END)

    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "track-a-p2-nested-vcall-bridge-source-v1",
        "exact_client": {
            "version": EXPECTED_VERSION,
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
            "platform": "official_native_linux_only",
        },
        "source_candidate_index": args.candidate_index,
        "runtime_access": "none",
        "source_operation": "single_bounded_file_byte_window_only",
        "source_disassembly": False,
        "source_semantic_classification": False,
        "client_process_accessed": False,
        "process_memory_accessed": False,
        "canonical_state_accessed": False,
        "client_executed": False,
        "client_byte_mutated": False,
        "raw_client_uploaded": False,
        "window": {
            "start": START,
            "end": END,
            "length": len(data),
            "sha256": sha256_bytes(data),
            "hex": data.hex(),
        },
    }
    (outdir / "source-evidence.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    (outdir / "source-fence.txt").write_text(
        "\n".join([
            f"P2_NESTED_BRIDGE_CLIENT_VERSION={EXPECTED_VERSION}",
            f"P2_NESTED_BRIDGE_CLIENT_SIZE={EXPECTED_SIZE}",
            f"P2_NESTED_BRIDGE_CLIENT_SHA256={EXPECTED_SHA256}",
            "P2_NESTED_BRIDGE_RUNTIME_ACCESS=none",
            "P2_NESTED_BRIDGE_SOURCE_OPERATION=single_bounded_file_byte_window_only",
            "P2_NESTED_BRIDGE_SOURCE_DISASSEMBLY=false",
            "P2_NESTED_BRIDGE_SOURCE_SEMANTIC_CLASSIFICATION=false",
            "P2_NESTED_BRIDGE_CLIENT_PROCESS_ACCESSED=false",
            "P2_NESTED_BRIDGE_PROCESS_MEMORY_ACCESSED=false",
            "P2_NESTED_BRIDGE_CANONICAL_STATE_ACCESSED=false",
            "P2_NESTED_BRIDGE_CLIENT_EXECUTED=false",
            "P2_NESTED_BRIDGE_CLIENT_BYTE_MUTATED=false",
            "P2_NESTED_BRIDGE_RAW_CLIENT_UPLOADED=false",
            "",
        ])
    )
    print("P2_NESTED_BRIDGE_SOURCE=PASS")
    return 0


def hosted_mode(args: argparse.Namespace) -> int:
    bundle = json.loads((args.bundle_dir / "source-evidence.json").read_text())
    fence = bundle.get("exact_client", {})
    require(fence.get("version") == EXPECTED_VERSION, "hosted_exact_version")
    require(fence.get("size") == EXPECTED_SIZE, "hosted_exact_size")
    require(fence.get("sha256") == EXPECTED_SHA256, "hosted_exact_sha256")
    require(bundle.get("runtime_access") == "none", "hosted_runtime_none")
    require(bundle.get("raw_client_uploaded") is False, "hosted_raw_absent")
    require(bundle.get("source_disassembly") is False, "hosted_source_no_disassembly")
    require(bundle.get("source_semantic_classification") is False, "hosted_source_no_semantics")
    window = bundle["window"]
    require(window["start"] == START and window["end"] == END, "hosted_exact_range")
    data = bytes.fromhex(window["hex"])
    require(len(data) == END - START, "hosted_window_length")
    require(sha256_bytes(data) == window["sha256"], "hosted_window_digest")

    with tempfile.TemporaryDirectory(prefix="p2-nested-bridge-") as td:
        raw = Path(td) / "bridge.bin"
        raw.write_bytes(data)
        proc = subprocess.run(
            [
                "objdump", "-D", "-b", "binary", "-m", "i386:x86-64", "-M", "intel",
                f"--adjust-vma=0x{START:x}", str(raw),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        disassembly = proc.stdout

    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "disassembly.txt").write_text(disassembly)
    result = {
        "schema": "track-a-p2-nested-vcall-bridge-hosted-v1",
        "exact_client": fence,
        "execution_class": "github_hosted",
        "runtime_access": "none",
        "primary_bytes_exact_fenced": True,
        "window": {"start": START, "end": END, "sha256": window["sha256"]},
        "classification": {
            "rbp_minus_c0_source": "PENDING_PRIMARY_HOSTED_REVIEW",
            "b56c93_receiver_vtable": "PENDING_PRIMARY_HOSTED_REVIEW",
            "b56c93_concrete_plus10_target": "PENDING_PRIMARY_HOSTED_REVIEW",
        },
    }
    (outdir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (outdir / "hosted-validation.txt").write_text(
        "\n".join([
            "P2_NESTED_BRIDGE_HOSTED_VALIDATION=PASS",
            f"P2_NESTED_BRIDGE_CLIENT_VERSION={EXPECTED_VERSION}",
            f"P2_NESTED_BRIDGE_CLIENT_SIZE={EXPECTED_SIZE}",
            f"P2_NESTED_BRIDGE_CLIENT_SHA256={EXPECTED_SHA256}",
            f"P2_NESTED_BRIDGE_WINDOW=0x{START:x}..0x{END:x}",
            "P2_NESTED_BRIDGE_EXECUTION_CLASS=github_hosted",
            "P2_NESTED_BRIDGE_RUNTIME_ACCESS=none",
            "P2_NESTED_BRIDGE_PRIMARY_BYTES_EXACT_FENCED=true",
            "",
        ])
    )
    print("P2_NESTED_BRIDGE_HOSTED=PASS")
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
