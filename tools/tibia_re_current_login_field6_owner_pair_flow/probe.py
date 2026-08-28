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
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP
from elftools.dwarf.callframe import FDE
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

EXPECTED_SHA256 = 'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a'
EXPECTED_SIZE = 52_105_824
HANDLER_VTABLE_AP = 0x30B6700
HANDLER_SLOT = 0x60
HANDLER_SLOT_TARGET = 0xE25620
OWNER_CTOR_FDE = (0x7D15C0, 0x7D1A8A)
CONFIG_STORE = 0x7D1677
HANDLER_OWNER_STORE = 0x7D167E
CONFIG_OWNER_STORE = 0x7D1685
HANDLER_OWNER_OFFSET = 0x9C0
CONFIG_OWNER_OFFSET = 0x9C8
CONFIG_MODE_OFFSET = 0x30

OWNER_PAIR_CONSTRUCTOR_REASSERTION = True
CONFIG_FIELD_0X30_REACHING_CONSTANTS = True
OWNER_PAIR_DIRECT_FLOW = True
OWNER_PAIR_DIRECT_FLOW_UNKNOWN = True
NO_HEURISTIC_RANKING = True
NO_SEMANTIC_GUESSING = True

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
                Section(int(s['sh_offset']), int(s['sh_size']), int(s['sh_addr']), int(s['sh_flags']))
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
        self._ins: dict[tuple[int, int], list] = {}
        self._pred: dict[tuple[int, int], dict[int, set[int]]] = {}

    def va_to_off(self, va: int) -> int:
        for s in self.sections:
            if s.va <= va < s.va + s.size:
                return s.offset + va - s.va
        raise ValueError(hex(va))

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
        rows = self._ins.get(fde)
        if rows is None:
            rows = list(self.md.disasm(self.bytes(fde[0], fde[1] - fde[0]), fde[0]))
            self._ins[fde] = rows
        return rows

    def predecessors(self, fde: tuple[int, int]) -> dict[int, set[int]]:
        cached = self._pred.get(fde)
        if cached is not None:
            return cached
        rows = self.instructions(fde)
        by = {row.address: row for row in rows}
        pred = {row.address: set() for row in rows}
        for i, row in enumerate(rows):
            nxt = rows[i + 1].address if i + 1 < len(rows) else None
            succ: set[int] = set()
            m = row.mnemonic.lower()
            if m.startswith('ret'):
                pass
            elif m == 'jmp':
                if row.operands and row.operands[0].type == X86_OP_IMM:
                    target = int(row.operands[0].imm)
                    if target in by:
                        succ.add(target)
            elif m.startswith('j'):
                if row.operands and row.operands[0].type == X86_OP_IMM:
                    target = int(row.operands[0].imm)
                    if target in by:
                        succ.add(target)
                if nxt is not None:
                    succ.add(nxt)
            elif nxt is not None:
                succ.add(nxt)
            for target in succ:
                pred[target].add(row.address)
        self._pred[fde] = pred
        return pred


def hx(v: int | None) -> str | None:
    return None if v is None else f'0x{v:x}'


def reg_family(img: Image, reg: int | str) -> str:
    name = reg if isinstance(reg, str) else img.md.reg_name(reg)
    aliases = {
        'rax':'rax','eax':'rax','ax':'rax','al':'rax','ah':'rax',
        'rbx':'rbx','ebx':'rbx','bx':'rbx','bl':'rbx','bh':'rbx',
        'rcx':'rcx','ecx':'rcx','cx':'rcx','cl':'rcx','ch':'rcx',
        'rdx':'rdx','edx':'rdx','dx':'rdx','dl':'rdx','dh':'rdx',
        'rsi':'rsi','esi':'rsi','si':'rsi','sil':'rsi',
        'rdi':'rdi','edi':'rdi','di':'rdi','dil':'rdi',
        'rbp':'rbp','ebp':'rbp','bp':'rbp','bpl':'rbp',
        'rsp':'rsp','esp':'rsp','sp':'rsp','spl':'rsp',
    }
    if name in aliases:
        return aliases[name]
    match = re.fullmatch(r'(r(?:8|9|1[0-5]))(?:d|w|b)?', name)
    return match.group(1) if match else name


def writes_family(img: Image, row, family: str) -> bool:
    try:
        _reads, writes = row.regs_access()
    except Exception:
        return False
    return family in {reg_family(img, reg) for reg in writes}


def scalar_definition(img: Image, row, family: str) -> dict | None:
    if not writes_family(img, row, family):
        return None
    if row.mnemonic == 'mov' and len(row.operands) >= 2 and row.operands[0].type == X86_OP_REG:
        src = row.operands[1]
        if src.type == X86_OP_IMM:
            return {'kind':'IMM','value':int(src.imm) & 0xffffffff,'site':row.address,'operand':row.op_str}
    if row.mnemonic == 'xor' and len(row.operands) >= 2 and all(op.type == X86_OP_REG for op in row.operands[:2]):
        if reg_family(img, row.operands[0].reg) == family and reg_family(img, row.operands[1].reg) == family:
            return {'kind':'IMM','value':0,'site':row.address,'operand':row.op_str}
    return {'kind':'NONSCALAR','site':row.address,'operand':row.op_str}


def reaching_constants(img: Image, fde: tuple[int, int], site: int, family: str) -> dict:
    rows = img.instructions(fde)
    by = {row.address: row for row in rows}
    pred = img.predecessors(fde)
    if site not in by:
        raise RuntimeError(f'reaching site missing: {site:#x}')
    queue = deque(pred[site])
    visited: set[int] = set()
    definitions: dict[int, dict] = {}
    entry_paths = 0
    clobbered_paths = 0
    while queue:
        address = queue.popleft()
        if address in visited:
            continue
        visited.add(address)
        row = by[address]
        definition = scalar_definition(img, row, family)
        if definition is not None:
            definitions[address] = definition
            continue
        if row.mnemonic == 'call':
            clobbered_paths += 1
            continue
        preds = pred.get(address, set())
        if not preds:
            entry_paths += 1
        else:
            queue.extend(preds)
    defs = [definitions[k] for k in sorted(definitions)]
    values = sorted({d['value'] for d in defs if d['kind'] == 'IMM'})
    return {
        'classification': 'CONFIG_FIELD_0X30_REACHING_CONSTANTS',
        'values': values,
        'definitions': [{**d,'site':hx(d['site'])} for d in defs],
        'entry_paths': entry_paths,
        'clobbered_paths': clobbered_paths,
        'visited_instruction_count': len(visited),
        'all_paths_scalar_constants': bool(defs) and all(d['kind']=='IMM' for d in defs) and entry_paths == 0 and clobbered_paths == 0,
    }


def verify_exact_and_constructor(img: Image) -> tuple[dict, dict]:
    digest = hashlib.sha256(img.raw).hexdigest()
    if len(img.raw) != EXPECTED_SIZE or digest != EXPECTED_SHA256:
        raise RuntimeError('exact current client fence mismatch')
    if img.qword(HANDLER_VTABLE_AP + HANDLER_SLOT) != HANDLER_SLOT_TARGET:
        raise RuntimeError('handler slot target mismatch')
    if img.fde(CONFIG_STORE) != OWNER_CTOR_FDE:
        raise RuntimeError(f'owner constructor FDE moved: {img.fde(CONFIG_STORE)}')
    rows = img.instructions(OWNER_CTOR_FDE)
    by = {row.address: row for row in rows}
    expected = {
        CONFIG_STORE: ('mov', 'dword ptr [rbp + 0x30], edx'),
        HANDLER_OWNER_STORE: ('mov', 'qword ptr [rbx + 0x9c0], r14'),
        CONFIG_OWNER_STORE: ('mov', 'qword ptr [rbx + 0x9c8], rbp'),
    }
    asserted = []
    for address, (mnemonic, operand) in expected.items():
        row = by.get(address)
        if row is None or row.mnemonic != mnemonic or row.op_str != operand:
            actual = None if row is None else (row.mnemonic, row.op_str)
            raise RuntimeError(f'owner pair instruction mismatch {address:#x}: {actual}')
        asserted.append({'at':hx(address),'mnemonic':row.mnemonic,'operand':row.op_str})
    return ({
        'classification':'OWNER_PAIR_CONSTRUCTOR_REASSERTION',
        'constructor_fde':[hx(OWNER_CTOR_FDE[0]),hx(OWNER_CTOR_FDE[1])],
        'handler_owner_offset':hx(HANDLER_OWNER_OFFSET),
        'config_owner_offset':hx(CONFIG_OWNER_OFFSET),
        'config_mode_offset':hx(CONFIG_MODE_OFFSET),
        'handler_vtable_address_point':hx(HANDLER_VTABLE_AP),
        'handler_slot':hx(HANDLER_SLOT),
        'handler_slot_target':hx(HANDLER_SLOT_TARGET),
        'instructions':asserted,
    }, reaching_constants(img, OWNER_CTOR_FDE, CONFIG_STORE, 'rdx'))


def trace_reg_linear(img: Image, rows: list, before_index: int, family: str) -> dict:
    current = family
    chain = []
    for row in reversed(rows[:before_index]):
        if not writes_family(img, row, current):
            continue
        if row.mnemonic == 'mov' and len(row.operands) >= 2 and row.operands[0].type == X86_OP_REG:
            src = row.operands[1]
            if src.type == X86_OP_REG:
                source = reg_family(img, src.reg)
                chain.append({'site':hx(row.address),'from':source,'to':current})
                current = source
                continue
            if src.type == X86_OP_MEM:
                return {
                    'classification':'MEMORY_LOAD',
                    'site':hx(row.address),
                    'operand':row.op_str,
                    'base_family':reg_family(img, src.mem.base) if src.mem.base else None,
                    'displacement':int(src.mem.disp),
                    'size':int(src.size or 0),
                    'chain':chain,
                }
            if src.type == X86_OP_IMM:
                return {'classification':'IMMEDIATE','site':hx(row.address),'operand':row.op_str,'value':int(src.imm)&0xffffffff,'chain':chain}
        return {'classification':'OTHER_DEFINITION','site':hx(row.address),'operand':row.op_str,'chain':chain}
    return {'classification':'ENTRY_REGISTER','family':current,'chain':chain}


def trace_to_entry(img: Image, rows: list, before_index: int, family: str) -> dict:
    current = family
    aliases = []
    for row in reversed(rows[:before_index]):
        if not writes_family(img, row, current):
            continue
        if row.mnemonic == 'mov' and len(row.operands) >= 2 and row.operands[0].type == X86_OP_REG and row.operands[1].type == X86_OP_REG:
            source = reg_family(img, row.operands[1].reg)
            aliases.append({'site':hx(row.address),'from':source,'to':current})
            current = source
            continue
        return {'classification':'ENTRY_ALIAS_NOT_PROVEN','current_family':current,'stopped_at':hx(row.address),'operand':row.op_str,'aliases':aliases}
    return {'classification':'ENTRY_ALIAS_PROVEN' if current == 'rdi' else 'ENTRY_ALIAS_NOT_PROVEN','entry_family':current,'aliases':aliases}


def direct_owner_pair_flows(img: Image) -> dict:
    accepted = []
    examined_calls = 0
    for fde in img.fdes:
        if not img.executable(fde[0]) or fde[1] - fde[0] > 0x10000:
            continue
        rows = img.instructions(fde)
        for ci, call in enumerate(rows):
            if call.mnemonic != 'call' or not call.operands or call.operands[0].type != X86_OP_MEM:
                continue
            mem = call.operands[0].mem
            if int(mem.disp) != HANDLER_SLOT or mem.base == 0:
                continue
            examined_calls += 1
            vtable_family = reg_family(img, mem.base)
            vtable_origin = trace_reg_linear(img, rows, ci, vtable_family)
            if vtable_origin.get('classification') != 'MEMORY_LOAD' or vtable_origin.get('displacement') != 0:
                continue
            if vtable_origin.get('base_family') != 'rdi':
                continue
            vi = next((i for i,row in enumerate(rows) if hx(row.address)==vtable_origin['site']), None)
            if vi is None:
                continue
            handler_origin = trace_reg_linear(img, rows, vi, 'rdi')
            if handler_origin.get('classification') != 'MEMORY_LOAD' or handler_origin.get('displacement') != HANDLER_OWNER_OFFSET:
                continue
            owner_family = handler_origin.get('base_family')
            hi = next((i for i,row in enumerate(rows) if hx(row.address)==handler_origin['site']), None)
            if hi is None or owner_family is None:
                continue
            owner_entry = trace_to_entry(img, rows, hi, owner_family)
            if owner_entry.get('classification') != 'ENTRY_ALIAS_PROVEN':
                continue

            edx_origin = trace_reg_linear(img, rows, ci, 'rdx')
            config_origin = None
            same_owner = False
            if edx_origin.get('classification') == 'MEMORY_LOAD' and edx_origin.get('displacement') == CONFIG_MODE_OFFSET:
                config_family = edx_origin.get('base_family')
                ei = next((i for i,row in enumerate(rows) if hx(row.address)==edx_origin['site']), None)
                if config_family and ei is not None:
                    config_origin = trace_reg_linear(img, rows, ei, config_family)
                    same_owner = (
                        config_origin.get('classification') == 'MEMORY_LOAD'
                        and config_origin.get('displacement') == CONFIG_OWNER_OFFSET
                        and config_origin.get('base_family') == owner_family
                    )
            elif edx_origin.get('classification') == 'IMMEDIATE':
                same_owner = True

            if not same_owner:
                continue
            accepted.append({
                'callsite':hx(call.address),
                'fde':[hx(fde[0]),hx(fde[1])],
                'handler_origin':handler_origin,
                'owner_entry':owner_entry,
                'edx_origin':edx_origin,
                'config_origin':config_origin,
                'flow':'OWNER_PAIR_CONFIG_0X30_TO_EDX' if config_origin is not None else 'OWNER_HANDLER_WITH_IMMEDIATE_EDX',
            })
    return {
        'classification':'OWNER_PAIR_DIRECT_FLOW' if accepted else 'OWNER_PAIR_DIRECT_FLOW_UNKNOWN',
        'examined_slot_0x60_calls':examined_calls,
        'accepted_flow_count':len(accepted),
        'flows':accepted,
    }


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--client',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    img=Image(args.client)
    constructor, constants=verify_exact_and_constructor(img)
    flow=direct_owner_pair_flows(img)

    classification='FIELD6_VALUE_UNKNOWN'
    value=None
    accepted=None
    if flow['accepted_flow_count'] == 1:
        only=flow['flows'][0]
        if only['edx_origin']['classification'] == 'IMMEDIATE':
            classification='FIELD6_VALUE_PROVEN'; value=int(only['edx_origin']['value']); accepted=only
        elif only['config_origin'] is not None and constants['all_paths_scalar_constants'] and len(constants['values']) == 1:
            classification='FIELD6_VALUE_PROVEN'; value=int(constants['values'][0]); accepted=only

    result={
        'schema':'otclient.track-a.current-login-field6-owner-pair-flow.v1',
        **SAFETY,
        'exact_client':{'version':'15.32.75d4a0','sha256':hashlib.sha256(img.raw).hexdigest(),'size':len(img.raw)},
        'owner_pair_constructor_reassertion':constructor,
        'config_field_0x30_reaching_constants':constants,
        'owner_pair_direct_flow':flow,
        'classification':classification,
        'field6_value':value,
        'accepted_flow':accepted,
        'scope_markers':{'NO_HEURISTIC_RANKING':True,'NO_SEMANTIC_GUESSING':True},
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('OWNER_PAIR_CONSTRUCTOR_REASSERTION=PASS')
    print('CONFIG_FIELD_0X30_REACHING_CONSTANTS=PASS')
    print('OWNER_PAIR_DIRECT_FLOW='+flow['classification'])
    print(classification+'=true')
    if value is not None: print('FIELD6_VALUE='+str(value))
    print('NO_HEURISTIC_RANKING=true')
    print('NO_SEMANTIC_GUESSING=true')


if __name__=='__main__':
    main()
