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
TARGET = 0xF50090
CODE_START = 0xF50040
CODE_END = 0xF50480


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise SystemExit(f"P2_F50090_FAIL={marker}")
    print(f"P2_F50090_OK={marker}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_segments(path: Path) -> list[tuple[int, int, int]]:
    with path.open("rb") as handle:
        ident = handle.read(16)
        require(ident[:4] == b"\x7fELF", "elf_magic")
        require(ident[4] == 2 and ident[5] == 1, "elf64_little")
        rest = handle.read(48)
        require(len(rest) == 48, "elf_header_complete")
        fields = struct.unpack("<HHIQQQIHHHHHH", rest)
        phoff = fields[4]
        phentsize = fields[8]
        phnum = fields[9]
        require(phentsize >= 56 and 0 < phnum < 128, "program_headers")
        segments: list[tuple[int, int, int]] = []
        for index in range(phnum):
            handle.seek(phoff + index * phentsize)
            row = handle.read(56)
            require(len(row) == 56, f"ph_{index}_complete")
            p_type, _flags, p_offset, p_vaddr, _paddr, p_filesz, _p_memsz, _align = struct.unpack(
                "<IIQQQQQQ", row
            )
            if p_type == 1 and p_filesz:
                segments.append((p_vaddr, p_filesz, p_offset))
        require(bool(segments), "load_segments")
        return segments


def read_va(path: Path, start: int, end: int) -> bytes:
    require(end > start, "range_order")
    for vaddr, filesz, offset in load_segments(path):
        if start >= vaddr and end <= vaddr + filesz:
            with path.open("rb") as handle:
                handle.seek(offset + start - vaddr)
                data = handle.read(end - start)
            require(len(data) == end - start, "range_complete")
            return data
    raise SystemExit("P2_F50090_FAIL=range_not_file_backed")


def record(start: int, end: int, data: bytes) -> dict[str, object]:
    return {
        "start": start,
        "end": end,
        "length": len(data),
        "sha256": sha256_bytes(data),
        "hex": data.hex(),
    }


def decode_record(entry: dict[str, object]) -> bytes:
    data = bytes.fromhex(str(entry["hex"]))
    require(len(data) == int(entry["length"]), "record_length")
    require(sha256_bytes(data) == entry["sha256"], "record_digest")
    return data


def source_mode(args: argparse.Namespace) -> int:
    client = args.client.resolve()
    require(client.is_file(), "source_file")
    require(not client.is_symlink(), "source_not_symlink")
    require(stat.S_ISREG(client.stat().st_mode), "source_regular")
    require(client.stat().st_size == EXPECTED_SIZE, "source_exact_size")
    require(sha256_file(client) == EXPECTED_SHA256, "source_exact_sha256")
    code = read_va(client, CODE_START, CODE_END)

    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "track-a-p2-f50090-source-v1",
        "exact_client": {
            "version": EXPECTED_VERSION,
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
            "platform": "official_native_linux_only",
        },
        "source_candidate_index": args.candidate_index,
        "runtime_access": "none",
        "source_operation": "single_bounded_file_backed_code_window_only",
        "source_disassembly": False,
        "source_semantic_classification": False,
        "client_process_accessed": False,
        "process_memory_accessed": False,
        "canonical_state_accessed": False,
        "client_executed": False,
        "client_byte_mutated": False,
        "raw_client_uploaded": False,
        "target": TARGET,
        "code_window": record(CODE_START, CODE_END, code),
    }
    (outdir / "source-evidence.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    (outdir / "source-fence.txt").write_text(
        "\n".join(
            [
                f"P2_F50090_CLIENT_VERSION={EXPECTED_VERSION}",
                f"P2_F50090_CLIENT_SIZE={EXPECTED_SIZE}",
                f"P2_F50090_CLIENT_SHA256={EXPECTED_SHA256}",
                f"P2_F50090_TARGET=0x{TARGET:x}",
                f"P2_F50090_CODE_WINDOW=0x{CODE_START:x}..0x{CODE_END:x}",
                "P2_F50090_RUNTIME_ACCESS=none",
                "P2_F50090_SOURCE_OPERATION=single_bounded_file_backed_code_window_only",
                "P2_F50090_SOURCE_DISASSEMBLY=false",
                "P2_F50090_SOURCE_SEMANTIC_CLASSIFICATION=false",
                "P2_F50090_CLIENT_PROCESS_ACCESSED=false",
                "P2_F50090_PROCESS_MEMORY_ACCESSED=false",
                "P2_F50090_CANONICAL_STATE_ACCESSED=false",
                "P2_F50090_CLIENT_EXECUTED=false",
                "P2_F50090_CLIENT_BYTE_MUTATED=false",
                "P2_F50090_RAW_CLIENT_UPLOADED=false",
                "",
            ]
        )
    )
    print("P2_F50090_SOURCE=PASS")
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
    require(bundle.get("target") == TARGET, "hosted_target")

    entry = bundle["code_window"]
    require(entry["start"] == CODE_START and entry["end"] == CODE_END, "hosted_code_range")
    code = decode_record(entry)

    with tempfile.TemporaryDirectory(prefix="p2-f50090-") as tempdir:
        raw = Path(tempdir) / "f50090.bin"
        raw.write_bytes(code)
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
                f"--adjust-vma=0x{CODE_START:x}",
                str(raw),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        disassembly = proc.stdout

    require(f"{TARGET:x}:" in disassembly, "target_anchor_present")

    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "disassembly.txt").write_text(disassembly)
    result = {
        "schema": "track-a-p2-f50090-hosted-v1",
        "exact_client": fence,
        "execution_class": "github_hosted",
        "runtime_access": "none",
        "primary_bytes_exact_fenced": True,
        "target": TARGET,
        "code_window": {
            "start": CODE_START,
            "end": CODE_END,
            "sha256": entry["sha256"],
        },
        "classification": {
            "same_message_input_relationship": "PENDING_PRIMARY_HOSTED_REVIEW",
            "first_same_message_downstream_target": "PENDING_PRIMARY_HOSTED_REVIEW",
            "direct_binary_write_sink": "UNKNOWN",
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
                "P2_F50090_HOSTED_VALIDATION=PASS",
                f"P2_F50090_CLIENT_VERSION={EXPECTED_VERSION}",
                f"P2_F50090_CLIENT_SIZE={EXPECTED_SIZE}",
                f"P2_F50090_CLIENT_SHA256={EXPECTED_SHA256}",
                f"P2_F50090_TARGET=0x{TARGET:x}",
                f"P2_F50090_CODE_WINDOW=0x{CODE_START:x}..0x{CODE_END:x}",
                "P2_F50090_EXECUTION_CLASS=github_hosted",
                "P2_F50090_RUNTIME_ACCESS=none",
                "P2_F50090_PRIMARY_BYTES_EXACT_FENCED=true",
                "",
            ]
        )
    )
    print("P2_F50090_HOSTED=PASS")
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
