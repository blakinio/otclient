#!/usr/bin/env python3
"""Bounded read-only runtime snapshot for the exact Tibia Linux P0 candidate.

This helper is a producer tool, not semantic proof. It locates relocation-backed
TPlayerData-typed objects by the exact primary vptr, then reads only the direct
signed-i32 candidate fields +0x78/+0x7c/+0x80. It never writes process memory,
never injects input and never creates or logs into a client session.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
import struct
import time


DIRECT_X_OFFSET = 0x78
DIRECT_Y_OFFSET = 0x7C
DIRECT_Z_OFFSET = 0x80
MAX_RW_REGION_BYTES = 512 * 1024 * 1024
SCAN_CHUNK_BYTES = 1024 * 1024


@dataclass(frozen=True)
class Region:
    begin: int
    end: int
    perms: str
    offset: int
    path: str

    def contains(self, address: int) -> bool:
        return self.begin <= address < self.end


@dataclass(frozen=True)
class TypedSnapshot:
    object_address: int
    private_data_pointer: int
    x: int
    y: int
    z: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pid", required=True, type=int)
    parser.add_argument("--client", required=True, type=Path)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--expected-size", required=True, type=int)
    parser.add_argument("--vptr-offset", required=True, type=lambda value: int(value, 0))
    parser.add_argument("--snapshot-label", required=True)
    parser.add_argument("--require-unique-typed-object", action="store_true")
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_client_fence(client: Path, expected_size: int, expected_sha256: str) -> Path:
    resolved = client.resolve()
    actual_size = resolved.stat().st_size
    actual_sha256 = sha256_file(resolved)
    if actual_size != expected_size:
        raise RuntimeError(f"client size mismatch: {actual_size} != {expected_size}")
    if actual_sha256 != expected_sha256:
        raise RuntimeError(f"client sha256 mismatch: {actual_sha256}")
    return resolved


def read_maps(pid: int) -> list[Region]:
    regions: list[Region] = []
    for line in Path(f"/proc/{pid}/maps").read_text(encoding="utf-8").splitlines():
        fields = line.split(maxsplit=5)
        if len(fields) < 5:
            continue
        begin_text, end_text = fields[0].split("-", 1)
        regions.append(
            Region(
                begin=int(begin_text, 16),
                end=int(end_text, 16),
                perms=fields[1],
                offset=int(fields[2], 16),
                path=fields[5] if len(fields) == 6 else "",
            )
        )
    return regions


def resolved_exe(pid: int) -> Path:
    return Path(os.path.realpath(f"/proc/{pid}/exe"))


def main_base(regions: list[Region], client: Path) -> int:
    wanted = str(client.resolve())
    candidates = [region.begin - region.offset for region in regions if region.path == wanted]
    if not candidates:
        raise RuntimeError("exact client mapping not found in /proc/PID/maps")
    return min(candidates)


def readable_writable(regions: list[Region]) -> list[Region]:
    return [
        region
        for region in regions
        if len(region.perms) >= 2
        and region.perms[0] == "r"
        and region.perms[1] == "w"
        and 0 < region.end - region.begin <= MAX_RW_REGION_BYTES
    ]


def address_in(regions: list[Region], address: int) -> bool:
    return any(region.contains(address) for region in regions)


def pread_exact(fd: int, address: int, size: int) -> bytes:
    data = os.pread(fd, size, address)
    if len(data) != size:
        raise OSError(f"short read at 0x{address:x}: {len(data)}/{size}")
    return data


def find_typed_objects(fd: int, regions: list[Region], expected_vptr: int) -> list[tuple[int, int]]:
    """Return aligned (object, private-data-pointer) pairs matching exact vptr."""
    pattern = struct.pack("<Q", expected_vptr)
    overlap = len(pattern) - 1
    rw = readable_writable(regions)
    hits: list[tuple[int, int]] = []
    for region in rw:
        cursor = region.begin
        tail = b""
        while cursor < region.end:
            wanted = min(SCAN_CHUNK_BYTES, region.end - cursor)
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
                object_address = merged_base + index
                if object_address % 8 == 0:
                    try:
                        private_data = struct.unpack(
                            "<Q", pread_exact(fd, object_address + 8, 8)
                        )[0]
                    except OSError:
                        private_data = 0
                    if private_data and address_in(rw, private_data):
                        hits.append((object_address, private_data))
                search_at = index + 1
            tail = merged[-overlap:] if overlap else b""
            cursor += len(data)
    return sorted(set(hits))


def decode_direct_xyz(blob: bytes) -> tuple[int, int, int]:
    if len(blob) != 12:
        raise ValueError("direct XYZ blob must be exactly 12 bytes")
    return struct.unpack("<iii", blob)


def read_direct_snapshot(fd: int, object_address: int, private_data: int) -> TypedSnapshot:
    blob = pread_exact(fd, object_address + DIRECT_X_OFFSET, 12)
    x, y, z = decode_direct_xyz(blob)
    return TypedSnapshot(object_address, private_data, x, y, z)


def parse_process_start_ticks(stat_text: str) -> int:
    """Parse Linux /proc/PID/stat field 22 without assuming comm has no spaces."""
    close = stat_text.rfind(")")
    if close < 0:
        raise ValueError("malformed /proc/PID/stat: missing comm terminator")
    suffix = stat_text[close + 1 :].strip().split()
    # suffix[0] is field 3 (state), so field 22 is suffix index 19.
    if len(suffix) <= 19:
        raise ValueError("malformed /proc/PID/stat: starttime unavailable")
    return int(suffix[19])


def process_start_ticks(pid: int) -> int:
    return parse_process_start_ticks(Path(f"/proc/{pid}/stat").read_text(encoding="utf-8"))


def boot_id_sha256() -> str:
    raw = Path("/proc/sys/kernel/random/boot_id").read_text(encoding="utf-8").strip()
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build_payload(
    *,
    label: str,
    pid: int,
    start_ticks: int,
    boot_hash: str,
    client: Path,
    client_sha256: str,
    client_size: int,
    main_image_base: int,
    expected_vptr: int,
    snapshots: list[TypedSnapshot],
    wall_time_ns: int,
    monotonic_ns: int,
) -> dict[str, object]:
    return {
        "schema": 1,
        "snapshot_label": label,
        "pid": pid,
        "process_start_ticks": start_ticks,
        "boot_id_sha256": boot_hash,
        "client_path": str(client),
        "client_sha256": client_sha256,
        "client_size": client_size,
        "main_base": main_image_base,
        "expected_tplayerdata_vptr": expected_vptr,
        "typed_object_count": len(snapshots),
        "typed_objects": [
            {
                "object": snapshot.object_address,
                "private_data": snapshot.private_data_pointer,
                "x": snapshot.x,
                "y": snapshot.y,
                "z": snapshot.z,
                "representation": "signed_i32_x3",
                "offsets": [DIRECT_X_OFFSET, DIRECT_Y_OFFSET, DIRECT_Z_OFFSET],
            }
            for snapshot in snapshots
        ],
        "wall_time_ns": wall_time_ns,
        "monotonic_ns": monotonic_ns,
        "process_memory_access": "read_only",
        "process_memory_writes": 0,
        "semantic_player_xyz_proven": False,
    }


def main() -> int:
    args = parse_args()
    client = exact_client_fence(args.client, args.expected_size, args.expected_sha256)
    if resolved_exe(args.pid) != client:
        raise SystemExit(f"P0_RUNTIME_SNAPSHOT_ERROR=pid_exe_mismatch:{resolved_exe(args.pid)}")

    start_ticks = process_start_ticks(args.pid)
    boot_hash = boot_id_sha256()
    regions = read_maps(args.pid)
    base = main_base(regions, client)
    expected_vptr = base + args.vptr_offset

    fd = os.open(f"/proc/{args.pid}/mem", os.O_RDONLY | os.O_CLOEXEC)
    try:
        typed = find_typed_objects(fd, regions, expected_vptr)
        snapshots = [read_direct_snapshot(fd, object_address, private_data) for object_address, private_data in typed]
    finally:
        os.close(fd)

    if args.require_unique_typed_object and len(snapshots) != 1:
        raise SystemExit(f"P0_RUNTIME_SNAPSHOT_ERROR=typed_object_count:{len(snapshots)}")

    payload = build_payload(
        label=args.snapshot_label,
        pid=args.pid,
        start_ticks=start_ticks,
        boot_hash=boot_hash,
        client=client,
        client_sha256=args.expected_sha256,
        client_size=args.expected_size,
        main_image_base=base,
        expected_vptr=expected_vptr,
        snapshots=snapshots,
        wall_time_ns=time.time_ns(),
        monotonic_ns=time.monotonic_ns(),
    )
    print("TRACK_A_P0_RUNTIME_SNAPSHOT_READ_ONLY=true")
    print(f"TRACK_A_P0_RUNTIME_SNAPSHOT_LABEL={args.snapshot_label}")
    print(f"TRACK_A_P0_RUNTIME_PID={args.pid}")
    print(f"TRACK_A_P0_RUNTIME_PROCESS_START_TICKS={start_ticks}")
    print(f"TRACK_A_P0_RUNTIME_BOOT_ID_SHA256={boot_hash}")
    print(f"TRACK_A_P0_RUNTIME_MAIN_BASE=0x{base:x}")
    print(f"TRACK_A_P0_RUNTIME_TPLAYERDATA_VPTR=0x{expected_vptr:x}")
    print(f"TRACK_A_P0_RUNTIME_TYPED_OBJECT_COUNT={len(snapshots)}")
    for snapshot in snapshots:
        print(
            "TRACK_A_P0_RUNTIME_DIRECT_CANDIDATE="
            f"object=0x{snapshot.object_address:x} private_data=0x{snapshot.private_data_pointer:x} "
            f"offsets=0x78,0x7c,0x80 representation=signed_i32_x3 "
            f"xyz={snapshot.x},{snapshot.y},{snapshot.z}"
        )
    print("TRACK_A_P0_RUNTIME_SNAPSHOT_JSON=" + json.dumps(payload, sort_keys=True, separators=(",", ":")))
    print("TRACK_A_P0_RUNTIME_SEMANTIC_PLAYER_XYZ_PROVEN=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
