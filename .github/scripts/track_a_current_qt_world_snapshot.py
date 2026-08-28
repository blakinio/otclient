#!/usr/bin/env python3
"""Bounded read-only Qt/world snapshot for the exact current Official Tibia client."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import time

PID = int(sys.argv[1])
START_TICKS = int(sys.argv[2])
EXPECTED_SIZE = int(sys.argv[3])
EXPECTED_SHA256 = sys.argv[4]
AUTH_MEMBER_SCAN_LIMIT = 0x1200
HEAP_SCAN_LIMIT = 768 * 1024 * 1024
KNOWN_QT_STATE_MACHINE_SIZE = 394_824
KNOWN_QT_STATE_MACHINE_SHA256 = "26f504ae723fa15c77e0c33a93a964a305c63577f2bed3f136c098b7b06921e8"
QSTATE_PRIVATE_OFFSET = 0x8
QSTATE_STATE_OFFSET = 0xF0
QSTATE_RUNNING_VALUE = 2

TYPES = {
    "game_client": ("tibia::client::TGameClient", "N5tibia6client11TGameClientE", True),
    "auth_controller": ("tibia::authentication::TAuthenticationProcessController", "N5tibia14authentication32TAuthenticationProcessControllerE", True),
    "player_protocol_handler": ("tibia::game::TPlayerProtocolMessageHandler", "N5tibia4game29TPlayerProtocolMessageHandlerE", False),
    "gameserver_game_session": ("tibia::game::TGameserverGameSession", "N5tibia4game22TGameserverGameSessionE", False),
    "worldmap_protocol_handler": ("tibia::worldmap::TWorldmapProtocolMessageHandler", "N5tibia8worldmap31TWorldmapProtocolMessageHandlerE", False),
    "disconnect_reaction_controller": ("tibia::gamewindow::TGameSessionDisconnectReactionController", "N5tibia10gamewindow40TGameSessionDisconnectReactionControllerE", False),
}


def fail(reason: str) -> "NoReturn":
    raise SystemExit(reason)


def ticks() -> int:
    raw = Path(f"/proc/{PID}/stat").read_text(encoding="ascii")
    return int(raw[raw.rfind(")") + 2 :].split()[19])


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def elf_layout(raw: bytes):
    if raw[:4] != b"\x7fELF" or raw[4] != 2 or raw[5] != 1:
        fail("ELF64_LITTLE_ENDIAN_REQUIRED")
    phoff = struct.unpack_from("<Q", raw, 0x20)[0]
    shoff = struct.unpack_from("<Q", raw, 0x28)[0]
    phentsize = struct.unpack_from("<H", raw, 0x36)[0]
    phnum = struct.unpack_from("<H", raw, 0x38)[0]
    shentsize = struct.unpack_from("<H", raw, 0x3A)[0]
    shnum = struct.unpack_from("<H", raw, 0x3C)[0]
    shstrndx = struct.unpack_from("<H", raw, 0x3E)[0]
    loads = []
    for index in range(phnum):
        off = phoff + index * phentsize
        p_type, _flags, p_offset, p_vaddr, _paddr, p_filesz, _memsz, _align = struct.unpack_from("<IIQQQQQQ", raw, off)
        if p_type == 1:
            loads.append((p_offset, p_vaddr, p_filesz))
    sections = []
    for index in range(shnum):
        off = shoff + index * shentsize
        sections.append(struct.unpack_from("<IIQQQQIIQQ", raw, off))
    if shstrndx >= len(sections):
        fail("ELF_SHSTRTAB_INVALID")
    shstr = sections[shstrndx]
    names = raw[shstr[4] : shstr[4] + shstr[5]]
    relative = {}
    for section in sections:
        name_off, sh_type, _flags, _addr, file_off, size, _link, _info, _align, entsize = section
        end = names.find(b"\0", name_off)
        name = names[name_off:end].decode("ascii", "replace") if end >= 0 else ""
        if sh_type != 4 or not name.startswith(".rela"):
            continue
        step = entsize or 24
        for pos in range(file_off, file_off + size, step):
            r_offset, r_info, r_addend = struct.unpack_from("<QQq", raw, pos)
            if (r_info & 0xFFFFFFFF) == 8:  # R_X86_64_RELATIVE
                relative[r_offset] = r_addend
    return loads, relative


def file_offset_to_va(loads, file_offset: int) -> int | None:
    for p_offset, p_vaddr, p_filesz in loads:
        if p_offset <= file_offset < p_offset + p_filesz:
            return p_vaddr + (file_offset - p_offset)
    return None


def string_vas(raw: bytes, loads, text: str) -> set[int]:
    needle = text.encode("utf-8") + b"\0"
    out = set()
    cursor = 0
    while True:
        found = raw.find(needle, cursor)
        if found < 0:
            break
        va = file_offset_to_va(loads, found)
        if va is not None:
            out.add(va)
        cursor = found + 1
    return out


def resolve_primary_vptr(raw: bytes, loads, relative, type_name: str, mangled: str) -> tuple[int, int]:
    if not string_vas(raw, loads, type_name):
        fail("TYPE_NAME_MISSING:" + type_name)
    mangled_vas = string_vas(raw, loads, mangled)
    if not mangled_vas:
        fail("MANGLED_TYPE_NAME_MISSING:" + type_name)
    typeinfos = {slot - 8 for slot, target in relative.items() if target in mangled_vas}
    candidates = set()
    for slot, target in relative.items():
        if target in typeinfos:
            vptr = slot + 8
            if vptr in relative:
                candidates.add((vptr, target))
    if len(candidates) != 1:
        fail("PRIMARY_VPTR_NOT_UNIQUE:" + type_name + ":" + str(sorted(candidates)))
    return next(iter(candidates))


if ticks() != START_TICKS:
    fail("START_TICKS_MISMATCH")
exe = Path(os.path.realpath(f"/proc/{PID}/exe"))
if exe.stat().st_size != EXPECTED_SIZE or digest(exe) != EXPECTED_SHA256:
    fail("EXACT_CLIENT_FENCE_MISMATCH")
raw = exe.read_bytes()
loads, relative = elf_layout(raw)

resolved = {}
for key, (type_name, mangled, required) in TYPES.items():
    try:
        vptr, typeinfo = resolve_primary_vptr(raw, loads, relative, type_name, mangled)
        resolved[key] = {"resolved": True, "vptr_offset": vptr, "typeinfo_offset": typeinfo}
    except SystemExit as exc:
        if required:
            raise
        resolved[key] = {"resolved": False, "reason": str(exc)}

regions = []
for line in Path(f"/proc/{PID}/maps").read_text(encoding="utf-8").splitlines():
    parts = line.split(maxsplit=5)
    begin, end = (int(value, 16) for value in parts[0].split("-"))
    regions.append((begin, end, parts[1], int(parts[2], 16), parts[5] if len(parts) == 6 else ""))
bases = [begin - file_off for begin, _end, _perms, file_off, path in regions if path == str(exe)]
if not bases:
    fail("CLIENT_MAPPING_MISSING")
base = min(bases)
heaps = [(begin, end) for begin, end, perms, _off, path in regions if path == "[heap]" and perms.startswith("rw")]
if len(heaps) != 1:
    fail("HEAP_MAPPING_COUNT=" + str(len(heaps)))
heap_begin, heap_end = heaps[0]
if heap_end - heap_begin > HEAP_SCAN_LIMIT:
    fail("HEAP_SCAN_BOUND_EXCEEDED")


def in_rw(address: int) -> bool:
    return any(begin <= address < end for begin, end, perms, _off, _path in regions if perms.startswith("rw"))

patterns = {
    key: struct.pack("<Q", base + int(data["vptr_offset"]))
    for key, data in resolved.items()
    if data.get("resolved")
}
hits = {key: [] for key in patterns}
fd = os.open(f"/proc/{PID}/mem", os.O_RDONLY | os.O_CLOEXEC)
try:
    cursor = heap_begin
    tail = b""
    while cursor < heap_end:
        want = min(8 * 1024 * 1024, heap_end - cursor)
        data = os.pread(fd, want, cursor)
        if len(data) != want:
            fail("PROC_MEM_SHORT_READ")
        merged = tail + data
        merged_base = cursor - len(tail)
        for key, pattern in patterns.items():
            pos = 0
            while True:
                found = merged.find(pattern, pos)
                if found < 0:
                    break
                address = merged_base + found
                if address % 8 == 0:
                    hits[key].append(address)
                pos = found + 1
        tail = merged[-7:]
        cursor += want
    for key in hits:
        hits[key] = sorted(set(hits[key]))
        resolved[key]["heap_vptr_hit_count"] = len(hits[key])

    game_hits = hits.get("game_client", [])
    if len(game_hits) != 1:
        fail("GAME_CLIENT_OBJECT_COUNT=" + str(len(game_hits)))
    auth_vptr = base + int(resolved["auth_controller"]["vptr_offset"])
    game = game_hits[0]
    game_bytes = os.pread(fd, AUTH_MEMBER_SCAN_LIMIT, game)
    if len(game_bytes) != AUTH_MEMBER_SCAN_LIMIT:
        fail("GAME_CLIENT_MEMBER_SCAN_SHORT_READ")
    auth_candidates = []
    for offset in range(0, AUTH_MEMBER_SCAN_LIMIT, 8):
        candidate = struct.unpack_from("<Q", game_bytes, offset)[0]
        if not candidate or not in_rw(candidate):
            continue
        try:
            candidate_vptr = struct.unpack("<Q", os.pread(fd, 8, candidate))[0]
        except (OSError, struct.error):
            continue
        if candidate_vptr == auth_vptr:
            auth_candidates.append((offset, candidate))
    if len(auth_candidates) != 1:
        fail("AUTH_CONTROLLER_MEMBER_NOT_UNIQUE=" + str([hex(item[0]) for item in auth_candidates]))
    auth_member_offset, auth_object = auth_candidates[0]

    qt_families = {
        "libQt6Core": "libQt6Core.so",
        "libQt6Network": "libQt6Network.so",
        "libQt6Qml": "libQt6Qml.so",
        "libQt6Quick": "libQt6Quick.so",
        "libQt6StateMachine": "libQt6StateMachine.so",
    }
    qt_paths = {}
    for _begin, _end, _perms, _off, path in regions:
        if not path:
            continue
        p = Path(path)
        if not p.is_file():
            continue
        for family, prefix in qt_families.items():
            if p.name.startswith(prefix):
                qt_paths[family] = p
    qt_fingerprints = {}
    for family in sorted(qt_paths):
        p = qt_paths[family]
        qt_fingerprints[family] = {"mapped_basename": p.name, "size": p.stat().st_size, "sha256": digest(p)}

    state_machine = qt_fingerprints.get("libQt6StateMachine")
    qstate_layout_known = bool(
        state_machine
        and state_machine["size"] == KNOWN_QT_STATE_MACHINE_SIZE
        and state_machine["sha256"] == KNOWN_QT_STATE_MACHINE_SHA256
    )
    auth_qstate_raw = None
    auth_running = None
    if qstate_layout_known:
        private = struct.unpack("<Q", os.pread(fd, 8, auth_object + QSTATE_PRIVATE_OFFSET))[0]
        if not private or not in_rw(private):
            fail("QSTATE_PRIVATE_POINTER_INVALID")
        auth_qstate_raw = struct.unpack("<I", os.pread(fd, 4, private + QSTATE_STATE_OFFSET))[0]
        if auth_qstate_raw not in (0, 1, 2):
            fail("QSTATE_LIFECYCLE_VALUE_UNEXPECTED")
        auth_running = auth_qstate_raw == QSTATE_RUNNING_VALUE
finally:
    os.close(fd)

if ticks() != START_TICKS:
    fail("START_TICKS_CHANGED_DURING_READ")

result = {
    "schema": "otclient.track-a.current-qt-world-snapshot.v1",
    "observed_epoch_ms": time.time_ns() // 1_000_000,
    "exact_client": {"size": EXPECTED_SIZE, "sha256": EXPECTED_SHA256, "start_ticks": START_TICKS},
    "resolved_types": resolved,
    "auth_relation": {
        "member_offset": auth_member_offset,
        "auth_controller_vptr_verified": True,
        "qstate_layout_known": qstate_layout_known,
        "auth_qstate_raw": auth_qstate_raw,
        "authentication_state_machine_running": auth_running,
    },
    "qt_libraries": qt_fingerprints,
    "process_memory_access": "read_only",
    "heap_bytes_retained": False,
    "raw_window_title_retained": False,
    "credentials_retained": False,
    "session_secrets_retained": False,
    "packet_payloads_retained": False,
    "process_environment_retained": False,
    "in_game_claimed": False,
    "semantic_promotion_performed": False,
}
print(json.dumps(result, sort_keys=True))
