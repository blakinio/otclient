#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from elftools.dwarf.callframe import FDE


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
                Section(s.name, int(s['sh_offset']), int(s['sh_size']), int(s['sh_addr']), int(s['sh_flags']))
                for s in elf.iter_sections()
                if int(s['sh_size']) > 0
            ]
            self.relocations: dict[int, int] = {}
            for sec in elf.iter_sections():
                if not isinstance(sec, RelocationSection):
                    continue
                for rel in sec.iter_relocations():
                    if not rel.is_RELA():
                        continue
                    self.relocations[int(rel['r_offset'])] = int(rel['r_addend'])
            dwarf = elf.get_dwarf_info()
            self.fdes = sorted(
                (int(entry['initial_location']), int(entry['initial_location']) + int(entry['address_range']))
                for entry in dwarf.EH_CFI_entries()
                if isinstance(entry, FDE)
            )
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True

    def off_to_va(self, off: int) -> int | None:
        for s in self.sections:
            if s.offset <= off < s.offset + s.size:
                return s.va + (off - s.offset)
        return None

    def va_to_off(self, va: int) -> int:
        for s in self.sections:
            if s.va <= va < s.va + s.size:
                return s.offset + (va - s.va)
        raise ValueError(f'unmapped VA 0x{va:x}')

    def mapped(self, va: int, size: int = 1) -> bool:
        try:
            off = self.va_to_off(va)
        except ValueError:
            return False
        return 0 <= off <= len(self.raw) - size

    def executable(self, va: int) -> bool:
        return any((s.flags & 4) and s.va <= va < s.va + s.size for s in self.sections)

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        matches = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        if len(matches) != 1:
            return None
        return matches[0]

    def u32(self, va: int) -> int:
        return struct.unpack_from('<I', self.raw, self.va_to_off(va))[0]

    def i32(self, va: int) -> int:
        return struct.unpack_from('<i', self.raw, self.va_to_off(va))[0]

    def bytes(self, va: int, size: int) -> bytes:
        off = self.va_to_off(va)
        return self.raw[off:off + size]

    def u64(self, va: int) -> int:
        return struct.unpack_from('<Q', self.raw, self.va_to_off(va))[0]

    def qword(self, va: int) -> int:
        if va in self.relocations:
            return int(self.relocations[va]) & 0xffffffffffffffff
        return self.u64(va)

    def string_occurrences(self, value: str) -> list[int]:
        needle = value.encode('utf-8')
        out: list[int] = []
        start = 0
        while True:
            off = self.raw.find(needle, start)
            if off < 0:
                return out
            va = self.off_to_va(off)
            if va is not None:
                out.append(va)
            start = off + 1

    def disasm(self, va: int, size: int = 0x300, limit: int = 160):
        return list(self.md.disasm(self.bytes(va, size), va))[:limit]


def qstring(img: Image, sbase: int, index: int) -> str:
    ent = sbase + index * 8
    rel = img.u32(ent)
    length = img.u32(ent + 4)
    if length > 4096:
        raise ValueError('Qt string too long')
    data = img.bytes(sbase + rel, length)
    return data.decode('utf-8', 'strict')


def find_stringdata(img: Image, class_name: str) -> list[int]:
    out: set[int] = set()
    for sva in img.string_occurrences(class_name):
        lower = max(0, sva - 0x10000)
        for base in range(sva & ~3, lower - 1, -4):
            if not img.mapped(base, 8):
                continue
            try:
                if img.u32(base) != sva - base or img.u32(base + 4) != len(class_name.encode()):
                    continue
                if qstring(img, base, 0) == class_name:
                    out.add(base)
            except (ValueError, UnicodeDecodeError, struct.error):
                continue
    return sorted(out)


def parse_meta(img: Image, sbase: int, mbase: int) -> dict | None:
    if not img.mapped(mbase, 56):
        return None
    try:
        h = [img.u32(mbase + i * 4) for i in range(14)]
    except (ValueError, struct.error):
        return None
    rev, class_index, ci_count, ci_off, method_count, method_off, prop_count, prop_off, enum_count, enum_off, ctor_count, ctor_off, flags, signal_count = h
    if not (7 <= rev <= 20 and class_index == 0 and 0 < method_count <= 1000 and 14 <= method_off < 200000 and signal_count <= method_count):
        return None
    if any(x > 10000 for x in (ci_count, prop_count, enum_count, ctor_count)):
        return None
    rows = []
    try:
        if qstring(img, sbase, class_index) == '':
            return None
        for i in range(method_count):
            base = mbase + (method_off + i * 6) * 4
            row = [img.u32(base + j * 4) for j in range(6)]
            name = qstring(img, sbase, row[0])
            if not name or len(name) > 256:
                return None
            rows.append({'index': i, 'name': name, 'argc': row[1], 'param_offset': row[2], 'tag': row[3], 'flags': row[4], 'meta_type_offset': row[5]})
    except (ValueError, UnicodeDecodeError, struct.error):
        return None
    return {
        'revision': rev,
        'class_index': class_index,
        'method_count': method_count,
        'method_offset': method_off,
        'signal_count': signal_count,
        'rows': rows,
    }


def find_metadata(img: Image, sbase: int, required_names: Iterable[str]) -> list[tuple[int, dict]]:
    required = set(required_names)
    results = []
    lo = max(0, sbase - 0x20000)
    hi = sbase + 0x20000
    for mbase in range(lo & ~3, hi, 4):
        meta = parse_meta(img, sbase, mbase)
        if not meta:
            continue
        names = {r['name'] for r in meta['rows']}
        if required.issubset(names):
            results.append((mbase, meta))
    return results


def find_qmeta_static_metacall(img: Image, sbase: int, mbase: int) -> list[dict]:
    out = []
    rel = img.relocations
    for where, addend in rel.items():
        if addend != sbase:
            continue
        if rel.get(where + 8) != mbase:
            continue
        st = rel.get(where + 16)
        if st is None or not img.executable(st):
            continue
        out.append({'qmetaobject': where - 8, 'static_metacall': st})
    return out


def recover_jump_table(img: Image, st: int, method_count: int) -> dict:
    ins = img.disasm(st, 0x700, 260)
    candidates = []
    for pos, x in enumerate(ins):
        if x.mnemonic != 'lea' or len(x.operands) < 2:
            continue
        op = x.operands[1]
        if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
            continue
        reg = x.operands[0].reg
        table = x.address + x.size + op.mem.disp
        used = any(
            any(yop.type == X86_OP_MEM and yop.mem.base == reg and yop.mem.scale == 4 for yop in y.operands)
            for y in ins[pos + 1:pos + 12]
        )
        if not used:
            continue
        try:
            targets = [table + img.i32(table + i * 4) for i in range(method_count)]
        except (ValueError, struct.error):
            continue
        score = sum(img.executable(t) for t in targets)
        candidates.append((score, table, targets))
    candidates.sort(reverse=True)
    if not candidates or candidates[0][0] != method_count:
        raise RuntimeError('complete Qt jump table not found')
    score, table, targets = candidates[0]
    return {'table': table, 'targets': targets, 'score': score}


def immediate_edges(img: Image, start: int, size: int = 0x280) -> list[dict]:
    out = []
    for ins in img.disasm(start, size, 120):
        if ins.mnemonic.startswith('ret'):
            break
        if ins.mnemonic not in {'call', 'jmp'} or not ins.operands:
            continue
        op = ins.operands[0]
        if op.type == X86_OP_IMM:
            target = int(op.imm)
            if img.executable(target):
                out.append({'at': ins.address, 'kind': ins.mnemonic, 'target': target})
        if ins.mnemonic == 'jmp':
            break
    return out


def function_control_transfers(img: Image, start: int, limit: int = 1200) -> dict:
    bounds = img.containing_fde(start)
    if bounds is None:
        raise RuntimeError(f'no unique FDE for 0x{start:x}')
    lo, hi = bounds
    rows = []
    for ins in list(img.md.disasm(img.bytes(lo, hi - lo), lo))[:limit]:
        if ins.mnemonic not in {'call', 'jmp'} or not ins.operands:
            continue
        op = ins.operands[0]
        row = {'at': ins.address, 'kind': ins.mnemonic, 'operand': ins.op_str}
        if op.type == X86_OP_IMM:
            row['mode'] = 'direct'
            row['target'] = int(op.imm)
        elif op.type == X86_OP_MEM:
            row['mode'] = 'indirect_mem'
            row['base'] = img.md.reg_name(op.mem.base) if op.mem.base else ''
            row['index'] = img.md.reg_name(op.mem.index) if op.mem.index else ''
            row['scale'] = int(op.mem.scale)
            row['disp'] = int(op.mem.disp)
        else:
            row['mode'] = 'indirect_reg'
            row['reg'] = img.md.reg_name(op.reg)
        rows.append(row)
    return {'fde': (lo, hi), 'transfers': rows}

def instruction_context(img: Image, center: int, before: int = 8, after: int = 5) -> list[dict]:
    bounds = img.containing_fde(center)
    if bounds is None:
        return []
    lo, hi = bounds
    ins = list(img.md.disasm(img.bytes(lo, hi - lo), lo))
    indexes = [i for i, row in enumerate(ins) if row.address == center]
    if len(indexes) != 1:
        return []
    i = indexes[0]
    return [
        {'at': hx(row.address), 'mnemonic': row.mnemonic, 'operand': row.op_str}
        for row in ins[max(0, i - before):min(len(ins), i + after + 1)]
    ]



def fde_instructions(img: Image, start: int, limit: int = 900) -> dict:
    bounds = img.containing_fde(start)
    if bounds is None:
        raise RuntimeError(f'no unique FDE for 0x{start:x}')
    lo, hi = bounds
    rows = [
        {'at': hx(ins.address), 'mnemonic': ins.mnemonic, 'operand': ins.op_str}
        for ins in list(img.md.disasm(img.bytes(lo, hi - lo), lo))[:limit]
    ]
    return {'fde': [hx(lo), hx(hi)], 'instructions': rows}


def named_vslot_target(vtables: dict, name: str, offset: str) -> int:
    rows = vtables.get(name, [])
    if len(rows) != 1 or len(rows[0].get('address_points', [])) != 1:
        raise RuntimeError(f'{name}: expected one RTTI/vtable candidate')
    slots = {row['offset']: row for row in rows[0]['address_points'][0]['slots']}
    row = slots.get(offset)
    if not row or not row.get('executable'):
        raise RuntimeError(f'{name}: executable slot {offset} not found')
    return int(row['target'], 16)

def rtti_vtable_candidates(img: Image, simple_name: str) -> list[dict]:
    found = {}
    for occurrence in img.string_occurrences(simple_name):
        off = img.va_to_off(occurrence)
        start = img.raw.rfind(b'\0', max(0, off - 192), off) + 1
        end = img.raw.find(b'\0', off, min(len(img.raw), off + 512))
        if end < 0:
            continue
        try:
            text = img.raw[start:end].decode('ascii')
        except UnicodeDecodeError:
            continue
        if simple_name not in text or '::' in text or not text.startswith('N'):
            continue
        name_va = img.off_to_va(start)
        if name_va is None:
            continue
        for name_ref, addend in img.relocations.items():
            if addend != name_va:
                continue
            rtti = name_ref - 8
            aps = []
            for type_slot, type_addend in img.relocations.items():
                if type_addend != rtti:
                    continue
                ap = type_slot + 8
                if not img.mapped(ap - 16, 24) or img.u64(ap - 16) != 0:
                    continue
                slots = []
                for slot_off in range(0, 0xc0, 8):
                    if not img.mapped(ap + slot_off, 8):
                        break
                    target = img.qword(ap + slot_off)
                    slots.append({
                        'offset': hex(slot_off),
                        'target': hx(target),
                        'executable': img.executable(target),
                    })
                aps.append({'address_point': hx(ap), 'slots': slots})
            if aps:
                found[(text, rtti)] = {
                    'rtti_name': text,
                    'rtti': hx(rtti),
                    'name_va': hx(name_va),
                    'address_points': aps,
                }
    return sorted(found.values(), key=lambda row: (row['rtti_name'], row['rtti']))


def locate_class(img: Image, class_name: str, required_methods: list[str]) -> dict:
    s_candidates = find_stringdata(img, class_name)
    matches = []
    for sbase in s_candidates:
        for mbase, meta in find_metadata(img, sbase, required_methods):
            qmos = find_qmeta_static_metacall(img, sbase, mbase)
            for qmo in qmos:
                try:
                    jt = recover_jump_table(img, qmo['static_metacall'], meta['method_count'])
                except RuntimeError:
                    continue
                rows = []
                for row in meta['rows']:
                    rows.append({**row, 'target': jt['targets'][row['index']]})
                matches.append({
                    'class': class_name,
                    'stringdata': sbase,
                    'metadata': mbase,
                    'qmetaobject': qmo['qmetaobject'],
                    'static_metacall': qmo['static_metacall'],
                    'jump_table': jt['table'],
                    'method_count': meta['method_count'],
                    'signal_count': meta['signal_count'],
                    'methods': rows,
                })
    if len(matches) != 1:
        raise RuntimeError(f'{class_name}: expected one complete Qt meta match, got {len(matches)}')
    return matches[0]


def dynamic_symbols(path: Path, patterns: tuple[str, ...]) -> list[str]:
    out = []
    with path.open('rb') as fh:
        elf = ELFFile(fh)
        dyn = elf.get_section_by_name('.dynsym')
        if dyn is None:
            return out
        for sym in dyn.iter_symbols():
            name = sym.name
            low = name.lower()
            if any(p.lower() in low for p in patterns):
                out.append(name)
    return sorted(set(out))


def reference_scan(img: Image, rip_targets: set[int], direct_targets: set[int]) -> dict:
    rip = {target: [] for target in rip_targets}
    direct = {target: [] for target in direct_targets}
    for sec in img.sections:
        if not (sec.flags & 4) or not sec.size:
            continue
        blob = img.raw[sec.offset:sec.offset + sec.size]
        for ins in img.md.disasm(blob, sec.va):
            if ins.mnemonic == 'call' and ins.operands and ins.operands[0].type == X86_OP_IMM:
                target = int(ins.operands[0].imm)
                if target in direct:
                    direct[target].append(ins.address)
            for op in ins.operands:
                if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
                    continue
                target = ins.address + ins.size + int(op.mem.disp)
                if target in rip:
                    rip[target].append(ins.address)
    return {'rip': rip, 'direct': direct}


def rip_refs(img: Image, target: int) -> list[int]:
    return reference_scan(img, {target}, set())['rip'][target]


def direct_calls(img: Image, target: int) -> list[int]:
    return reference_scan(img, set(), {target})['direct'][target]


def plt_symbol_addresses(path: Path, needles: tuple[str, ...]) -> dict[str, list[int]]:
    out = {}
    with path.open('rb') as fh:
        elf = ELFFile(fh)
        plt = elf.get_section_by_name('.plt')
        plt_sec = elf.get_section_by_name('.plt.sec')
        for relsec in elf.iter_sections():
            if not isinstance(relsec, RelocationSection) or '.plt' not in relsec.name:
                continue
            symtab = elf.get_section(relsec['sh_link'])
            for index, rel in enumerate(relsec.iter_relocations()):
                name = symtab.get_symbol(rel['r_info_sym']).name if rel['r_info_sym'] else ''
                if not name or not any(token in name for token in needles):
                    continue
                addresses = out.setdefault(name, [])
                if plt_sec is not None:
                    entsize = int(plt_sec['sh_entsize']) or 16
                    addresses.append(int(plt_sec['sh_addr']) + index * entsize)
                if plt is not None:
                    entsize = int(plt['sh_entsize']) or 16
                    addresses.append(int(plt['sh_addr']) + (index + 1) * entsize)
    return {name: sorted(set(values)) for name, values in sorted(out.items())}


def hx(v: int) -> str:
    return f'0x{v:x}'


def sanitize_transfer(row: dict) -> dict:
    out = dict(row)
    out['at'] = hx(int(out['at']))
    if 'target' in out:
        out['target'] = hx(int(out['target']))
    if 'disp' in out:
        out['disp_hex'] = hex(int(out['disp']))
    return out


def sanitize_class(c: dict, method_filter: re.Pattern[str] | None = None) -> dict:
    methods = c['methods']
    if method_filter:
        methods = [m for m in methods if method_filter.search(m['name'])]
    return {
        'class': c['class'],
        'stringdata': hx(c['stringdata']),
        'metadata': hx(c['metadata']),
        'qmetaobject': hx(c['qmetaobject']),
        'static_metacall': hx(c['static_metacall']),
        'jump_table': hx(c['jump_table']),
        'method_count': c['method_count'],
        'signal_count': c['signal_count'],
        'methods': [
            {
                'index': m['index'],
                'name': m['name'],
                'argc': m['argc'],
                'target': hx(m['target']),
                'edges': [{**e, 'at': hx(e['at']), 'target': hx(e['target'])} for e in immediate_edges(GLOBAL_IMAGE, m['target'])],
            }
            for m in methods
        ],
    }



PUBLIC_PACKAGE_MANIFEST = 'tibiaclient-linux-current/package.json'
MESSAGE_CLASSES = (
    'GameclientMessageLogin',
    'LoginRSAEncryptedBlock',
    'GameclientMessageSecondaryLogin',
    'SecondaryLoginRSAEncryptedBlock',
    'GameclientMessageEnterWorld',
)


def expected_mangled_full(full: str) -> str:
    return 'N' + ''.join(str(len(part)) + part for part in full.split('::')) + 'E'


def expected_mangled_rtti(simple_name: str) -> str:
    full = 'tibia::protobuf::protocol::' + simple_name
    return expected_mangled_full(full)


def recover_exact_named_vtable(img: Image, simple_name: str, full_name: str) -> dict:
    expected = expected_mangled_full(full_name)
    rows = [row for row in rtti_vtable_candidates(img, simple_name) if row['rtti_name'] == expected]
    if len(rows) != 1:
        raise RuntimeError(f'{full_name}: expected one exact RTTI row, got {len(rows)}')
    aps = rows[0].get('address_points', [])
    if len(aps) != 1:
        raise RuntimeError(f'{full_name}: expected one vtable AP, got {len(aps)}')
    return {'rtti_name': rows[0]['rtti_name'], 'rtti': rows[0]['rtti'], **aps[0]}


def recover_vtable(img: Image, simple_name: str) -> dict:
    expected = expected_mangled_rtti(simple_name)
    rows = [row for row in rtti_vtable_candidates(img, simple_name) if row['rtti_name'] == expected]
    if len(rows) != 1:
        raise RuntimeError(f'{simple_name}: expected one exact RTTI row, got {len(rows)}')
    aps = rows[0].get('address_points', [])
    if len(aps) != 1:
        raise RuntimeError(f'{simple_name}: expected one vtable AP, got {len(aps)}')
    return {'rtti_name': rows[0]['rtti_name'], 'rtti': rows[0]['rtti'], **aps[0]}


required_generated_offsets = tuple(hex(value) for value in range(0, 0x68, 8))


def generated_vtable_slots(vtable: dict) -> list[dict]:
    by_offset = {row['offset']: row for row in vtable['slots']}
    rows = []
    for offset in required_generated_offsets:
        row = by_offset.get(offset)
        if row is None:
            raise RuntimeError(f"{vtable['rtti_name']}: missing generated slot {offset}")
        rows.append(row)
    return rows



def function_snapshot(img: Image, target: int) -> dict:
    return fde_instructions(img, target, limit=1200)


def wire_fields(snapshot: dict) -> dict:
    immediates = []
    memory = []
    calls = []
    for row in snapshot['instructions']:
        op = row['operand']
        if row['mnemonic'] in ('mov', 'cmp', 'test') and re.search(r'\b0x[0-9a-f]+\b|, [0-9]+$', op):
            immediates.append(row)
        if '[' in op and ']' in op:
            memory.append(row)
        if row['mnemonic'] == 'call':
            calls.append(row)
    return {'immediate_candidates': immediates, 'memory_candidates': memory, 'calls': calls}


GLOBAL_IMAGE: Image


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', type=Path, required=True)
    ap.add_argument('--version', required=True)
    ap.add_argument('--packed-sha256', required=True)
    ap.add_argument('--unpacked-sha256', required=True)
    ap.add_argument('--unpacked-size', type=int, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()

    global GLOBAL_IMAGE
    GLOBAL_IMAGE = Image(args.client)
    classes = {}
    for name in MESSAGE_CLASSES:
        vt = recover_vtable(GLOBAL_IMAGE, name)
        generated_vtable_slots_current = generated_vtable_slots(vt)
        slot_snapshots = {}
        for slot in generated_vtable_slots_current:
            offset = slot['offset']
            if slot.get('executable'):
                target = int(slot['target'], 16)
                snapshot = function_snapshot(GLOBAL_IMAGE, target)
                slot_snapshots[offset] = {
                    'target': slot['target'],
                    'snapshot': snapshot,
                    'wire_fields': wire_fields(snapshot),
                }
            else:
                slot_snapshots[offset] = {'target': slot['target'], 'snapshot': None}
        classes[name] = {
            'rtti_name': vt['rtti_name'],
            'rtti': vt['rtti'],
            'vtable_ap': vt['address_point'],
            'generated_vtable_slots': generated_vtable_slots_current,
            'slot_snapshots': slot_snapshots,
        }

    login_handler = recover_exact_named_vtable(
        GLOBAL_IMAGE, 'TLoginProtocolMessageHandler',
        'tibia::authentication::TLoginProtocolMessageHandler')
    auth_info = recover_exact_named_vtable(
        GLOBAL_IMAGE, 'TAuthenticationAndEncryptionInfo',
        'tibia::authentication::TAuthenticationAndEncryptionInfo')

    login_ap = int(classes['GameclientMessageLogin']['vtable_ap'], 16)
    rsa_ap = int(classes['LoginRSAEncryptedBlock']['vtable_ap'], 16)
    producer_reference_intersection = reference_scan(GLOBAL_IMAGE, {login_ap, rsa_ap}, set())['rip']

    def fde_key(site: int) -> str | None:
        fde = GLOBAL_IMAGE.containing_fde(site)
        return f'{hx(fde[0])}..{hx(fde[1])}' if fde else None

    login_fdes = {fde_key(site) for site in producer_reference_intersection.get(login_ap, [])}
    rsa_fdes = {fde_key(site) for site in producer_reference_intersection.get(rsa_ap, [])}
    common_fdes = sorted((login_fdes & rsa_fdes) - {None})
    login_handler_owner_slots = []
    for slot in login_handler['slots']:
        if not slot.get('executable'):
            continue
        target = int(slot['target'], 16)
        key = fde_key(target)
        if key in common_fdes:
            login_handler_owner_slots.append({**slot, 'fde': key})
    producer_candidates = []
    for key in common_fdes:
        lo_s, hi_s = key.split('..')
        lo = int(lo_s, 16)
        producer_candidates.append({
            'fde': [lo_s, hi_s],
            'login_vtable_refs': [hx(site) for site in producer_reference_intersection.get(login_ap, []) if fde_key(site) == key],
            'rsa_vtable_refs': [hx(site) for site in producer_reference_intersection.get(rsa_ap, []) if fde_key(site) == key],
            'snapshot': fde_instructions(GLOBAL_IMAGE, lo, limit=1600),
        })

    result = {
        'schema': 'otclient.track-a.current-game-login-schema.discovery.v1',
        'exact_client': {
            'version': args.version,
            'packed_sha256': args.packed_sha256,
            'unpacked_sha256': args.unpacked_sha256,
            'unpacked_size': args.unpacked_size,
        },        'runtime_access': 'none',
        'login_performed': False,
        'secret_access': False,
        'raw_client_uploaded': False,
        'classes': classes,
        'login_handler': login_handler,
        'authentication_info': auth_info,
        'producer_reference_intersection': {hx(k): [hx(site) for site in v] for k, v in producer_reference_intersection.items()},
        'login_handler_owner_slots': login_handler_owner_slots,
        'producer_candidates': producer_candidates,
        'classification': {
            'current_rtti_vtables': 'PROVEN',
            'current_generated_method_slots': 'DISCOVERY_ONLY',
            'current_wire_schema': 'UNKNOWN',
            'semantic_field_names': 'UNKNOWN',
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('CURRENT_GAME_LOGIN_SCHEMA_PROBE=PASS')
    print('CURRENT_CLIENT_VERSION=' + args.version)
    for name, row in classes.items():
        print('SCHEMA_CLASS=' + name)
        print('SCHEMA_VTABLE=' + row['vtable_ap'])
        print('SCHEMA_GENERATED_SLOT_COUNT=' + str(len(row['generated_vtable_slots'])))
    print('PRODUCER_CANDIDATE_COUNT=' + str(len(producer_candidates)))
    print('LOGIN_HANDLER_OWNER_SLOT_COUNT=' + str(len(login_handler_owner_slots)))
    print('RAW_CLIENT_UPLOADED=false')
    print('LOGIN_PERFORMED=false')
    print('SECRET_ACCESS=false')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
