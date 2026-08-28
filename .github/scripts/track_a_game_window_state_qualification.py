#!/usr/bin/env python3
"""Bounded read-only qualification reader for exact-current gameWindowState."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import time
from typing import Callable, NoReturn, Sequence

import track_a_current_world_entered_anchor as anchor
import track_a_current_world_entered_durable_state as durable

GAME_WINDOW_CLASS = "tibia::gamewindow::TGameWindowController"
GAME_WINDOW_STATE_MEMBER_OFFSET = 0x60
GAME_WINDOW_STATE_MEMBER_WIDTH = 24
MAX_QSTRING_CHARS = 32
HEAP_SCAN_LIMIT = 768 * 1024 * 1024
SCAN_CHUNK = 8 * 1024 * 1024
CURRENT_VERSION = "15.32.75d4a0"
INGAME_TEXT = "INGAME"
DISALLOWED_SPECIAL_MAPPINGS = {"[vvar]", "[vdso]", "[vsyscall]"}


class QualificationError(RuntimeError):
    pass


@dataclass(frozen=True)
class Mapping:
    begin: int
    end: int
    perms: str
    path: str
    file_offset: int = 0


def parse_maps(text: str) -> list[Mapping]:
    regions: list[Mapping] = []
    for line in text.splitlines():
        parts = line.split(maxsplit=5)
        if len(parts) < 5:
            raise QualificationError("PROC_MAPS_MALFORMED")
        span = parts[0].split("-", 1)
        if len(span) != 2:
            raise QualificationError("PROC_MAPS_MALFORMED")
        try:
            begin, end = int(span[0], 16), int(span[1], 16)
            file_offset = int(parts[2], 16)
        except ValueError as exc:
            raise QualificationError("PROC_MAPS_MALFORMED") from exc
        if begin >= end:
            raise QualificationError("PROC_MAPS_RANGE_INVALID")
        regions.append(Mapping(begin, end, parts[1], parts[5] if len(parts) == 6 else "", file_offset))
    return regions


def payload_range_allowed(regions: Sequence[Mapping], address: int, byte_length: int) -> bool:
    if address <= 0 or byte_length <= 0:
        return False
    end = address + byte_length
    if end <= address:
        return False
    for region in regions:
        if not region.perms.startswith("r") or region.path in DISALLOWED_SPECIAL_MAPPINGS:
            continue
        if region.begin <= address and end <= region.end:
            return True
    return False


def classify_qstring_payload(length: int, payload: bytes) -> dict[str, object]:
    if length < 0 or length > MAX_QSTRING_CHARS:
        raise QualificationError("QSTRING_LENGTH_OUT_OF_BOUNDS")
    if len(payload) != length * 2:
        raise QualificationError("QSTRING_PAYLOAD_SHORT_READ")
    try:
        value = payload.decode("utf-16-le", "strict")
    except UnicodeDecodeError as exc:
        raise QualificationError("QSTRING_UTF16_INVALID") from exc
    if len(value) != length:
        raise QualificationError("QSTRING_DECODED_LENGTH_MISMATCH")
    if value == INGAME_TEXT:
        return {
            "semantic_state": "INGAME",
            "value_length": length,
            "known_text": INGAME_TEXT,
            "known_value_sha256": hashlib.sha256(INGAME_TEXT.encode("utf-8")).hexdigest(),
        }
    if value == "":
        return {
            "semantic_state": "EMPTY",
            "value_length": 0,
            "known_text": "",
            "known_value_sha256": hashlib.sha256(b"").hexdigest(),
        }
    return {
        "semantic_state": "OTHER",
        "value_length": length,
        "known_text": None,
        "known_value_sha256": None,
    }


def decode_qstring_member(
    member: bytes,
    regions: Sequence[Mapping],
    read_payload: Callable[[int, int], bytes],
) -> dict[str, object]:
    if len(member) != GAME_WINDOW_STATE_MEMBER_WIDTH:
        raise QualificationError("QSTRING_MEMBER_SHORT_READ")
    _allocation, data_pointer, length = struct.unpack("<QQq", member)
    if length < 0 or length > MAX_QSTRING_CHARS:
        raise QualificationError("QSTRING_LENGTH_OUT_OF_BOUNDS")
    if length == 0:
        if data_pointer and not payload_range_allowed(regions, data_pointer, 1):
            raise QualificationError("QSTRING_PAYLOAD_POINTER_OUT_OF_BOUNDS")
        return classify_qstring_payload(0, b"")
    byte_length = length * 2
    if not payload_range_allowed(regions, data_pointer, byte_length):
        raise QualificationError("QSTRING_PAYLOAD_POINTER_OUT_OF_BOUNDS")
    payload = read_payload(data_pointer, byte_length)
    if len(payload) != byte_length:
        raise QualificationError("QSTRING_PAYLOAD_SHORT_READ")
    return classify_qstring_payload(length, payload)


def select_unique_object(hits: Sequence[int]) -> int:
    unique = sorted(set(int(value) for value in hits))
    if len(unique) != 1:
        raise QualificationError(f"GAME_WINDOW_CONTROLLER_COUNT={len(unique)}")
    return unique[0]


def build_event(
    *,
    pid: int,
    start_ticks: int,
    uniqueness: str,
    semantic: dict[str, object],
    event_kind: str,
    exact_client_fence: str = "PASS",
    reason_code: str | None = None,
) -> dict[str, object]:
    event: dict[str, object] = {
        "schema": "otclient.track-a.game-window-state-qualification.v1",
        "event_kind": event_kind,
        "observed_epoch_ms": time.time_ns() // 1_000_000,
        "pid": int(pid),
        "process_start_ticks": int(start_ticks),
        "exact_client_fence": exact_client_fence,
        "tgamewindowcontroller_uniqueness": uniqueness,
        "semantic_state": str(semantic.get("semantic_state", "UNKNOWN")),
        "value_length": semantic.get("value_length"),
        "known_text": semantic.get("known_text"),
        "known_value_sha256": semantic.get("known_value_sha256"),
        "process_memory_access": "read_only",
        "raw_heap_bytes_retained": False,
        "raw_pointer_values_retained": False,
        "raw_window_title_retained": False,
        "credentials_retained": False,
        "session_secrets_retained": False,
        "packet_payloads_retained": False,
        "process_environment_retained": False,
        "in_game_claimed": False,
        "semantic_promotion_performed": False,
    }
    if reason_code:
        event["reason_code"] = reason_code
    return event


def _unknown(reason: str) -> dict[str, object]:
    return {
        "semantic_state": "UNKNOWN",
        "value_length": None,
        "known_text": None,
        "known_value_sha256": None,
        "reason_code": reason,
    }


def _start_ticks(pid: int) -> int:
    try:
        raw = Path(f"/proc/{pid}/stat").read_text(encoding="ascii")
        return int(raw[raw.rfind(")") + 2 :].split()[19])
    except (OSError, ValueError, IndexError) as exc:
        raise QualificationError("PROCESS_START_TICKS_UNAVAILABLE") from exc


def _read_exact(fd: int, address: int, length: int, code: str) -> bytes:
    try:
        payload = os.pread(fd, length, address)
    except OSError as exc:
        raise QualificationError(code) from exc
    if len(payload) != length:
        raise QualificationError(code)
    return payload


def _digest_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _load_exact_executable(pid: int, expected_size: int, expected_sha256: str) -> tuple[Path, bytes, os.stat_result]:
    if expected_size != int(anchor.EXPECTED_SIZE) or expected_sha256 != str(anchor.EXPECTED_SHA256):
        raise QualificationError("CALLER_EXACT_CLIENT_FENCE_NOT_CANONICAL")
    proc_exe = Path(f"/proc/{pid}/exe")
    try:
        stat = proc_exe.stat()
        exe = Path(os.path.realpath(proc_exe))
        raw = exe.read_bytes()
    except OSError as exc:
        raise QualificationError("EXACT_CLIENT_EXECUTABLE_UNAVAILABLE") from exc
    if len(raw) != expected_size or _digest_bytes(raw) != expected_sha256:
        raise QualificationError("EXACT_CLIENT_FENCE_MISMATCH")
    return exe, raw, stat


def _mapping_base(regions: Sequence[Mapping], exe: Path) -> int:
    executable_path = str(exe)
    bases = {
        region.begin - region.file_offset
        for region in regions
        if region.path == executable_path
    }
    if len(bases) != 1:
        raise QualificationError(f"CLIENT_MAPPING_BASE_COUNT={len(bases)}")
    return next(iter(bases))


def _heap_bounds(regions: Sequence[Mapping]) -> tuple[int, int]:
    heaps = [region for region in regions if region.path == "[heap]" and region.perms.startswith("rw")]
    if len(heaps) != 1:
        raise QualificationError(f"HEAP_MAPPING_COUNT={len(heaps)}")
    heap = heaps[0]
    if heap.end - heap.begin > HEAP_SCAN_LIMIT:
        raise QualificationError("HEAP_SCAN_BOUND_EXCEEDED")
    return heap.begin, heap.end


def _scan_unique_runtime_vptr(fd: int, heap_begin: int, heap_end: int, runtime_vptr: int) -> int:
    pattern = struct.pack("<Q", runtime_vptr)
    hits: list[int] = []
    cursor = heap_begin
    tail = b""
    while cursor < heap_end:
        want = min(SCAN_CHUNK, heap_end - cursor)
        data = _read_exact(fd, cursor, want, "HEAP_SCAN_SHORT_READ")
        merged = tail + data
        merged_base = cursor - len(tail)
        pos = 0
        while True:
            found = merged.find(pattern, pos)
            if found < 0:
                break
            address = merged_base + found
            if address % 8 == 0:
                hits.append(address)
                if len(set(hits)) > 1:
                    raise QualificationError("GAME_WINDOW_CONTROLLER_COUNT=2")
            pos = found + 1
        tail = merged[-7:]
        cursor += want
    return select_unique_object(hits)


def _verify_process_identity(pid: int, start_ticks: int, initial_stat: os.stat_result) -> None:
    if _start_ticks(pid) != start_ticks:
        raise QualificationError("PROCESS_START_TICKS_CHANGED")
    try:
        current = Path(f"/proc/{pid}/exe").stat()
    except OSError as exc:
        raise QualificationError("PROCESS_EXECUTABLE_IDENTITY_UNAVAILABLE") from exc
    if (current.st_dev, current.st_ino, current.st_size) != (initial_stat.st_dev, initial_stat.st_ino, initial_stat.st_size):
        raise QualificationError("PROCESS_EXECUTABLE_IDENTITY_CHANGED")


def _observe_state(
    fd: int,
    pid: int,
    start_ticks: int,
    initial_stat: os.stat_result,
    object_address: int,
    runtime_vptr: int,
    regions: Sequence[Mapping],
) -> dict[str, object]:
    _verify_process_identity(pid, start_ticks, initial_stat)
    vptr = struct.unpack("<Q", _read_exact(fd, object_address, 8, "OBJECT_VPTR_READ_FAILED"))[0]
    if vptr != runtime_vptr:
        raise QualificationError("GAME_WINDOW_CONTROLLER_VPTR_CHANGED")
    member = _read_exact(
        fd,
        object_address + GAME_WINDOW_STATE_MEMBER_OFFSET,
        GAME_WINDOW_STATE_MEMBER_WIDTH,
        "QSTRING_MEMBER_READ_FAILED",
    )
    result = decode_qstring_member(
        member,
        regions,
        lambda address, length: _read_exact(fd, address, length, "QSTRING_PAYLOAD_READ_FAILED"),
    )
    _verify_process_identity(pid, start_ticks, initial_stat)
    return result


def _write_event(handle, event: dict[str, object]) -> None:
    handle.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
    handle.flush()


def run(args: argparse.Namespace) -> int:
    if args.pid <= 0 or args.start_ticks <= 0:
        raise QualificationError("PID_IDENTITY_INVALID")
    if not (0.05 <= args.poll_seconds <= 5.0):
        raise QualificationError("POLL_INTERVAL_OUT_OF_BOUNDS")
    if not (1.0 <= args.heartbeat_seconds <= 60.0):
        raise QualificationError("HEARTBEAT_INTERVAL_OUT_OF_BOUNDS")
    if not (1 <= args.duration_seconds <= 3600):
        raise QualificationError("DURATION_OUT_OF_BOUNDS")
    if _start_ticks(args.pid) != args.start_ticks:
        raise QualificationError("START_TICKS_MISMATCH")

    exe, raw, initial_stat = _load_exact_executable(args.pid, args.expected_size, args.expected_sha256)
    sections, relocs = anchor.parse_elf_layout(raw)
    resolved = durable.resolve_primary_vptr_from_rtti(raw, sections, relocs, GAME_WINDOW_CLASS)
    regions = parse_maps(Path(f"/proc/{args.pid}/maps").read_text(encoding="utf-8"))
    base = _mapping_base(regions, exe)
    runtime_vptr = base + int(resolved["vptr_offset"])
    heap_begin, heap_end = _heap_bounds(regions)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(f"/proc/{args.pid}/mem", os.O_RDONLY | os.O_CLOEXEC)
    try:
        object_address = _scan_unique_runtime_vptr(fd, heap_begin, heap_end, runtime_vptr)
        _verify_process_identity(args.pid, args.start_ticks, initial_stat)
        deadline = time.monotonic() + args.duration_seconds
        last_key: tuple[object, ...] | None = None
        next_heartbeat = 0.0
        with output.open("w", encoding="utf-8", newline="\n") as handle:
            while time.monotonic() < deadline:
                try:
                    semantic = _observe_state(
                        fd, args.pid, args.start_ticks, initial_stat, object_address, runtime_vptr, regions
                    )
                except QualificationError as exc:
                    unknown = _unknown(str(exc))
                    _write_event(handle, build_event(
                        pid=args.pid,
                        start_ticks=args.start_ticks,
                        uniqueness="PROVEN",
                        semantic=unknown,
                        event_kind="FAIL_CLOSED",
                        reason_code=str(exc),
                    ))
                    return 2
                now = time.monotonic()
                key = (
                    semantic["semantic_state"], semantic["value_length"],
                    semantic["known_text"], semantic["known_value_sha256"],
                )
                if key != last_key:
                    _write_event(handle, build_event(
                        pid=args.pid,
                        start_ticks=args.start_ticks,
                        uniqueness="PROVEN",
                        semantic=semantic,
                        event_kind="INITIAL" if last_key is None else "STATE_CHANGE",
                    ))
                    last_key = key
                    next_heartbeat = now + args.heartbeat_seconds
                elif now >= next_heartbeat:
                    _write_event(handle, build_event(
                        pid=args.pid,
                        start_ticks=args.start_ticks,
                        uniqueness="PROVEN",
                        semantic=semantic,
                        event_kind="HEARTBEAT",
                    ))
                    next_heartbeat = now + args.heartbeat_seconds
                time.sleep(args.poll_seconds)
    finally:
        os.close(fd)
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pid", type=int, required=True)
    parser.add_argument("--start-ticks", type=int, required=True)
    parser.add_argument("--expected-size", type=int, required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--duration-seconds", type=int, default=1800)
    parser.add_argument("--poll-seconds", type=float, default=0.25)
    parser.add_argument("--heartbeat-seconds", type=float, default=5.0)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        return run(args)
    except (QualificationError, durable.DurableStateError, anchor.AnchorError, OSError, ValueError, struct.error) as exc:
        print(f"GAME_WINDOW_STATE_QUALIFICATION_FAIL_CLOSED={type(exc).__name__}:{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
