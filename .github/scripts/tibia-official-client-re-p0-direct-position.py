#!/usr/bin/env python3
"""Passive exact-build probe for direct player-position candidates.

The probe is intentionally scoped to the relocation-backed TPlayerData owner.
It never scans the process globally for XYZ triples and never writes to the
process. Structural map-strip data is reported only as an independent oracle
for later semantic discrimination.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import struct
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Region:
    begin: int
    end: int
    perms: str
    offset: int
    path: str

    def contains(self, address: int) -> bool:
        return self.begin <= address < self.end


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pid", type=int, required=True)
    parser.add_argument("--client", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--expected-size", type=int, required=True)
    parser.add_argument("--vptr-offset", type=lambda value: int(value, 0), required=True)
    parser.add_argument("--strips", type=Path)
    parser.add_argument("--object-bytes", type=lambda value: int(value, 0), default=0x1000)
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_maps(pid: int) -> list[Region]:
    regions: list[Region] = []
    for line in Path(f"/proc/{pid}/maps").read_text().splitlines():
        fields = line.split(maxsplit=5)
        if len(fields) < 5:
            continue
        begin_text, end_text = fields[0].split("-", 1)
        path = fields[5] if len(fields) == 6 else ""
        regions.append(
            Region(
                begin=int(begin_text, 16),
                end=int(end_text, 16),
                perms=fields[1],
                offset=int(fields[2], 16),
                path=path,
            )
        )
    return regions


def resolved_exe(pid: int) -> Path:
    return Path(os.path.realpath(f"/proc/{pid}/exe"))


def main_base(regions: list[Region], client: Path) -> int:
    wanted = str(client.resolve())
    candidates = [region.begin - region.offset for region in regions if region.path == wanted]
    if not candidates:
        raise RuntimeError("client mapping not found in /proc/PID/maps")
    return min(candidates)


def writable_readable(regions: list[Region]) -> list[Region]:
    return [
        region
        for region in regions
        if len(region.perms) >= 2
        and region.perms[0] == "r"
        and region.perms[1] == "w"
        and region.end > region.begin
        and region.end - region.begin <= 512 * 1024 * 1024
    ]


def address_in(regions: list[Region], address: int) -> bool:
    return any(region.contains(address) for region in regions)


def pread_exact(fd: int, address: int, size: int) -> bytes:
    data = os.pread(fd, size, address)
    if len(data) != size:
        raise OSError(f"short read at 0x{address:x}: {len(data)}/{size}")
    return data


def find_typed_hits(fd: int, regions: list[Region], expected_vptr: int) -> list[int]:
    pattern = struct.pack("<Q", expected_vptr)
    hits: list[int] = []
    chunk_size = 1024 * 1024
    overlap = len(pattern) - 1
    for region in writable_readable(regions):
        cursor = region.begin
        tail = b""
        while cursor < region.end:
            wanted = min(chunk_size, region.end - cursor)
            try:
                data = os.pread(fd, wanted, cursor)
            except OSError:
                cursor += wanted
                tail = b""
                continue
            if not data:
                cursor += wanted
                tail = b""
                continue
            merged = tail + data
            merged_base = cursor - len(tail)
            search_at = 0
            while True:
                index = merged.find(pattern, search_at)
                if index < 0:
                    break
                address = merged_base + index
                if address % 8 == 0:
                    try:
                        private_data = struct.unpack("<Q", pread_exact(fd, address + 8, 8))[0]
                    except OSError:
                        private_data = 0
                    if private_data and address_in(writable_readable(regions), private_data):
                        hits.append(address)
                search_at = index + 1
            tail = merged[-overlap:] if overlap else b""
            cursor += len(data)
    return sorted(set(hits))


def plausible_u32(value: int) -> bool:
    return 30000 <= value <= 40000


def scan_inline_candidates(blob: bytes) -> list[tuple[str, int, tuple[int, int, int]]]:
    found: list[tuple[str, int, tuple[int, int, int]]] = []
    for offset in range(0, max(0, len(blob) - 12) + 1, 4):
        x, y, z = struct.unpack_from("<III", blob, offset)
        if plausible_u32(x) and plausible_u32(y) and 0 <= z <= 15:
            found.append(("u32x3", offset, (x, y, z)))
    for offset in range(0, max(0, len(blob) - 5) + 1, 2):
        x, y = struct.unpack_from("<HH", blob, offset)
        z = blob[offset + 4]
        if plausible_u32(x) and plausible_u32(y) and 0 <= z <= 15:
            found.append(("u16_u16_u8", offset, (x, y, z)))
    return found


def first_level_pointer_candidates(
    fd: int, regions: list[Region], owner_blob: bytes, limit: int = 48
) -> list[tuple[int, int, str, int, tuple[int, int, int]]]:
    rw = writable_readable(regions)
    results: list[tuple[int, int, str, int, tuple[int, int, int]]] = []
    seen_targets: set[int] = set()
    for owner_offset in range(8, min(len(owner_blob), 0x200) - 7, 8):
        target = struct.unpack_from("<Q", owner_blob, owner_offset)[0]
        if target in seen_targets or not address_in(rw, target):
            continue
        seen_targets.add(target)
        try:
            pointed = os.pread(fd, 0x400, target)
        except OSError:
            continue
        if len(pointed) < 16:
            continue
        for encoding, field_offset, xyz in scan_inline_candidates(pointed):
            results.append((owner_offset, target, encoding, field_offset, xyz))
            if len(results) >= limit:
                return results
    return results


def strip_oracle(path: Path | None) -> None:
    if path is None or not path.is_file():
        print("TRACK_A_P0_STRUCTURAL_ORACLE=unavailable")
        return
    records: list[tuple[int, int, int, int]] = []
    for raw in path.read_text(errors="replace").splitlines()[-500:]:
        fields = raw.split("\t")
        if len(fields) < 4:
            continue
        try:
            records.append(tuple(int(fields[index]) for index in range(4)))
        except ValueError:
            continue
    if not records:
        print("TRACK_A_P0_STRUCTURAL_ORACLE=empty")
        return

    # Cluster the most recent decoder burst; a 0.5 s gap separates the known
    # reversible movement bursts while retaining every row from one strip.
    groups: list[list[tuple[int, int, int, int]]] = [[records[0]]]
    for record in records[1:]:
        if record[0] - groups[-1][-1][0] > 500_000_000:
            groups.append([])
        groups[-1].append(record)
    latest = groups[-1]
    floor7 = [(x, y) for _, x, y, z in latest if z == 7]
    if not floor7:
        print(f"TRACK_A_P0_STRUCTURAL_ORACLE=latest_group_without_floor7 records={len(latest)}")
        return
    xs = sorted({x for x, _ in floor7})
    ys = sorted({y for _, y in floor7})
    print(
        "TRACK_A_P0_STRUCTURAL_ORACLE="
        f"records={len(latest)} floor7_x={xs[0]}..{xs[-1]} "
        f"floor7_y={ys[0]}..{ys[-1]} unique_x={len(xs)} unique_y={len(ys)}"
    )
    if len(xs) == 18 and len(ys) == 1:
        center_x = xs[0] + 9
        print(
            "TRACK_A_P0_VERTICAL_STRIP_ORACLE_CANDIDATES="
            f"({center_x},{ys[0] + 7},7),({center_x},{ys[0] - 6},7)"
        )


def nearby_type_strings(client: Path) -> None:
    data = client.read_bytes()
    needle = b"tibia::game::TPlayerData"
    start = 0
    hits = []
    while True:
        index = data.find(needle, start)
        if index < 0:
            break
        hits.append(index)
        start = index + 1
    print(f"TRACK_A_P0_TPLAYERDATA_STRING_HITS={len(hits)}")
    for index in hits[:8]:
        lo = max(0, index - 2048)
        hi = min(len(data), index + 4096)
        strings: list[str] = []
        current = bytearray()
        for value in data[lo:hi]:
            if 32 <= value < 127:
                current.append(value)
            else:
                if len(current) >= 4:
                    strings.append(current.decode("ascii", "replace"))
                current.clear()
        if len(current) >= 4:
            strings.append(current.decode("ascii", "replace"))
        compact = []
        for value in strings:
            if value not in compact:
                compact.append(value)
        print(f"TRACK_A_P0_TPLAYERDATA_STRING_OFFSET=0x{index:x}")
        for value in compact[:60]:
            print(f"TRACK_A_P0_NEAR_TYPE_STRING={value}")


def main() -> int:
    args = parse_args()
    client = args.client.resolve()
    actual_size = client.stat().st_size
    actual_sha = sha256(client)
    if actual_size != args.expected_size:
        raise SystemExit(f"client size mismatch: {actual_size}")
    if actual_sha != args.expected_sha256:
        raise SystemExit(f"client sha256 mismatch: {actual_sha}")
    if resolved_exe(args.pid) != client:
        raise SystemExit(f"PID exe mismatch: {resolved_exe(args.pid)} != {client}")

    print("TRACK_A_P0_EXACT_CLIENT_FENCE=true")
    print(f"TRACK_A_P0_CLIENT_SHA256={actual_sha}")
    print(f"TRACK_A_P0_CLIENT_SIZE={actual_size}")
    print(f"TRACK_A_P0_PID={args.pid}")

    regions = read_maps(args.pid)
    base = main_base(regions, client)
    expected_vptr = base + args.vptr_offset
    print(f"TRACK_A_P0_MAIN_BASE=0x{base:x}")
    print(f"TRACK_A_P0_TPLAYERDATA_VPTR=0x{expected_vptr:x}")

    mem_fd = os.open(f"/proc/{args.pid}/mem", os.O_RDONLY | os.O_CLOEXEC)
    try:
        hits = find_typed_hits(mem_fd, regions, expected_vptr)
        print(f"TRACK_A_P0_TPLAYERDATA_TYPED_HITS={len(hits)}")
        for index, address in enumerate(hits):
            print(f"TRACK_A_P0_TPLAYERDATA_OBJECT[{index}]=0x{address:x}")
            blob = os.pread(mem_fd, args.object_bytes, address)
            inline = scan_inline_candidates(blob)
            print(f"TRACK_A_P0_INLINE_XYZ_CANDIDATES[{index}]={len(inline)}")
            for encoding, offset, xyz in inline[:64]:
                print(
                    f"TRACK_A_P0_INLINE_CANDIDATE object=0x{address:x} "
                    f"encoding={encoding} offset=0x{offset:x} xyz={xyz[0]},{xyz[1]},{xyz[2]}"
                )
            pointed = first_level_pointer_candidates(mem_fd, regions, blob)
            print(f"TRACK_A_P0_LEVEL1_XYZ_CANDIDATES[{index}]={len(pointed)}")
            for owner_offset, target, encoding, field_offset, xyz in pointed:
                print(
                    f"TRACK_A_P0_LEVEL1_CANDIDATE object=0x{address:x} owner_offset=0x{owner_offset:x} "
                    f"target=0x{target:x} encoding={encoding} field_offset=0x{field_offset:x} "
                    f"xyz={xyz[0]},{xyz[1]},{xyz[2]}"
                )
    finally:
        os.close(mem_fd)

    strip_oracle(args.strips)
    nearby_type_strings(client)
    print("TRACK_A_P0_PASSIVE_PROBE_COMPLETE=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
