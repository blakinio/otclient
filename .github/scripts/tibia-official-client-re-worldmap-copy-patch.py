#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import stat
import struct
import tempfile

EXACT_SIZE = 51965216
EXACT_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
TARGET_VA = 0x01CDD958
PREIMAGE = bytes.fromhex("120000000e0000000800000006000000")
POST_PREFIX = struct.pack("<II", 19, 14)
POSTIMAGE = POST_PREFIX + PREIMAGE[8:]
PT_LOAD = 1


class PatchRefused(RuntimeError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_regular_nonsymlink(path: Path, label: str) -> None:
    try:
        st = path.lstat()
    except OSError as exc:
        raise PatchRefused(f"{label}_LSTAT:{exc.__class__.__name__}") from exc
    if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode):
        raise PatchRefused(f"{label}_NOT_REGULAR_NONSYMLINK")


def parse_target_offset(path: Path, target_va: int = TARGET_VA, span: int = 16) -> int:
    with path.open("rb") as f:
        header = f.read(64)
        if len(header) != 64 or header[:4] != b"\x7fELF":
            raise PatchRefused("ELF_MAGIC")
        if header[4] != 2 or header[5] != 1:
            raise PatchRefused("ELF_NOT_64_LE")
        e_type, e_machine = struct.unpack_from("<HH", header, 16)
        if e_type != 3 or e_machine != 62:
            raise PatchRefused(f"ELF_TYPE_MACHINE:{e_type}:{e_machine}")
        e_phoff = struct.unpack_from("<Q", header, 32)[0]
        e_phentsize = struct.unpack_from("<H", header, 54)[0]
        e_phnum = struct.unpack_from("<H", header, 56)[0]
        if e_phentsize < 56 or e_phnum == 0 or e_phnum > 256:
            raise PatchRefused("ELF_PHDR_SHAPE")
        candidates: list[int] = []
        for index in range(e_phnum):
            f.seek(e_phoff + index * e_phentsize)
            raw = f.read(56)
            if len(raw) != 56:
                raise PatchRefused("ELF_PHDR_TRUNCATED")
            p_type, _flags, p_offset, p_vaddr, _p_paddr, p_filesz, _p_memsz, _align = struct.unpack(
                "<IIQQQQQQ", raw
            )
            if p_type != PT_LOAD:
                continue
            if p_vaddr <= target_va and target_va + span <= p_vaddr + p_filesz:
                derived = p_offset + (target_va - p_vaddr)
                if derived + span <= path.stat().st_size:
                    candidates.append(derived)
        if len(candidates) != 1:
            raise PatchRefused(f"ELF_TARGET_LOAD_COUNT:{len(candidates)}")
        return candidates[0]


def full_diff(source: Path, patched: Path) -> list[int]:
    diffs: list[int] = []
    offset = 0
    with source.open("rb") as a, patched.open("rb") as b:
        while True:
            ca = a.read(1024 * 1024)
            cb = b.read(1024 * 1024)
            if not ca and not cb:
                break
            if len(ca) != len(cb):
                raise PatchRefused("DIFF_SIZE_MISMATCH")
            if ca != cb:
                diffs.extend(offset + i for i, (x, y) in enumerate(zip(ca, cb)) if x != y)
                if len(diffs) > 16:
                    raise PatchRefused("DIFF_TOO_MANY_BYTES")
            offset += len(ca)
    return diffs


def patch_copy(source: Path, patched: Path, manifest: Path, *, exact_fence: bool = True) -> dict[str, str]:
    require_regular_nonsymlink(source, "SOURCE")
    require_regular_nonsymlink(patched, "PATCHED")
    source_size = source.stat().st_size
    patched_size = patched.stat().st_size
    if source_size != patched_size:
        raise PatchRefused("COPY_SIZE_MISMATCH")
    source_sha = sha256(source)
    patched_pre_sha = sha256(patched)
    if source_sha != patched_pre_sha:
        raise PatchRefused("COPY_PREIMAGE_SHA_MISMATCH")
    if exact_fence and (source_size != EXACT_SIZE or source_sha != EXACT_SHA256):
        raise PatchRefused(f"EXACT_SOURCE_FENCE:{source_size}:{source_sha}")

    file_offset = parse_target_offset(source)
    with source.open("rb") as f:
        f.seek(file_offset)
        source_guard = f.read(16)
    with patched.open("rb") as f:
        f.seek(file_offset)
        copy_guard = f.read(16)
    if source_guard != PREIMAGE or copy_guard != PREIMAGE:
        raise PatchRefused(f"PREIMAGE_GUARD:{source_guard.hex()}:{copy_guard.hex()}")

    with patched.open("r+b", buffering=0) as f:
        f.seek(file_offset)
        f.write(POST_PREFIX)
        f.flush()
        os.fsync(f.fileno())
        f.seek(file_offset)
        post = f.read(16)
    if post != POSTIMAGE:
        raise PatchRefused(f"POSTIMAGE_GUARD:{post.hex()}")

    patched_sha = sha256(patched)
    diffs = full_diff(source, patched)
    if diffs != [file_offset]:
        raise PatchRefused(f"FULL_DIFF:{','.join(hex(x) for x in diffs)}")
    if sha256(source) != source_sha:
        raise PatchRefused("SOURCE_CHANGED_DURING_PATCH")

    data = {
        "source_size": str(source_size),
        "source_sha256": source_sha,
        "target_va": f"0x{TARGET_VA:08x}",
        "file_offset": f"0x{file_offset:x}",
        "preimage_16_hex": PREIMAGE.hex(),
        "postimage_16_hex": POSTIMAGE.hex(),
        "candidate_pair": "19,14",
        "immutable_guard_pair": "8,6",
        "changed_byte_count": "1",
        "changed_file_offset": f"0x{file_offset:x}",
        "patched_sha256": patched_sha,
    }
    manifest.write_text("\n".join(f"{k}={v}" for k, v in data.items()) + "\n", encoding="utf-8")
    return data


def synthetic_elf() -> bytes:
    size = 0x4000
    target_segment_va = TARGET_VA - 0x1000
    target_file_offset = 0x1000
    data = bytearray(size)
    data[:16] = b"\x7fELF" + bytes([2, 1, 1, 0]) + b"\0" * 8
    struct.pack_into("<HHIQQQIHHHHHH", data, 16, 3, 62, 1, 0, 64, 0, 0, 64, 56, 1, 0, 0, 0)
    struct.pack_into(
        "<IIQQQQQQ",
        data,
        64,
        PT_LOAD,
        5,
        target_file_offset,
        target_segment_va,
        target_segment_va,
        0x2000,
        0x2000,
        0x1000,
    )
    off = target_file_offset + (TARGET_VA - target_segment_va)
    data[off : off + 16] = PREIMAGE
    return bytes(data)


def self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        source = root / "source"
        patched = root / "patched"
        manifest = root / "manifest.txt"
        source.write_bytes(synthetic_elf())
        patched.write_bytes(source.read_bytes())
        source.chmod(0o755)
        patched.chmod(0o755)
        result = patch_copy(source, patched, manifest, exact_fence=False)
        expected = 0x2000
        if result["file_offset"] != hex(expected):
            raise PatchRefused(f"SELFTEST_OFFSET:{result['file_offset']}")
        if result["changed_byte_count"] != "1":
            raise PatchRefused("SELFTEST_DIFF")
        if source.read_bytes()[expected : expected + 16] != PREIMAGE:
            raise PatchRefused("SELFTEST_SOURCE_MUTATED")
        if patched.read_bytes()[expected : expected + 16] != POSTIMAGE:
            raise PatchRefused("SELFTEST_POSTIMAGE")
    print("WORLDMAP_COPY_PATCH_SELFTEST=PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("self-test")
    p = sub.add_parser("patch")
    p.add_argument("source", type=Path)
    p.add_argument("patched", type=Path)
    p.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        if args.cmd == "self-test":
            return self_test()
        result = patch_copy(args.source, args.patched, args.manifest)
    except PatchRefused as exc:
        print(f"WORLDMAP_COPY_PATCH_REFUSED={exc}")
        return 44
    print("WORLDMAP_COPY_PATCH=PASS")
    for key in ("target_va", "file_offset", "changed_byte_count", "patched_sha256"):
        print(f"WORLDMAP_COPY_PATCH_{key.upper()}={result[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
