#!/usr/bin/env python3
"""Exact-current static QMeta recovery for TPlayerProtocolMessageHandler::worldEntered."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import struct
import sys

SHF_ALLOC = 0x2
SHF_EXECINSTR = 0x4
TARGET_CLASS = "tibia::game::TPlayerProtocolMessageHandler"
TARGET_METHOD = "worldEntered"
EXPECTED_SIZE = 52_105_824
EXPECTED_SHA256 = "d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a"


class AnchorError(RuntimeError):
    pass


def _va_to_offset(sections, va: int) -> int:
    for addr, file_offset, size, _flags in sections:
        if addr <= va < addr + size:
            return file_offset + va - addr
    raise AnchorError(f"VA_NOT_MAPPED:{va:#x}")


def _offset_to_va(sections, offset: int) -> int | None:
    for addr, file_offset, size, _flags in sections:
        if file_offset <= offset < file_offset + size:
            return addr + offset - file_offset
    return None


def _u32(raw: bytes, sections, va: int) -> int:
    offset = _va_to_offset(sections, va)
    if offset + 4 > len(raw):
        raise AnchorError(f"U32_OUT_OF_RANGE:{va:#x}")
    return struct.unpack_from("<I", raw, offset)[0]


def _qstring(raw: bytes, sections, base: int, index: int) -> str:
    relative = _u32(raw, sections, base + index * 8)
    length = _u32(raw, sections, base + index * 8 + 4)
    start = _va_to_offset(sections, base + relative)
    end = start + length
    if end > len(raw):
        raise AnchorError("QSTRING_OUT_OF_RANGE")
    try:
        return raw[start:end].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AnchorError("QSTRING_UTF8_INVALID") from exc


def _is_executable(sections, va: int) -> bool:
    return any(
        (flags & SHF_EXECINSTR) and addr <= va < addr + size
        for addr, _file_offset, size, flags in sections
    )


def _stringdata_candidates(raw: bytes, sections, class_name: str) -> list[int]:
    needle = class_name.encode("utf-8")
    candidates: set[int] = set()
    cursor = 0
    while True:
        found = raw.find(needle, cursor)
        if found < 0:
            break
        class_va = _offset_to_va(sections, found)
        if class_va is not None:
            lower = max(0, found - 0x4000)
            for base_offset in range(lower, found + 1, 4):
                base_va = _offset_to_va(sections, base_offset)
                if base_va is None or base_offset + 8 > len(raw):
                    continue
                relative, length = struct.unpack_from("<II", raw, base_offset)
                if length == len(needle) and base_va + relative == class_va:
                    candidates.add(base_va)
        cursor = found + 1
    return sorted(candidates)


def recover_world_entered_anchor(raw: bytes, sections, relocs: dict[int, int]) -> dict[str, object]:
    stringdata_candidates = _stringdata_candidates(raw, sections, TARGET_CLASS)
    qmeta_candidates = []
    for stringdata in stringdata_candidates:
        try:
            if _qstring(raw, sections, stringdata, 0) != TARGET_CLASS:
                continue
        except AnchorError:
            continue
        for slot, target in relocs.items():
            if target != stringdata or slot < 8:
                continue
            static_meta = slot - 8
            metadata = relocs.get(static_meta + 16)
            static_metacall = relocs.get(static_meta + 24)
            if metadata is None or static_metacall is None:
                continue
            if not _is_executable(sections, static_metacall):
                continue
            try:
                header = [_u32(raw, sections, metadata + index * 4) for index in range(14)]
                method_count = header[4]
                method_data = header[5]
                signal_count = header[13]
                if method_count <= 0 or method_count > 4096:
                    continue
                if signal_count < 0 or signal_count > method_count:
                    continue
                method_names = []
                methods = []
                for method_index in range(method_count):
                    row_va = metadata + (method_data + method_index * 6) * 4
                    row = [_u32(raw, sections, row_va + field * 4) for field in range(6)]
                    name = _qstring(raw, sections, stringdata, row[0])
                    method_names.append(name)
                    methods.append((method_index, name, row[1], row[4]))
            except AnchorError:
                continue
            qmeta_candidates.append(
                (static_meta, stringdata, metadata, static_metacall, method_count, signal_count, method_names, methods)
            )

    unique = {candidate[:4]: candidate for candidate in qmeta_candidates}
    if len(unique) != 1:
        raise AnchorError(f"TARGET_QMETA_NOT_UNIQUE:{sorted(unique)}")
    candidate = next(iter(unique.values()))
    static_meta, stringdata, metadata, static_metacall, method_count, signal_count, method_names, methods = candidate
    world_methods = [method for method in methods if method[1] == TARGET_METHOD]
    if len(world_methods) != 1:
        raise AnchorError(f"WORLD_ENTERED_NOT_UNIQUE:{len(world_methods)}")
    method_index, _name, argc, flags = world_methods[0]
    if argc != 0:
        raise AnchorError(f"WORLD_ENTERED_ARGC_UNEXPECTED:{argc}")
    if method_index >= signal_count:
        raise AnchorError(f"WORLD_ENTERED_NOT_SIGNAL:{method_index}>={signal_count}")

    return {
        "class_name": TARGET_CLASS,
        "static_metaobject_va": static_meta,
        "stringdata_va": stringdata,
        "metadata_va": metadata,
        "static_metacall_va": static_metacall,
        "method_count": method_count,
        "signal_count": signal_count,
        "method_names": method_names,
        "world_entered_method_index": method_index,
        "world_entered_argc": argc,
        "world_entered_flags": flags,
        "world_entered_is_signal": True,
    }


def parse_elf_layout(raw: bytes):
    if raw[:4] != b"\x7fELF" or raw[4] != 2 or raw[5] != 1:
        raise AnchorError("ELF64_LITTLE_ENDIAN_REQUIRED")
    shoff = struct.unpack_from("<Q", raw, 0x28)[0]
    shentsize = struct.unpack_from("<H", raw, 0x3A)[0]
    shnum = struct.unpack_from("<H", raw, 0x3C)[0]
    if shentsize < 64 or shoff + shentsize * shnum > len(raw):
        raise AnchorError("ELF_SECTION_TABLE_INVALID")

    section_rows = []
    sections = []
    for index in range(shnum):
        offset = shoff + index * shentsize
        row = struct.unpack_from("<IIQQQQIIQQ", raw, offset)
        section_rows.append(row)
        _name, sh_type, flags, addr, file_offset, size, _link, _info, _align, entsize = row
        if (flags & SHF_ALLOC) and sh_type != 8 and file_offset + size <= len(raw):
            sections.append((addr, file_offset, size, flags))

    relocs: dict[int, int] = {}
    for row in section_rows:
        _name, sh_type, _flags, _addr, file_offset, size, _link, _info, _align, entsize = row
        if sh_type != 4:
            continue
        step = entsize or 24
        for offset in range(file_offset, file_offset + size, step):
            if offset + 24 > len(raw):
                raise AnchorError("ELF_RELA_OUT_OF_RANGE")
            r_offset, r_info, r_addend = struct.unpack_from("<QQq", raw, offset)
            if (r_info & 0xFFFFFFFF) != 8:  # R_X86_64_RELATIVE
                continue
            previous = relocs.get(r_offset)
            if previous is not None and previous != r_addend:
                raise AnchorError(f"ELF_RELA_CONFLICT:{r_offset:#x}")
            relocs[r_offset] = r_addend
    if not sections or not relocs:
        raise AnchorError("ELF_LAYOUT_INCOMPLETE")
    return sections, relocs


def _i32(raw: bytes, sections, va: int) -> int:
    offset = _va_to_offset(sections, va)
    if offset + 4 > len(raw):
        raise AnchorError(f"I32_OUT_OF_RANGE:{va:#x}")
    return struct.unpack_from("<i", raw, offset)[0]


def recover_dispatch_case(raw: bytes, sections, anchor: dict[str, object]) -> dict[str, object]:
    try:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86_const import X86_OP_MEM, X86_REG_RIP
    except ImportError as exc:
        raise AnchorError("CAPSTONE_REQUIRED_FOR_DISPATCH_RECOVERY") from exc

    static_metacall = int(anchor["static_metacall_va"])
    method_count = int(anchor["method_count"])
    method_index = int(anchor["world_entered_method_index"])
    code_offset = _va_to_offset(sections, static_metacall)
    code = raw[code_offset : min(len(raw), code_offset + 0x1000)]
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    instructions = list(md.disasm(code, static_metacall))
    candidates = []
    for pos, inst in enumerate(instructions):
        if inst.mnemonic != "lea" or len(inst.operands) < 2:
            continue
        memory = inst.operands[1]
        if memory.type != X86_OP_MEM or memory.mem.base != X86_REG_RIP:
            continue
        table = inst.address + inst.size + memory.mem.disp
        register = inst.operands[0].reg
        used_as_scaled_table = False
        for nxt in instructions[pos + 1 : pos + 12]:
            for operand in nxt.operands:
                if operand.type == X86_OP_MEM and operand.mem.base == register and operand.mem.scale == 4:
                    used_as_scaled_table = True
        if not used_as_scaled_table:
            continue
        try:
            targets = [table + _i32(raw, sections, table + index * 4) for index in range(method_count)]
        except AnchorError:
            continue
        if not all(_is_executable(sections, target) for target in targets):
            continue
        context = instructions[max(0, pos - 12) : pos + 3]
        normalized = [(item.mnemonic, item.op_str.replace(" ", "")) for item in context]
        invoke_guard = any(mnemonic == "test" and operands == "esi,esi" for mnemonic, operands in normalized)
        invoke_guard |= any(mnemonic == "cmp" and operands in ("esi,0", "esi,0x0") for mnemonic, operands in normalized)
        range_tokens = (f"edx,{method_count - 1}", f"edx,0x{method_count - 1:x}")
        full_range = any(mnemonic == "cmp" and operands in range_tokens for mnemonic, operands in normalized)
        if invoke_guard and full_range:
            candidates.append((table, targets, inst.address))

    unique = {(table, lea): (table, targets, lea) for table, targets, lea in candidates}
    if len(unique) != 1:
        raise AnchorError(f"FULL_RANGE_DISPATCH_NOT_UNIQUE:{sorted(unique)}")
    table, targets, lea = next(iter(unique.values()))
    target = targets[method_index]
    target_offset = _va_to_offset(sections, target)
    window = raw[target_offset : min(len(raw), target_offset + 64)]
    if len(window) < 32:
        raise AnchorError("WORLD_ENTERED_TARGET_WINDOW_TOO_SHORT")
    return {
        "dispatch_lea_va": lea,
        "dispatch_table_va": table,
        "world_entered_dispatch_target_va": target,
        "world_entered_target_window_sha256": hashlib.sha256(window).hexdigest(),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        raise SystemExit("usage: track_a_current_world_entered_anchor.py CLIENT OUTPUT_JSON")
    client = Path(argv[1])
    output = Path(argv[2])
    raw = client.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or actual_sha != EXPECTED_SHA256:
        raise AnchorError(f"EXACT_CLIENT_FENCE_MISMATCH:{len(raw)}:{actual_sha}")

    sections, relocs = parse_elf_layout(raw)
    anchor = recover_world_entered_anchor(raw, sections, relocs)
    dispatch = recover_dispatch_case(raw, sections, anchor)
    document = {
        "schema": "otclient.track-a.current-world-entered-anchor.v1",
        "classification": "STATIC_QMETA_DISPATCH_ANCHOR_NOT_RUNTIME_PROMOTED",
        "exact_client": {
            "version": "15.32.75d4a0",
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
        },
        "anchor": {**anchor, **dispatch},
        "safety": {
            "runtime_access": "none",
            "client_executed": False,
            "raw_client_retained": False,
            "historical_address_reuse": False,
            "credentials_accessed": False,
            "session_secrets_accessed": False,
            "packet_payloads_captured": False,
            "in_game_claimed": False,
            "semantic_promotion_performed": False,
        },
    }
    output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("WORLD_ENTERED_STATIC_ANCHOR=PASS")
    print(f"WORLD_ENTERED_METHOD_INDEX={anchor['world_entered_method_index']}")
    print(f"WORLD_ENTERED_DISPATCH_TARGET=0x{dispatch['world_entered_dispatch_target_va']:x}")
    print("HISTORICAL_ADDRESS_REUSE=false")
    print("RAW_CLIENT_RETAINED=false")
    print("IN_GAME_CLAIMED=false")
    print("SEMANTIC_PROMOTION_PERFORMED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
