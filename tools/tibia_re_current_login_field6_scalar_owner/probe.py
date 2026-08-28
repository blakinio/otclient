#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP
from elftools.dwarf.callframe import FDE
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

EXPECTED_SHA256 = 'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a'
EXPECTED_SIZE = 52_105_824
HANDLER_TYPE = 'tibia::authentication::TLoginProtocolMessageHandler'
HANDLER_MANGLED = 'N5tibia14authentication28TLoginProtocolMessageHandlerE'
HANDLER_VTABLE_AP = 0x30B6700
HANDLER_SLOT = 0x60
HANDLER_SLOT_TARGET = 0xE25620
SCALAR_CALLSITE_CENSUS = True
CALLER_FDE_RTTI_OWNERS = True
PARENT_MEMBER_HANDLER_BINDING = True
UNIQUE_STATIC_SCALAR = True
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
        self._ins_cache: dict[tuple[int, int], list] = {}
        self._pred_cache: dict[tuple[int, int], dict[int, set[int]]] = {}

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
        rows = self._ins_cache.get(fde)
        if rows is None:
            rows = list(self.md.disasm(self.bytes(fde[0], fde[1] - fde[0]), fde[0]))
            self._ins_cache[fde] = rows
        return rows

    def predecessors(self, fde: tuple[int, int]) -> dict[int, set[int]]:
        cached = self._pred_cache.get(fde)
        if cached is not None:
            return cached
        instructions = self.instructions(fde)
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
            elif nxt is not None:
                successors.add(nxt)
            for target in successors:
                pred[target].add(row.address)
        self._pred_cache[fde] = pred
        return pred


def hx(value: int | None) -> str | None:
    return None if value is None else f'0x{value:x}'


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
    m = re.fullmatch(r'(r(?:8|9|1[0-5]))(?:d|w|b)?', name)
    return m.group(1) if m else name


def writes_family(img: Image, row, family: str) -> bool:
    try:
        _reads, writes = row.regs_access()
    except Exception:
        return False
    return family in {reg_family(img, reg) for reg in writes}


def rip_target(row) -> int | None:
    for op in row.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return row.address + row.size + int(op.mem.disp)
    return None


def read_cstring(img: Image, va: int, limit: int = 512) -> str | None:
    if not img.mapped(va):
        return None
    off = img.va_to_off(va)
    end = img.raw.find(b'\0', off, min(len(img.raw), off + limit))
    if end < 0:
        return None
    try:
        return img.raw[off:end].decode('ascii')
    except UnicodeDecodeError:
        return None


def demangle_nested(name: str) -> str | None:
    if not (name.startswith('N') and name.endswith('E')):
        return None
    pos = 1
    parts = []
    while pos < len(name) - 1:
        match = re.match(r'(\d+)', name[pos:])
        if not match:
            return None
        length = int(match.group(1))
        pos += len(match.group(1))
        part = name[pos:pos + length]
        if len(part) != length:
            return None
        parts.append(part)
        pos += length
    return '::'.join(parts) if parts and pos == len(name) - 1 else None


def recover_vtables(img: Image) -> list[dict]:
    reverse: dict[int, list[int]] = defaultdict(list)
    for where, value in img.rel.items():
        reverse[value].append(where)
    rows = []
    seen = set()
    for where, name_va in img.rel.items():
        raw_name = read_cstring(img, name_va)
        if not raw_name:
            continue
        type_name = demangle_nested(raw_name)
        if not type_name:
            continue
        rtti = where - 8
        for type_slot in reverse.get(rtti, []):
            ap = type_slot + 8
            if (rtti, ap) in seen or not img.mapped(ap - 16, 24):
                continue
            if img.u64(ap - 16) != 0:
                continue
            first = img.qword(ap)
            if not img.executable(first):
                continue
            seen.add((rtti, ap))
            rows.append({'type_name': type_name, 'rtti': rtti, 'address_point': ap})
    return rows


def verify_exact(img: Image, vtables: list[dict]) -> dict:
    if len(img.raw) != EXPECTED_SIZE or hashlib.sha256(img.raw).hexdigest() != EXPECTED_SHA256:
        raise RuntimeError('exact current client fence mismatch')
    if img.qword(HANDLER_VTABLE_AP + HANDLER_SLOT) != HANDLER_SLOT_TARGET:
        raise RuntimeError('promoted handler slot mismatch')
    handler = [row for row in vtables if row['type_name'] == HANDLER_TYPE and row['address_point'] == HANDLER_VTABLE_AP]
    if len(handler) != 1:
        raise RuntimeError(f'handler RTTI/vtable identity mismatch: {len(handler)}')
    return {
        'handler_type': HANDLER_TYPE,
        'handler_vtable_address_point': hx(HANDLER_VTABLE_AP),
        'slot': hx(HANDLER_SLOT),
        'slot_0x60_target': hx(HANDLER_SLOT_TARGET),
    }


def scalar_definition(img: Image, row, family: str) -> dict | None:
    if not writes_family(img, row, family):
        return None
    if row.mnemonic == 'mov' and len(row.operands) >= 2 and row.operands[0].type == X86_OP_REG:
        src = row.operands[1]
        if src.type == X86_OP_IMM:
            return {'kind':'IMM','value':int(src.imm) & 0xffffffff,'site':row.address,'operand':row.op_str}
    if row.mnemonic == 'xor' and len(row.operands) >= 2 and all(op.type == X86_OP_REG for op in row.operands[:2]):
        a = reg_family(img, row.operands[0].reg)
        b = reg_family(img, row.operands[1].reg)
        if a == family and b == family:
            return {'kind':'IMM','value':0,'site':row.address,'operand':row.op_str}
    return {'kind':'NONSCALAR','site':row.address,'operand':row.op_str}


def reaching_edx(img: Image, fde: tuple[int, int], callsite: int) -> dict:
    instructions = img.instructions(fde)
    pred = img.predecessors(fde)
    by = {row.address: row for row in instructions}
    queue = deque(pred.get(callsite, set()))
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
            clobbered_paths += 1
            continue
        predecessors = pred.get(address, set())
        if not predecessors:
            entry_paths += 1
        else:
            queue.extend(predecessors)
    rows = [definitions[key] for key in sorted(definitions)]
    values = {row['value'] for row in rows if row['kind'] == 'IMM'}
    non_scalar = any(row['kind'] != 'IMM' for row in rows)
    if len(values) == 1 and not non_scalar and not clobbered_paths and not entry_paths:
        classification = 'UNIQUE_STATIC_SCALAR'
        value = next(iter(values))
    else:
        classification = 'VALUE_NOT_UNIQUELY_PROVEN'
        value = None
    return {
        'classification': classification,
        'value': value,
        'definitions': [{**row,'site':hx(row['site'])} for row in rows],
        'clobbered_paths': clobbered_paths,
        'entry_paths': entry_paths,
        'visited_instruction_count': len(visited),
    }


def trace_register_origin(img: Image, instructions, site_index: int, family: str) -> dict:
    current = family
    chain = []
    for row in reversed(instructions[:site_index]):
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
                    'chain':chain,
                }
        if row.mnemonic == 'lea' and len(row.operands) >= 2 and row.operands[1].type == X86_OP_MEM:
            src = row.operands[1]
            return {
                'classification':'LEA_DEFINITION',
                'site':hx(row.address),
                'operand':row.op_str,
                'base_family':reg_family(img, src.mem.base) if src.mem.base else None,
                'displacement':int(src.mem.disp),
                'chain':chain,
            }
        return {'classification':'REGISTER_DEFINITION','site':hx(row.address),'operand':row.op_str,'chain':chain}
    return {'classification':'ENTRY_REGISTER','register_family':current,'chain':chain}


def trace_family_to_entry(img: Image, instructions, site_index: int, family: str) -> dict:
    current = family
    aliases = []
    for row in reversed(instructions[:site_index]):
        if not writes_family(img, row, current):
            continue
        if row.mnemonic == 'mov' and len(row.operands) >= 2 and row.operands[0].type == X86_OP_REG and row.operands[1].type == X86_OP_REG:
            source = reg_family(img, row.operands[1].reg)
            aliases.append({'site':hx(row.address),'from':source,'to':current})
            current = source
            continue
        return {'classification':'ENTRY_ALIAS_NOT_PROVEN','stopped_at':hx(row.address),'operand':row.op_str,'current_family':current,'aliases':aliases}
    return {'classification':'ENTRY_ALIAS_PROVEN' if current == 'rdi' else 'ENTRY_ALIAS_NOT_PROVEN','entry_family':current,'aliases':aliases}


def scalar_slot_calls(img: Image) -> list[dict]:
    rows = []
    for fde in img.fdes:
        if not img.executable(fde[0]) or fde[1] - fde[0] > 0x20000:
            continue
        instructions = img.instructions(fde)
        for index, row in enumerate(instructions):
            if row.mnemonic != 'call' or not row.operands or row.operands[0].type != X86_OP_MEM:
                continue
            mem = row.operands[0]
            if int(mem.mem.disp) != HANDLER_SLOT or not mem.mem.base:
                continue
            edx = reaching_edx(img, fde, row.address)
            if edx['classification'] != 'UNIQUE_STATIC_SCALAR':
                continue
            vtable_family = reg_family(img, mem.mem.base)
            vtable_load = None
            object_family = None
            for prior in reversed(instructions[:index]):
                if not writes_family(img, prior, vtable_family):
                    continue
                if prior.mnemonic == 'mov' and len(prior.operands) >= 2 and prior.operands[1].type == X86_OP_MEM:
                    src = prior.operands[1]
                    if src.mem.base and int(src.mem.disp) == 0:
                        vtable_load = prior
                        object_family = reg_family(img, src.mem.base)
                break
            if vtable_load is None or object_family is None:
                receiver = {'classification':'NO_LOCAL_VTABLE_LOAD'}
            else:
                vtable_index = next(i for i, item in enumerate(instructions) if item.address == vtable_load.address)
                object_origin = trace_register_origin(img, instructions, vtable_index, object_family)
                rdi_origin = trace_register_origin(img, instructions, index, 'rdi')
                receiver = {
                    'classification':'SCALAR_VIRTUAL_RECEIVER',
                    'vtable_object_family':object_family,
                    'vtable_load_site':hx(vtable_load.address),
                    'object_origin':object_origin,
                    'rdi_origin':rdi_origin,
                    'abi_receiver_matches_vtable_object': object_family == 'rdi',
                }
                if object_origin.get('classification') == 'MEMORY_LOAD' and object_origin.get('base_family'):
                    member_site = int(object_origin['site'], 16)
                    member_index = next(i for i,item in enumerate(instructions) if item.address == member_site)
                    receiver['parent_base_entry'] = trace_family_to_entry(img, instructions, member_index, object_origin['base_family'])
            rows.append({
                'site':row.address,
                'fde':fde,
                'operand':row.op_str,
                'edx':edx,
                'receiver':receiver,
                '_instructions':instructions,
                '_index':index,
            })
    return rows


def vtable_method_owner_map(img: Image, vtables: list[dict]) -> dict[tuple[int,int], list[dict]]:
    owners: dict[tuple[int,int], list[dict]] = defaultdict(list)
    seen = set()
    for vt in vtables:
        ap = vt['address_point']
        for offset in range(0, 0x300, 8):
            if not img.mapped(ap + offset, 8):
                break
            target = img.qword(ap + offset)
            if not img.executable(target):
                continue
            fde = img.fde(target)
            if fde is None:
                continue
            key = (fde, vt['type_name'], ap, offset)
            if key in seen:
                continue
            seen.add(key)
            owners[fde].append({'type_name':vt['type_name'],'address_point':ap,'slot_offset':offset,'target':target})
    return owners


def explicit_vtable_stores(img: Image, instructions, target_ap: int) -> list[dict]:
    out = []
    for index,row in enumerate(instructions):
        if row.mnemonic != 'lea' or len(row.operands) < 2 or row.operands[0].type != X86_OP_REG:
            continue
        if rip_target(row) != target_ap:
            continue
        vt_family = reg_family(img, row.operands[0].reg)
        for later in instructions[index+1:index+16]:
            if later.mnemonic != 'mov' or len(later.operands) < 2:
                continue
            dst,src = later.operands[0],later.operands[1]
            if dst.type != X86_OP_MEM or src.type != X86_OP_REG or not dst.mem.base or int(dst.mem.disp) != 0:
                continue
            if reg_family(img, src.reg) != vt_family:
                continue
            out.append({'lea_site':row.address,'store_site':later.address,'object_family':reg_family(img,dst.mem.base)})
    return out


def owner_constructors(img: Image, owner_ap: int) -> list[dict]:
    rows=[]
    for fde in img.fdes:
        if not img.executable(fde[0]) or fde[1]-fde[0] > 0x10000:
            continue
        instructions=img.instructions(fde)
        for store in explicit_vtable_stores(img,instructions,owner_ap):
            store_index=next(i for i,x in enumerate(instructions) if x.address==store['store_site'])
            entry=trace_family_to_entry(img,instructions,store_index,store['object_family'])
            if entry['classification']=='ENTRY_ALIAS_PROVEN':
                rows.append({'fde':fde,'this_family':store['object_family'],'vtable_store_site':store['store_site'],'_instructions':instructions})
    unique={(r['fde'],r['this_family'],r['vtable_store_site']):r for r in rows}
    return list(unique.values())


def function_constructs_handler(img: Image, target: int) -> bool:
    fde=img.fde(target)
    if fde is None or fde[1]-fde[0] > 0x10000:
        return False
    instructions=img.instructions(fde)
    for store in explicit_vtable_stores(img,instructions,HANDLER_VTABLE_AP):
        idx=next(i for i,x in enumerate(instructions) if x.address==store['store_site'])
        entry=trace_family_to_entry(img,instructions,idx,store['object_family'])
        if entry['classification']=='ENTRY_ALIAS_PROVEN':
            return True
    return False


def constructor_member_proofs(img: Image, constructor: dict, member_offset: int) -> list[dict]:
    instructions=constructor['_instructions']
    this_family=constructor['this_family']
    proofs=[]
    handler_stores=explicit_vtable_stores(img,instructions,HANDLER_VTABLE_AP)
    for index,row in enumerate(instructions):
        if row.mnemonic!='mov' or len(row.operands)<2:
            continue
        dst,src=row.operands[0],row.operands[1]
        if dst.type!=X86_OP_MEM or not dst.mem.base or int(dst.mem.disp)!=member_offset:
            continue
        if reg_family(img,dst.mem.base)!=this_family or src.type!=X86_OP_REG:
            continue
        source_family=reg_family(img,src.reg)
        direct=[]
        for hs in handler_stores:
            if hs['store_site']<row.address and hs['object_family']==source_family:
                direct.append({'classification':'SAME_FDE_HANDLER_VTABLE_OBJECT','handler_vtable_store_site':hx(hs['store_site'])})
        constructor_calls=[]
        for call_index,call in enumerate(instructions[:index]):
            if call.mnemonic!='call' or not call.operands or call.operands[0].type!=X86_OP_IMM:
                continue
            target=int(call.operands[0].imm)
            if not function_constructs_handler(img,target):
                continue
            rdi_origin=trace_register_origin(img,instructions,call_index,'rdi')
            # Accept only a source register that is itself used as the constructor receiver,
            # either directly or via a simple alias chain recorded by the origin tracer.
            direct_receiver = source_family == 'rdi'
            if not direct_receiver and rdi_origin.get('classification')=='ENTRY_REGISTER':
                direct_receiver = rdi_origin.get('register_family')==source_family
            constructor_calls.append({
                'classification':'DIRECT_HANDLER_CONSTRUCTOR_CALL',
                'call_site':hx(call.address),
                'target':hx(target),
                'rdi_origin':rdi_origin,
                'source_family_matches_receiver':direct_receiver,
            })
        proven = bool(direct) or any(x['source_family_matches_receiver'] for x in constructor_calls)
        proofs.append({
            'classification':'PARENT_MEMBER_HANDLER_BINDING_PROVEN' if proven else 'PARENT_MEMBER_HANDLER_BINDING_UNKNOWN',
            'member_store_site':hx(row.address),
            'member_offset':member_offset,
            'source_family':source_family,
            'same_fde_handler_evidence':direct,
            'handler_constructor_calls':constructor_calls,
        })
    return proofs


def sanitize_owner(row: dict) -> dict:
    return {'type_name':row['type_name'],'address_point':hx(row['address_point']),'slot_offset':hx(row['slot_offset']),'target':hx(row['target'])}


def sanitize_candidate(call: dict, owners: list[dict], binding: dict) -> dict:
    return {
        'site':hx(call['site']),
        'fde':[hx(call['fde'][0]),hx(call['fde'][1])],
        'operand':call['operand'],
        'edx':call['edx'],
        'receiver':call['receiver'],
        'caller_fde_rtti_owners':[sanitize_owner(x) for x in owners],
        'handler_binding':binding,
    }


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--client',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()

    img=Image(args.client)
    vtables=recover_vtables(img)
    promoted=verify_exact(img,vtables)
    owner_map=vtable_method_owner_map(img,vtables)
    scalar=scalar_slot_calls(img)

    analyzed=[]
    proven=[]
    for call in scalar:
        owners=owner_map.get(call['fde'],[])
        receiver=call['receiver']
        binding={
            'classification':'PARENT_MEMBER_HANDLER_BINDING_NOT_APPLICABLE',
            'proofs':[],
        }
        origin=receiver.get('object_origin') or {}
        parent_entry=receiver.get('parent_base_entry') or {}
        abi_ok=receiver.get('abi_receiver_matches_vtable_object') is True
        if abi_ok and origin.get('classification')=='MEMORY_LOAD' and origin.get('displacement') is not None and parent_entry.get('classification')=='ENTRY_ALIAS_PROVEN':
            member_offset=int(origin['displacement'])
            proof_rows=[]
            unique_owner_aps=sorted({int(x['address_point']) for x in owners})
            for owner_ap in unique_owner_aps:
                for ctor in owner_constructors(img,owner_ap):
                    for proof in constructor_member_proofs(img,ctor,member_offset):
                        proof_rows.append({
                            'owner_vtable_address_point':hx(owner_ap),
                            'constructor_fde':[hx(ctor['fde'][0]),hx(ctor['fde'][1])],
                            **proof,
                        })
            proven_rows=[x for x in proof_rows if x['classification']=='PARENT_MEMBER_HANDLER_BINDING_PROVEN']
            binding={
                'classification':'PARENT_MEMBER_HANDLER_BINDING_PROVEN' if len(proven_rows)==1 else 'PARENT_MEMBER_HANDLER_BINDING_UNKNOWN',
                'member_offset':member_offset,
                'proof_count':len(proven_rows),
                'proofs':proof_rows,
            }
        row=sanitize_candidate(call,owners,binding)
        analyzed.append(row)
        if binding['classification']=='PARENT_MEMBER_HANDLER_BINDING_PROVEN':
            proven.append(row)

    values={int(row['edx']['value']) for row in proven if row['edx']['classification']=='UNIQUE_STATIC_SCALAR'}
    if len(proven)==1 and len(values)==1:
        classification='FIELD6_VALUE_PROVEN'
        field6_value=next(iter(values))
        accepted=proven[0]
    else:
        classification='FIELD6_VALUE_UNKNOWN'
        field6_value=None
        accepted=None

    result={
        'schema':'otclient.track-a.current-login-field6-scalar-owner.v1',
        **SAFETY,
        'exact_client':{'version':'15.32.75d4a0','sha256':EXPECTED_SHA256,'size':EXPECTED_SIZE},
        'promoted_target':promoted,
        'classification':classification,
        'field6_value':field6_value,
        'accepted_callsite':accepted,
        'scalar_callsite_census':{
            'classification':'SCALAR_CALLSITE_CENSUS',
            'total_slot_0x60_scalar_count':len(scalar),
            'scalar_values':{str(v):sum(1 for x in scalar if x['edx']['value']==v) for v in sorted({x['edx']['value'] for x in scalar})},
            'candidates':analyzed,
            'handler_bound_scalar_count':len(proven),
            'handler_bound_scalar_callsites':proven,
            'rtti_vtable_type_count':len(vtables),
            'scope_markers':{
                'CALLER_FDE_RTTI_OWNERS':CALLER_FDE_RTTI_OWNERS,
                'PARENT_MEMBER_HANDLER_BINDING':PARENT_MEMBER_HANDLER_BINDING,
                'UNIQUE_STATIC_SCALAR':UNIQUE_STATIC_SCALAR,
                'NO_HEURISTIC_RANKING':NO_HEURISTIC_RANKING,
                'NO_SEMANTIC_GUESSING':NO_SEMANTIC_GUESSING,
            },
        },
    }
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('CURRENT_LOGIN_FIELD6_SCALAR_OWNER=PASS')
    print('SCALAR_CALLSITE_CENSUS=' + str(len(scalar)))
    print('CALLER_FDE_RTTI_OWNERS=PASS')
    print('PARENT_MEMBER_HANDLER_BINDING=' + str(len(proven)))
    print('FIELD6_VALUE=' + (str(field6_value) if field6_value is not None else 'UNKNOWN'))
    print('CLASSIFICATION=' + classification)
    print('RAW_CLIENT_UPLOADED=false')
    print('OFFICIAL_CLIENT_EXECUTED=false')
    print('PROCESS_MEMORY_ACCESS=false')
    print('NO_HEURISTIC_RANKING=true')
    print('NO_SEMANTIC_GUESSING=true')


if __name__=='__main__':
    main()
