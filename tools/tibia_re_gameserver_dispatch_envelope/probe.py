#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from dataclasses import dataclass
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP
from elftools.dwarf.callframe import FDE
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

TARGET_DISPATCH_ID = 0x34
CONTROL_TYPES = {
    0x14: 'GameserverMessageLoginError',
    0x17: 'GameserverMessageLoginSuccess',
    0x1F: 'GameserverMessageLoginChallenge',
}

SAFETY = {
    'runtime_access': 'none',
    'login_performed': False,
    'secret_access': False,
    'process_memory_access': False,
    'raw_client_uploaded': False,
}


@dataclass(frozen=True)
class Section:
    name: str
    offset: int
    size: int
    va: int
    flags: int


class Image:
    def __init__(self, path: Path):
        self.path = path
        self.raw = path.read_bytes()
        with path.open('rb') as fh:
            elf = ELFFile(fh)
            self.sections = [
                Section(
                    section.name,
                    int(section['sh_offset']),
                    int(section['sh_size']),
                    int(section['sh_addr']),
                    int(section['sh_flags']),
                )
                for section in elf.iter_sections()
                if int(section['sh_size'])
            ]
            self.rel: dict[int, int] = {}
            for section in elf.iter_sections():
                if not isinstance(section, RelocationSection):
                    continue
                for relocation in section.iter_relocations():
                    if relocation.is_RELA():
                        self.rel[int(relocation['r_offset'])] = (
                            int(relocation['r_addend']) & 0xFFFFFFFFFFFFFFFF
                        )
            dwarf = elf.get_dwarf_info()
            self.fdes = sorted(
                (
                    int(entry['initial_location']),
                    int(entry['initial_location']) + int(entry['address_range']),
                )
                for entry in dwarf.EH_CFI_entries()
                if isinstance(entry, FDE)
            )
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True

    def va_to_off(self, va: int) -> int:
        for section in self.sections:
            if section.va <= va < section.va + section.size:
                return section.offset + va - section.va
        raise ValueError(hex(va))

    def off_to_va(self, offset: int) -> int | None:
        for section in self.sections:
            if section.offset <= offset < section.offset + section.size:
                return section.va + offset - section.offset
        return None

    def mapped(self, va: int, size: int = 1) -> bool:
        try:
            offset = self.va_to_off(va)
        except ValueError:
            return False
        return 0 <= offset <= len(self.raw) - size

    def executable(self, va: int) -> bool:
        return any(
            (section.flags & 4) and section.va <= va < section.va + section.size
            for section in self.sections
        )

    def bytes(self, va: int, size: int) -> bytes:
        offset = self.va_to_off(va)
        return self.raw[offset:offset + size]

    def u64(self, va: int) -> int:
        return struct.unpack_from('<Q', self.raw, self.va_to_off(va))[0]

    def i32(self, va: int) -> int:
        return struct.unpack_from('<i', self.raw, self.va_to_off(va))[0]

    def qword(self, va: int) -> int:
        if va in self.rel:
            return self.rel[va]
        return self.u64(va)

    def fde(self, va: int) -> tuple[int, int] | None:
        matches = [row for row in self.fdes if row[0] <= va < row[1]]
        return matches[0] if len(matches) == 1 else None

    def occurrences(self, needle: bytes) -> list[int]:
        rows: list[int] = []
        start = 0
        while True:
            offset = self.raw.find(needle, start)
            if offset < 0:
                break
            va = self.off_to_va(offset)
            if va is not None:
                rows.append(va)
            start = offset + 1
        return rows


def reg_family(name: str) -> str:
    aliases = {
        'rax': 'ax', 'eax': 'ax', 'ax': 'ax', 'al': 'ax', 'ah': 'ax',
        'rbx': 'bx', 'ebx': 'bx', 'bx': 'bx', 'bl': 'bx', 'bh': 'bx',
        'rcx': 'cx', 'ecx': 'cx', 'cx': 'cx', 'cl': 'cx', 'ch': 'cx',
        'rdx': 'dx', 'edx': 'dx', 'dx': 'dx', 'dl': 'dx', 'dh': 'dx',
        'rsi': 'si', 'esi': 'si', 'si': 'si', 'sil': 'si',
        'rdi': 'di', 'edi': 'di', 'di': 'di', 'dil': 'di',
        'rbp': 'bp', 'ebp': 'bp', 'bp': 'bp', 'bpl': 'bp',
        'rsp': 'sp', 'esp': 'sp', 'sp': 'sp', 'spl': 'sp',
    }
    if name in aliases:
        return aliases[name]
    match = re.fullmatch(r'(r(?:8|9|1[0-5]))(?:d|w|b)?', name)
    return match.group(1) if match else name


def resolve_type_identities(img: Image) -> dict[int, str]:
    reverse: dict[int, list[int]] = {}
    for where, value in img.rel.items():
        reverse.setdefault(value, []).append(where)

    pattern = re.compile(rb'N5tibia8protobuf8protocol(\d+)(GameserverMessage[A-Za-z0-9_]*)E')
    mapping: dict[int, str] = {}
    for match in pattern.finditer(img.raw):
        name = match.group(2).decode('ascii')
        if int(match.group(1)) != len(name):
            continue
        name_va = img.off_to_va(match.start())
        if name_va is None:
            continue
        for name_slot in reverse.get(name_va, []):
            rtti = name_slot - 8
            for type_slot in reverse.get(rtti, []):
                address_point = type_slot + 8
                if not img.mapped(address_point - 16, 24):
                    continue
                if img.u64(address_point - 16) != 0:
                    continue
                first = img.qword(address_point)
                if not img.executable(first):
                    continue
                previous = mapping.get(address_point)
                if previous is not None and previous != name:
                    raise RuntimeError('ambiguous GameserverMessage RTTI mapping')
                mapping[address_point] = name
    if 'GameserverMessage' not in set(mapping.values()):
        raise RuntimeError('generic GameserverMessage RTTI not found')
    return mapping


def rip_refs_to(img: Image, target: int) -> list[int]:
    refs: list[int] = []
    for section in img.sections:
        if not (section.flags & 4):
            continue
        blob = img.raw[section.offset:section.offset + section.size]
        for pos in range(0, max(0, len(blob) - 7)):
            if not (0x40 <= blob[pos] <= 0x4F):
                continue
            if blob[pos + 1] not in (0x8D, 0x8B):
                continue
            if (blob[pos + 2] & 0xC7) != 0x05:
                continue
            displacement = int.from_bytes(blob[pos + 3:pos + 7], 'little', signed=True)
            site = section.va + pos
            if site + 7 + displacement == target:
                refs.append(site)
    return refs


def find_jump_table(img: Image, instructions: list) -> dict:
    candidates: list[dict] = []
    for index, ins in enumerate(instructions):
        if ins.mnemonic != 'jmp' or not ins.operands or ins.operands[0].type != X86_OP_REG:
            continue
        jump_reg = ins.operands[0].reg
        for mov_index in range(max(0, index - 8), index):
            mov = instructions[mov_index]
            if mov.mnemonic != 'movsxd' or len(mov.operands) < 2:
                continue
            if mov.operands[0].type != X86_OP_REG or mov.operands[0].reg != jump_reg:
                continue
            mem = mov.operands[1]
            if mem.type != X86_OP_MEM or mem.mem.scale != 4 or mem.mem.base == 0 or mem.mem.index == 0:
                continue
            table_reg = mem.mem.base
            index_reg = mem.mem.index
            add_ok = any(
                row.mnemonic == 'add'
                and len(row.operands) >= 2
                and row.operands[0].type == X86_OP_REG
                and row.operands[0].reg == jump_reg
                and row.operands[1].type == X86_OP_REG
                and row.operands[1].reg == table_reg
                for row in instructions[mov_index + 1:index]
            )
            if not add_ok:
                continue
            table = None
            for row in reversed(instructions[max(0, mov_index - 10):mov_index]):
                if row.mnemonic != 'lea' or len(row.operands) < 2:
                    continue
                if row.operands[0].type != X86_OP_REG or row.operands[0].reg != table_reg:
                    continue
                src = row.operands[1]
                if src.type == X86_OP_MEM and src.mem.base == X86_REG_RIP:
                    table = row.address + row.size + int(src.mem.disp)
                    break
            if table is None or not img.mapped(table, 4):
                continue
            index_family = reg_family(img.md.reg_name(index_reg))
            base_dispatch_id = None
            for row in reversed(instructions[max(0, mov_index - 20):mov_index]):
                if row.mnemonic != 'sub' or len(row.operands) < 2:
                    continue
                if row.operands[0].type != X86_OP_REG or row.operands[1].type != X86_OP_IMM:
                    continue
                if reg_family(img.md.reg_name(row.operands[0].reg)) == index_family:
                    base_dispatch_id = int(row.operands[1].imm) & 0xFF
                    break
            if base_dispatch_id is None:
                continue
            candidates.append({
                'table': table,
                'base_dispatch_id': base_dispatch_id,
                'jump_site': ins.address,
                'index_register': img.md.reg_name(index_reg),
            })
    unique = {
        (row['table'], row['base_dispatch_id'], row['jump_site']): row
        for row in candidates
    }
    if len(unique) != 1:
        raise RuntimeError(f'dispatch jump table ambiguous: {len(unique)}')
    return next(iter(unique.values()))


def resolve_dispatch_parser(img: Image, types: dict[int, str]) -> dict:
    generic_aps = [ap for ap, name in types.items() if name == 'GameserverMessage']
    if len(generic_aps) != 1:
        raise RuntimeError(f'generic GameserverMessage address point ambiguous: {len(generic_aps)}')
    refs = rip_refs_to(img, generic_aps[0])
    candidates: list[dict] = []
    seen_fdes: set[tuple[int, int]] = set()
    for ref in refs:
        fde = img.fde(ref)
        if fde is None or fde in seen_fdes:
            continue
        seen_fdes.add(fde)
        instructions = list(img.md.disasm(img.bytes(fde[0], fde[1] - fde[0]), fde[0]))
        try:
            jump = find_jump_table(img, instructions)
        except RuntimeError:
            continue
        candidates.append({
            'fde': fde,
            'generic_vtable_ref': ref,
            'instructions': instructions,
            **jump,
        })
    if len(candidates) != 1:
        raise RuntimeError(f'Gameserver dispatch parser ambiguous: {len(candidates)}')
    return candidates[0]


def resolve_dispatch_case(img: Image, parser: dict, dispatch_id: int) -> dict:
    index = dispatch_id - int(parser['base_dispatch_id'])
    if index < 0 or index > 0xFF:
        raise RuntimeError(f'dispatch id outside recovered table: {dispatch_id}')
    table = int(parser['table'])
    entry = table + index * 4
    if not img.mapped(entry, 4):
        raise RuntimeError('dispatch table entry unmapped')
    destination = table + img.i32(entry)
    fde = img.fde(destination)
    if fde is None:
        raise RuntimeError('dispatch destination has no unique FDE')
    instructions = list(img.md.disasm(img.bytes(fde[0], fde[1] - fde[0]), fde[0]))
    start_indexes = [i for i, row in enumerate(instructions) if row.address == destination]
    if len(start_indexes) != 1:
        raise RuntimeError('dispatch destination not instruction-aligned')
    start = start_indexes[0]
    window = instructions[start:start + 32]
    id_sites = [
        (i, row)
        for i, row in enumerate(window)
        if row.mnemonic == 'mov'
        and len(row.operands) >= 2
        and row.operands[0].type == X86_OP_REG
        and reg_family(img.md.reg_name(row.operands[0].reg)) == 'dx'
        and row.operands[1].type == X86_OP_IMM
        and (int(row.operands[1].imm) & 0xFFFFFFFF) == dispatch_id
    ]
    if len(id_sites) != 1:
        return {
            'dispatch_id': dispatch_id,
            'destination': destination,
            'classification': 'UNKNOWN_FALLBACK',
            'metadata': None,
        }
    id_index, _ = id_sites[0]
    metadata = None
    for row in reversed(window[max(0, id_index - 10):id_index]):
        if row.mnemonic != 'lea' or len(row.operands) < 2:
            continue
        if row.operands[0].type != X86_OP_REG or img.md.reg_name(row.operands[0].reg) != 'r8':
            continue
        src = row.operands[1]
        if src.type == X86_OP_MEM and src.mem.base == X86_REG_RIP:
            metadata = row.address + row.size + int(src.mem.disp)
            break
    if metadata is None or not img.mapped(metadata, 8):
        raise RuntimeError('concrete dispatch metadata not recovered')
    return {
        'dispatch_id': dispatch_id,
        'destination': destination,
        'classification': 'CONCRETE_TYPE',
        'metadata': metadata,
    }


def resolve_type_identity(img: Image, types: dict[int, str], case: dict) -> dict:
    if case['classification'] != 'CONCRETE_TYPE':
        return {**case, 'type_vtable_address_point': None, 'type_name': None}
    metadata = int(case['metadata'])
    address_point = img.qword(metadata)
    type_name = types.get(address_point)
    if type_name is None:
        raise RuntimeError('dispatch metadata vtable is not a recovered GameserverMessage type')
    return {
        **case,
        'type_vtable_address_point': address_point,
        'type_name': type_name,
    }


def sanitized_case(case: dict) -> dict:
    return {
        'dispatch_id': case['dispatch_id'],
        'classification': case['classification'],
        'destination': f"0x{case['destination']:x}",
        'metadata': f"0x{case['metadata']:x}" if case['metadata'] is not None else None,
        'type_vtable_address_point': (
            f"0x{case['type_vtable_address_point']:x}"
            if case.get('type_vtable_address_point') is not None else None
        ),
        'type_name': case.get('type_name'),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    img = Image(args.client)
    types = resolve_type_identities(img)
    dispatch_parser = resolve_dispatch_parser(img, types)

    controls = {}
    for dispatch_id, expected_type in CONTROL_TYPES.items():
        case = resolve_type_identity(
            img,
            types,
            resolve_dispatch_case(img, dispatch_parser, dispatch_id),
        )
        if case['classification'] != 'CONCRETE_TYPE' or case['type_name'] != expected_type:
            raise RuntimeError(
                f'control dispatch mismatch 0x{dispatch_id:02x}: '
                f"{case.get('type_name')} != {expected_type}"
            )
        controls[f'0x{dispatch_id:02x}'] = sanitized_case(case)

    target = resolve_type_identity(
        img,
        types,
        resolve_dispatch_case(img, dispatch_parser, TARGET_DISPATCH_ID),
    )

    result = {
        'schema': 'otclient.track-a.current-gameserver-dispatch-envelope.v1',
        **SAFETY,
        'client': {
            'sha256': hashlib.sha256(img.raw).hexdigest(),
            'size': len(img.raw),
        },
        'target_dispatch_id': TARGET_DISPATCH_ID,
        'gameserver_message_type_count': len(types),
        'dispatch_parser': {
            'fde': [f"0x{dispatch_parser['fde'][0]:x}", f"0x{dispatch_parser['fde'][1]:x}"],
            'generic_vtable_ref': f"0x{dispatch_parser['generic_vtable_ref']:x}",
            'jump_table': f"0x{dispatch_parser['table']:x}",
            'base_dispatch_id': dispatch_parser['base_dispatch_id'],
            'jump_site': f"0x{dispatch_parser['jump_site']:x}",
            'index_register': dispatch_parser['index_register'],
        },
        'controls': controls,
        'dispatch': sanitized_case(target),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('CURRENT_GAMESERVER_DISPATCH_ENVELOPE=PASS')
    print('TARGET_DISPATCH_CLASSIFICATION=' + target['classification'])
    if target.get('type_name'):
        print('TARGET_DISPATCH_TYPE=' + target['type_name'])
    print('RAW_CLIENT_UPLOADED=false')
    print('LOGIN_PERFORMED=false')
    print('SECRET_ACCESS=false')


if __name__ == '__main__':
    main()
