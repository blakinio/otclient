#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from collections import deque
from dataclasses import dataclass
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP, X86_REG_RSP
from elftools.dwarf.callframe import FDE
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

EXPECTED_SHA256 = 'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a'
EXPECTED_SIZE = 52105824
HANDLER_NAME = 'TLoginProtocolMessageHandler'
HANDLER_MANGLED = 'N5tibia14authentication28TLoginProtocolMessageHandlerE'
HANDLER_VTABLE_AP = 0x30B6700
HANDLER_SLOT = 0x60
HANDLER_SLOT_TARGET = 0xE25620
HANDLER_OWNER_FIELD = 0x9C0

SAFETY = {
    'runtime_access': 'none',
    'official_client_executed': False,
    'login_performed': False,
    'secret_access': False,
    'process_memory_access': False,
    'packet_capture': False,
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
        self.raw = path.read_bytes()
        with path.open('rb') as fh:
            elf = ELFFile(fh)
            self.sections = [
                Section(s.name, int(s['sh_offset']), int(s['sh_size']), int(s['sh_addr']), int(s['sh_flags']))
                for s in elf.iter_sections() if int(s['sh_size'])
            ]
            self.rel: dict[int, int] = {}
            for sec in elf.iter_sections():
                if isinstance(sec, RelocationSection):
                    for rel in sec.iter_relocations():
                        if rel.is_RELA():
                            self.rel[int(rel['r_offset'])] = int(rel['r_addend']) & 0xFFFFFFFFFFFFFFFF
            dwarf = elf.get_dwarf_info()
            self.fdes = sorted(
                (int(e['initial_location']), int(e['initial_location']) + int(e['address_range']))
                for e in dwarf.EH_CFI_entries() if isinstance(e, FDE)
            )
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True

    def va_to_off(self, va: int) -> int:
        for s in self.sections:
            if s.va <= va < s.va + s.size:
                return s.offset + va - s.va
        raise ValueError(hex(va))

    def off_to_va(self, off: int) -> int | None:
        for s in self.sections:
            if s.offset <= off < s.offset + s.size:
                return s.va + off - s.offset
        return None

    def mapped(self, va: int, size: int = 1) -> bool:
        try:
            off = self.va_to_off(va)
        except ValueError:
            return False
        return 0 <= off <= len(self.raw) - size

    def executable(self, va: int) -> bool:
        return any((s.flags & 4) and s.va <= va < s.va + s.size for s in self.sections)

    def bytes(self, va: int, size: int) -> bytes:
        off = self.va_to_off(va)
        return self.raw[off:off + size]

    def u64(self, va: int) -> int:
        return struct.unpack_from('<Q', self.raw, self.va_to_off(va))[0]

    def qword(self, va: int) -> int:
        return self.rel.get(va, self.u64(va))

    def fde(self, va: int) -> tuple[int, int] | None:
        rows = [row for row in self.fdes if row[0] <= va < row[1]]
        return rows[0] if len(rows) == 1 else None

    def instructions(self, fde: tuple[int, int]):
        return list(self.md.disasm(self.bytes(fde[0], fde[1] - fde[0]), fde[0]))

    def occurrences(self, needle: bytes) -> list[int]:
        rows: list[int] = []
        start = 0
        while True:
            off = self.raw.find(needle, start)
            if off < 0:
                return rows
            va = self.off_to_va(off)
            if va is not None:
                rows.append(va)
            start = off + 1


def hx(value: int | None) -> str | None:
    return None if value is None else f'0x{value:x}'


def reg_family(name: str) -> str:
    aliases = {
        'rax': 'rax', 'eax': 'rax', 'ax': 'rax', 'al': 'rax', 'ah': 'rax',
        'rbx': 'rbx', 'ebx': 'rbx', 'bx': 'rbx', 'bl': 'rbx', 'bh': 'rbx',
        'rcx': 'rcx', 'ecx': 'rcx', 'cx': 'rcx', 'cl': 'rcx', 'ch': 'rcx',
        'rdx': 'rdx', 'edx': 'rdx', 'dx': 'rdx', 'dl': 'rdx', 'dh': 'rdx',
        'rsi': 'rsi', 'esi': 'rsi', 'si': 'rsi', 'sil': 'rsi',
        'rdi': 'rdi', 'edi': 'rdi', 'di': 'rdi', 'dil': 'rdi',
        'rbp': 'rbp', 'ebp': 'rbp', 'bp': 'rbp', 'bpl': 'rbp',
        'rsp': 'rsp', 'esp': 'rsp', 'sp': 'rsp', 'spl': 'rsp',
    }
    if name in aliases:
        return aliases[name]
    m = re.fullmatch(r'(r(?:8|9|1[0-5]))(?:d|w|b)?', name)
    return m.group(1) if m else name


def writes_family(img: Image, ins, family: str) -> bool:
    try:
        _reads, writes = ins.regs_access()
    except Exception:
        return False
    return family in {reg_family(img.md.reg_name(reg)) for reg in writes}


def rip_target(ins) -> int | None:
    for op in ins.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return ins.address + ins.size + int(op.mem.disp)
    return None


def verify_promoted_target(img: Image) -> dict:
    if hashlib.sha256(img.raw).hexdigest() != EXPECTED_SHA256 or len(img.raw) != EXPECTED_SIZE:
        raise RuntimeError('exact current client fence mismatch')
    if img.qword(HANDLER_VTABLE_AP + HANDLER_SLOT) != HANDLER_SLOT_TARGET:
        raise RuntimeError('promoted handler slot target mismatch')

    # Re-assert RTTI identity rather than trusting the promoted absolute address alone.
    names = img.occurrences(HANDLER_MANGLED.encode('ascii'))
    if not names:
        raise RuntimeError('TLoginProtocolMessageHandler RTTI name missing')
    rtti_match = False
    reverse: dict[int, list[int]] = {}
    for where, value in img.rel.items():
        reverse.setdefault(value, []).append(where)
    for name_va in names:
        for name_slot in reverse.get(name_va, []):
            rtti = name_slot - 8
            for type_slot in reverse.get(rtti, []):
                if type_slot + 8 == HANDLER_VTABLE_AP:
                    rtti_match = True
    if not rtti_match:
        raise RuntimeError('promoted handler vtable does not match exact RTTI')
    return {
        'handler_type': HANDLER_NAME,
        'handler_vtable_address_point': hx(HANDLER_VTABLE_AP),
        'slot': hx(HANDLER_SLOT),
        'slot_0x60_target': hx(HANDLER_SLOT_TARGET),
    }


def build_predecessors(instructions) -> dict[int, set[int]]:
    by = {row.address: row for row in instructions}
    pred = {row.address: set() for row in instructions}
    for index, row in enumerate(instructions):
        nxt = instructions[index + 1].address if index + 1 < len(instructions) else None
        successors: set[int] = set()
        mnemonic = row.mnemonic.lower()
        if mnemonic.startswith('ret'):
            pass
        elif mnemonic == 'jmp':
            if row.operands and row.operands[0].type == X86_OP_IMM:
                target = int(row.operands[0].imm)
                if target in by:
                    successors.add(target)
        elif mnemonic.startswith('j'):
            if row.operands and row.operands[0].type == X86_OP_IMM:
                target = int(row.operands[0].imm)
                if target in by:
                    successors.add(target)
            if nxt is not None:
                successors.add(nxt)
        else:
            if nxt is not None:
                successors.add(nxt)
        for target in successors:
            pred[target].add(row.address)
    return pred


def mem_shape(img: Image, op) -> tuple[str | None, int, int, int]:
    base = reg_family(img.md.reg_name(op.mem.base)) if op.mem.base else None
    index = reg_family(img.md.reg_name(op.mem.index)) if op.mem.index else None
    return base, int(op.mem.disp), int(op.mem.scale), 0 if index is None else hash(index)


def previous_in_block(instructions, site_index: int, limit: int = 80):
    # Conservative local window: stop at unconditional/conditional branch boundaries.
    out = []
    for row in reversed(instructions[max(0, site_index - limit):site_index]):
        if row.mnemonic.lower().startswith('j') or row.mnemonic.lower().startswith('ret'):
            break
        out.append(row)
    return out


def trace_register_origin(img: Image, instructions, site_index: int, family: str) -> dict:
    current = family
    depth = 0
    for row in previous_in_block(instructions, site_index, limit=120):
        if not writes_family(img, row, current):
            continue
        if not row.operands or row.operands[0].type != X86_OP_REG:
            return {'classification': 'REGISTER_ORIGIN_UNKNOWN', 'at': hx(row.address), 'operand': row.op_str}
        if len(row.operands) < 2:
            return {'classification': 'REGISTER_ORIGIN_UNKNOWN', 'at': hx(row.address), 'operand': row.op_str}
        src = row.operands[1]
        if row.mnemonic == 'mov' and src.type == X86_OP_REG:
            current = reg_family(img.md.reg_name(src.reg))
            depth += 1
            if depth > 12:
                return {'classification': 'REGISTER_ALIAS_DEPTH_EXCEEDED'}
            continue
        if row.mnemonic == 'mov' and src.type == X86_OP_MEM:
            base = reg_family(img.md.reg_name(src.mem.base)) if src.mem.base else None
            return {
                'classification': 'MEMORY_LOAD',
                'at': hx(row.address),
                'operand': row.op_str,
                'base_family': base,
                'displacement': int(src.mem.disp),
            }
        if row.mnemonic == 'lea' and src.type == X86_OP_MEM and src.mem.base == X86_REG_RIP:
            return {
                'classification': 'RIP_LEA',
                'at': hx(row.address),
                'operand': row.op_str,
                'target': hx(row.address + row.size + int(src.mem.disp)),
            }
        return {'classification': 'REGISTER_DEFINITION', 'at': hx(row.address), 'operand': row.op_str}
    return {'classification': 'REGISTER_REACHES_BLOCK_ENTRY', 'register_family': current}


def find_vtable_store_for_object(img: Image, instructions, call_index: int, object_family: str) -> dict | None:
    # Accept only an explicit write of the promoted vtable AP to [object+0].
    window = instructions[max(0, call_index - 140):call_index]
    for i, row in enumerate(window):
        if row.mnemonic != 'lea' or len(row.operands) < 2 or row.operands[0].type != X86_OP_REG:
            continue
        if rip_target(row) != HANDLER_VTABLE_AP:
            continue
        vt_family = reg_family(img.md.reg_name(row.operands[0].reg))
        for later in window[i + 1:i + 12]:
            if later.mnemonic != 'mov' or len(later.operands) < 2:
                continue
            dst, src = later.operands[0], later.operands[1]
            if dst.type != X86_OP_MEM or src.type != X86_OP_REG:
                continue
            if int(dst.mem.disp) != 0:
                continue
            base = reg_family(img.md.reg_name(dst.mem.base)) if dst.mem.base else None
            source = reg_family(img.md.reg_name(src.reg))
            if base == object_family and source == vt_family:
                return {
                    'classification': 'EXPLICIT_HANDLER_VTABLE_STORE',
                    'vtable_load_site': hx(row.address),
                    'store_site': hx(later.address),
                }
    return None


def bind_callsite_owner(img: Image, instructions, call_index: int) -> dict:
    call = instructions[call_index]
    mem = call.operands[0]
    vtable_family = reg_family(img.md.reg_name(mem.mem.base))
    # Find the load of the vtable register from [object].
    object_family = None
    vtable_load = None
    for row in previous_in_block(instructions, call_index, limit=40):
        if not writes_family(img, row, vtable_family):
            continue
        if row.mnemonic == 'mov' and len(row.operands) >= 2 and row.operands[1].type == X86_OP_MEM:
            src = row.operands[1]
            if int(src.mem.disp) == 0 and src.mem.base:
                object_family = reg_family(img.md.reg_name(src.mem.base))
                vtable_load = row
        break
    if object_family is None or vtable_load is None:
        return {'classification': 'NO_LOCAL_VTABLE_LOAD'}

    vt_index = next(i for i, row in enumerate(instructions) if row.address == vtable_load.address)
    origin = trace_register_origin(img, instructions, vt_index, object_family)
    explicit_store = find_vtable_store_for_object(img, instructions, call_index, object_family)

    if origin.get('classification') == 'MEMORY_LOAD' and origin.get('displacement') == HANDLER_OWNER_FIELD:
        return {
            'classification': 'BOUND_HANDLER_OWNER_FIELD',
            'object_register_family': object_family,
            'vtable_load_site': hx(vtable_load.address),
            'origin': origin,
        }
    if explicit_store is not None:
        return {
            'classification': 'BOUND_HANDLER_EXPLICIT_VTABLE',
            'object_register_family': object_family,
            'vtable_load_site': hx(vtable_load.address),
            'origin': origin,
            'vtable_evidence': explicit_store,
        }
    return {
        'classification': 'UNBOUND_RECEIVER',
        'object_register_family': object_family,
        'vtable_load_site': hx(vtable_load.address),
        'origin': origin,
    }


def enumerate_slot_calls(img: Image) -> list[dict]:
    rows = []
    for fde in img.fdes:
        if not img.executable(fde[0]) or fde[1] - fde[0] > 0x20000:
            continue
        instructions = img.instructions(fde)
        for index, ins in enumerate(instructions):
            if ins.mnemonic != 'call' or not ins.operands or ins.operands[0].type != X86_OP_MEM:
                continue
            mem = ins.operands[0]
            if int(mem.mem.disp) != HANDLER_SLOT or not mem.mem.base:
                continue
            binding = bind_callsite_owner(img, instructions, index)
            rows.append({
                'site': ins.address,
                'fde': fde,
                'operand': ins.op_str,
                'binding': binding,
                '_instructions': instructions,
                '_index': index,
            })
    return rows


def scalar_definition(img: Image, row, family: str) -> dict | None:
    if not writes_family(img, row, family):
        return None
    if row.mnemonic == 'mov' and len(row.operands) >= 2 and row.operands[0].type == X86_OP_REG:
        src = row.operands[1]
        if src.type == X86_OP_IMM:
            return {'kind': 'IMM', 'value': int(src.imm) & 0xFFFFFFFF, 'site': row.address, 'operand': row.op_str}
    if row.mnemonic == 'xor' and len(row.operands) >= 2 and row.operands[0].type == X86_OP_REG and row.operands[1].type == X86_OP_REG:
        a = reg_family(img.md.reg_name(row.operands[0].reg))
        b = reg_family(img.md.reg_name(row.operands[1].reg))
        if a == family and b == family:
            return {'kind': 'IMM', 'value': 0, 'site': row.address, 'operand': row.op_str}
    return {'kind': 'NONSCALAR', 'site': row.address, 'operand': row.op_str}


def reaching_edx(img: Image, instructions, call_index: int) -> dict:
    callsite = instructions[call_index].address
    pred = build_predecessors(instructions)
    by = {row.address: row for row in instructions}
    queue = deque(pred[callsite])
    visited: set[int] = set()
    definitions: dict[int, dict] = {}
    clobbered_paths = 0
    entry_paths = 0
    while queue:
        address = queue.popleft()
        if address in visited:
            continue
        visited.add(address)
        row = by[address]
        definition = scalar_definition(img, row, 'rdx')
        if definition is not None:
            definitions[address] = definition
            continue
        if row.mnemonic == 'call':
            # SysV caller-saved RDX is no longer a valid reaching value across a call.
            clobbered_paths += 1
            continue
        preds = pred.get(address, set())
        if not preds:
            entry_paths += 1
        else:
            queue.extend(preds)

    rows = [definitions[key] for key in sorted(definitions)]
    scalar_values = {row['value'] for row in rows if row['kind'] == 'IMM'}
    non_scalar = any(row['kind'] != 'IMM' for row in rows)
    if len(scalar_values) == 1 and not non_scalar and not clobbered_paths and not entry_paths:
        value = next(iter(scalar_values))
        classification = 'UNIQUE_STATIC_SCALAR'
    else:
        value = None
        classification = 'VALUE_NOT_UNIQUELY_PROVEN'
    return {
        'classification': classification,
        'value': value,
        'definitions': [
            {**row, 'site': hx(row['site'])}
            for row in rows
        ],
        'clobbered_paths': clobbered_paths,
        'entry_paths': entry_paths,
        'visited_instruction_count': len(visited),
    }


def sanitize_candidate(row: dict) -> dict:
    return {
        'site': hx(row['site']),
        'fde': [hx(row['fde'][0]), hx(row['fde'][1])],
        'operand': row['operand'],
        'binding': row['binding'],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    img = Image(args.client)
    promoted = verify_promoted_target(img)
    calls = enumerate_slot_calls(img)
    bound = [row for row in calls if row['binding']['classification'].startswith('BOUND_HANDLER_')]

    edx = None
    accepted = None
    if len(bound) == 1:
        accepted = bound[0]
        edx = reaching_edx(img, accepted['_instructions'], accepted['_index'])

    if accepted is not None and edx is not None and edx['classification'] == 'UNIQUE_STATIC_SCALAR':
        classification = 'FIELD6_VALUE_PROVEN'
        field6_value = edx['value']
        owner_marker = 'PROVEN'
        value_marker = str(field6_value)
    else:
        classification = 'FIELD6_VALUE_UNKNOWN'
        field6_value = None
        owner_marker = 'PROVEN' if len(bound) == 1 else 'UNKNOWN'
        value_marker = 'UNKNOWN'

    result = {
        'schema': 'otclient.track-a.current-login-field6-callsite-owner.v1',
        **SAFETY,
        'exact_client': {
            'sha256': hashlib.sha256(img.raw).hexdigest(),
            'size': len(img.raw),
        },
        'promoted_target': promoted,
        'slot_callsite_count': len(calls),
        'bound_handler_callsite_count': len(bound),
        'bound_handler_callsites': [sanitize_candidate(row) for row in bound],
        'accepted_callsite': sanitize_candidate(accepted) if accepted is not None else None,
        'field6_edx_reaching_value': edx,
        'field6_value': field6_value,
        'classification': classification,
        'boundary': 'NO_HEURISTIC_RANKING_IF_RECEIVER_OR_VALUE_IS_NOT_UNIQUE',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    print('CURRENT_LOGIN_FIELD6_CALLSITE_OWNER=PASS')
    print('FIELD6_CALLSITE_OWNER=' + owner_marker)
    print('FIELD6_EDX_REACHING_VALUE=' + value_marker)
    print('CLASSIFICATION=' + classification)
    print('RAW_CLIENT_UPLOADED=false')
    print('OFFICIAL_CLIENT_EXECUTED=false')
    print('PROCESS_MEMORY_ACCESS=false')


if __name__ == '__main__':
    main()
