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
BUFFER_WRITER_HELPER = 0x1960340
KNOWN_INTERMEDIATE = (0x7DE7F0, 0x7DFD60, 0xC10960, 0xC20290, 0xC20C70)


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


def normalize_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def relevant_lines(text: str) -> list[str]:
    needles = (
        "call", "QBuffer", "QDataStream", "QIODevice", "QByteArray", "[rdi+0x18]", "[rdi+0x20]",
        "[rbx+0x18]", "[rbx+0x20]", "[rax+0x18]", "[rax+0x20]", "compress", "encrypt", "write", "send",
    )
    out: list[str] = []
    for line in normalize_lines(text):
        if any(n.lower() in line.lower() for n in needles):
            out.append(line)
    return out[:120]


def vtable_slots(elf: Elf64, ap: int, maximum: int) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for index in range(maximum):
        va = elf.u64(ap + index * 8)
        out.append({"index": index, "va": f"0x{va:x}", "executable": elf.executable(va)})
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
    args = parse_args()
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

    for i, expected in enumerate(KNOWN_INTERMEDIATE):
        require(elf.u64(INTERMEDIATE_AP + i * 8) == expected, f"intermediate_slot_{i}")
        require(elf.executable(expected), f"intermediate_slot_{i}_exec")

    writer_slots = vtable_slots(elf, WRITER_AP, 12)
    iodevice_slots = vtable_slots(elf, IODEVICE_WRITER_AP, 12)
    intermediate_slots = vtable_slots(elf, INTERMEDIATE_AP, 8)

    windows: dict[str, dict[str, object]] = {}
    for label, slots in (("writer", writer_slots), ("iodevice_writer", iodevice_slots), ("intermediate", intermediate_slots)):
        for slot in slots:
            if not slot["executable"]:
                continue
            va = int(str(slot["va"]), 16)
            text = disassemble(args.objdump, args.client, va, va + 0x280)
            key = f"{label}_slot_{slot['index']}"
            windows[key] = {
                "va": slot["va"],
                "relevant": relevant_lines(text),
                "reads_retained_plus18": bool(re.search(r"\[[^\]]+\+0x18\]", text, re.I)),
                "reads_retained_plus20": bool(re.search(r"\[[^\]]+\+0x20\]", text, re.I)),
                "qbuffer": "QBuffer" in text,
                "qdatastream": "QDataStream" in text,
                "qiodevice": "QIODevice" in text,
                "qbytearray": "QByteArray" in text,
            }

    # Construction/retention neighborhood is a bounded provenance control, not protocol-order proof.
    setup = disassemble(args.objdump, args.client, 0x1970C60, 0x1971250)
    require("1970d16:" in setup and "1960340" in setup, "persistent_helper_call_revalidated")
    require("1970d71:" in setup and "+0x18" in setup, "writer_retention_revalidated")
    require("1971068:" in setup and "+0x18" in setup, "processor_retention_revalidated")

    # Candidate means a TYPE-ANCHORED callable slot reads retained-looking +0x18/+0x20 and also
    # contains a concrete Qt byte/device/container operation. It is not yet a temporal/framing proof.
    candidates: list[dict[str, object]] = []
    for key, item in windows.items():
        if not key.startswith(("writer_", "iodevice_writer_")):
            continue
        member_read = bool(item["reads_retained_plus18"] or item["reads_retained_plus20"])
        byte_op = bool(item["qbuffer"] or item["qiodevice"] or item["qbytearray"])
        if member_read and byte_op:
            candidates.append({"slot": key, "va": item["va"], "relevant": item["relevant"]})

    result = {
        "schema_version": 1,
        "exact_client": {
            "sha256": digest,
            "size": EXPECTED_SIZE,
            "version_mapping": "15.32.df7b29",
            "platform": "official_native_linux_only",
        },
        "pinned": {
            "writer_ap": "0x2f69dd0",
            "writer_rtti": "0x3080728",
            "iodevice_writer_ap": "0x2f69d48",
            "iodevice_writer_rtti": "0x3080718",
            "intermediate_ap": "0x2f69e30",
            "intermediate_rtti": "0x3080748",
            "helper": "0x1960340",
        },
        "slots": {
            "writer": writer_slots,
            "iodevice_writer": iodevice_slots,
            "intermediate": intermediate_slots,
        },
        "windows": windows,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "classification": {
            "first_downstream_consumer": "CANDIDATE" if candidates else "UNKNOWN",
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
        "semantic_result": "TYPED_DOWNSTREAM_CANDIDATES_INVENTORIED" if candidates else "BOUNDED_TYPED_INVENTORY_NO_CONSUMER_PROVEN",
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.output_text.write_text(
        "\n".join(
            [
                f"P2_DOWNSTREAM_RESULT={result['semantic_result']}",
                f"CLIENT_SHA256={digest}",
                f"CLIENT_SIZE={EXPECTED_SIZE}",
                f"TYPED_CANDIDATE_COUNT={len(candidates)}",
                f"FIRST_DOWNSTREAM_CONSUMER={result['classification']['first_downstream_consumer']}",
                "PROTOCOL_STAGE_ORDER=UNKNOWN",
                "PROTOCOL_FRAMING=UNKNOWN",
                "SEQUENCE=UNKNOWN",
                "COMPRESSION=UNKNOWN",
                "ENCRYPTION=UNKNOWN",
                "FINAL_BINARY_EGRESS=UNKNOWN",
            ]
        ) + "\n",
        encoding="utf-8",
    )

    evidence_lines = [
        "# Exact typed vtable slot inventory",
        json.dumps(result["slots"], indent=2, sort_keys=True),
        "",
        "# Candidate windows",
    ]
    for c in candidates:
        evidence_lines.append(f"## {c['slot']} @ {c['va']}")
        evidence_lines.extend(str(x) for x in c["relevant"])
    evidence_lines.extend(["", "# Persistent provenance control", *relevant_lines(setup)])
    args.evidence.write_text("\n".join(evidence_lines) + "\n", encoding="utf-8")

    print("P2_DOWNSTREAM_COMPLETE=true")
    print(f"P2_DOWNSTREAM_RESULT={result['semantic_result']}")
    print(f"P2_DOWNSTREAM_TYPED_CANDIDATE_COUNT={len(candidates)}")
    print("P2_DOWNSTREAM_PROTOCOL_STAGE_ORDER=UNKNOWN")
    print("P2_DOWNSTREAM_FINAL_BINARY_EGRESS=UNKNOWN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
